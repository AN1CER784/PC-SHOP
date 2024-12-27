from django.views.generic import TemplateView, DetailView
from main.models import InfoOnPage


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Main"
        context["content"] = "PC Shop"
        return context


class AboutView(DetailView):
    model = InfoOnPage
    template_name = "main/about.html"
    context_object_name = "info"

    def get_object(self, queryset=None):
        return InfoOnPage.objects.get(page_name="about")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "About"
        return context


class ContactView(DetailView):
    template_name = "main/contact.html"
    context_object_name = "info"

    def get_object(self, queryset=None):
        return InfoOnPage.objects.get(page_name="contact")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contact"
        return context
