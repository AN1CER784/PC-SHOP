import random
import aiohttp
import asyncio

from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
from goods.models import Product, Category
from loguru import logger

SEMAPHORE_LIMIT = 5  # Лимит одновременных запросов
semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)


@sync_to_async
def get_category(slug):
    return Category.objects.get(slug=slug)


@sync_to_async
def create_product(**kwargs):
    return Product.objects.get_or_create(**kwargs)


async def fetch_with_semaphore(session, url):
        await asyncio.sleep(random.uniform(1, 5))
        return await fetch(session, url)


async def fetch(session, url, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            headers = {'User-Agent': UserAgent().random}
            async with session.get(url, headers=headers) as response:
                html = await response.text()
                if "<title>Just a moment...</title>" in html:
                    print(f"Server responded with 'Just a moment...', retrying... ({retries + 1}/{max_retries})")
                    retries += 1
                    await asyncio.sleep(2)
                    continue
                return html
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            retries += 1
            await asyncio.sleep(2)

    print(f"Failed to fetch {url} after {max_retries} retries.")
    return None


async def fetch_and_process_page(session, url, headers, my_category):
    html = await fetch_with_semaphore(session, url)
    if html:
        return await process_page(html, session, headers, my_category)
    return None


async def process_page(page, session, headers, my_category):
    soup = BeautifulSoup(page, 'html.parser')
    all_cards = soup.find_all('div', class_='product product-carousel grid-list')
    tasks = []
    for card in all_cards:
        product_url = card.find('div', 'product-title').find('a').get('href')
        tasks.append(process_product(session, product_url, my_category))
    return await asyncio.gather(*tasks, return_exceptions=True)


async def process_category(session, category_link, headers, my_category):
    base_url = "https://global.microless.com"
    tasks = []

    url = f'{base_url}/{category_link}/l/?sort=popularity'
    html = await fetch_with_semaphore(session, url)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    tasks.append(process_page(html, session, headers, my_category))
    for _ in range(10):
        next_page = soup.find('i', class_='fa fa-angle-double-right fa-fw')
        if not next_page:
            break
        next_page_url = next_page.findParent('a').get('href')
        full_url = f'{base_url}/{next_page_url}'
        tasks.append(fetch_and_process_page(session, full_url, headers, my_category))

        html = await fetch_with_semaphore(session, full_url)
        if not html:
            break
        soup = BeautifulSoup(html, 'html.parser')

    return await asyncio.gather(*tasks, return_exceptions=True)


@logger.catch
async def process_product(session, product_url, my_category):
    html = await fetch_with_semaphore(session, product_url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        product_name = soup.findChild('h1', class_='product-title-h1')
        product_image = soup.find('a', class_='elem image lightbox-opener')
        try:
            description = soup.find('table', class_='table table-bordered table-responsive')
            attributes_list = description.find_all('td')
            if attributes_list:
                product_name = product_name.get_text()
                price = soup.find('span', class_='price-amount').get_text()
                product_image = product_image.get('href')
                json_description = {}
                for i in range(len(attributes_list) // 2):
                    table_cap, table_td = attributes_list[i].findChild('span'), attributes_list[i + 1].findChild('span')
                    if table_cap and table_td:
                        json_description[table_cap.text] = table_td.text

                order = await create_product(
                    name=product_name,
                    description=json_description,
                    image=product_image,
                    price=float(price.replace(',', '.').replace(' ', '')),
                    quantity=random.randint(10, 100),
                    category=await get_category(slug=my_category)
                )
                logger.info("----------------------")
                logger.info(order)
            else:
                logger.warning("Attributes not found.")
        except AttributeError as ex:
            logger.error(ex)


async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://global.microless.com/computer_hardware/l/?sort=popularity"
        headers = {'User-Agent': UserAgent().random}
        html = await fetch_with_semaphore(session, url)

        if html:
            soup = BeautifulSoup(html, 'html.parser')
            all_categories = soup.find_all('div', class_='top-category product product-carousel')
            category_links = [category.find('a').get('href') for category in all_categories[:8]]
            my_category_slugs = ['storage', 'cooling', 'rams', 'cases', 'motherboards', 'gpus', 'psus', 'cpus']
            linked_categories = dict(zip(category_links, my_category_slugs))

            tasks = [process_category(session, category_link, headers, linked_categories[category_link]) for
                     category_link in category_links]
            await asyncio.gather(*tasks, return_exceptions=True)


start_time = time.time()
asyncio.run(main())
