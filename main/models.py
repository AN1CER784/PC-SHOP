from django.db import models


class InfoOnPage(models.Model):
    page_name = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        db_table = 'information_on_page'
        verbose_name = 'Information on page'
        verbose_name_plural = 'Information on pages'

    def __str__(self):
        return self.page_name
