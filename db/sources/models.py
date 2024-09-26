from django.db import models

from db.common.models import CreatedUpdatedData


class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'source'


class SourceAttributes(models.Model):
    source_attribute_id = models.AutoField(primary_key=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'source_attributes'
