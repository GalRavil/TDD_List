from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(blank=False, null=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
