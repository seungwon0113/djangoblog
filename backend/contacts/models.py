from django.db import models


class Inquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "inquiries"
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"
