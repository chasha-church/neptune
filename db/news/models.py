from datetime import datetime

from django.db import models


class NewsContentAssets(models.Model):
    news_content_asset_id = models.AutoField(primary_key=True)
    news_content = models.ForeignKey('NewsContent', on_delete=models.CASCADE)
    asset = models.ForeignKey('Assets', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'news_content_assets'


class NewsContent(models.Model):
    news_content_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    view_data = models.JSONField(null=True)

    main_asset = models.ForeignKey('Assets', on_delete=models.DO_NOTHING, related_name='news_with_mian_asset', null=True)
    assets = models.ManyToManyField('Assets', through="NewsContentAssets", related_name='news_with_asset')

    created_date = models.DateTimeField(default=datetime.utcnow)
    created_by_id = models.IntegerField()
    updated_date = models.DateTimeField(default=datetime.utcnow)
    updated_by_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news_content'


class Assets(models.Model):
    asset_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=500)

    created_date = models.DateTimeField(default=datetime.utcnow)
    created_by_id = models.IntegerField()
    updated_date = models.DateTimeField(default=datetime.utcnow)
    updated_by_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'assets'
