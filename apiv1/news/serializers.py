from rest_framework import serializers

from apiv1.assets.utils import get_asset_url_by_file_name
from db import models


class NewsListSerializer(serializers.ModelSerializer):
    created_by_id = serializers.IntegerField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    updated_by_id = serializers.IntegerField(read_only=True, allow_null=True)
    updated_date = serializers.DateTimeField(read_only=True, allow_null=True, default='null')
    main_asset_url = serializers.SerializerMethodField()

    @staticmethod
    def get_main_asset_url(obj):
        return get_asset_url_by_file_name(obj.main_asset.file_name) if obj.main_asset else None

    class Meta:
        model = models.NewsContent
        fields = (
            'news_content_id',
            'title',
            'main_asset_url',
            'created_date',
            'created_by_id',
            'updated_date',
            'updated_by_id',
        )


class NewsDetailsSerializer(NewsListSerializer):
    assets_url = serializers.SerializerMethodField()

    @staticmethod
    def get_assets_url(obj):
        return [get_asset_url_by_file_name(asset.file_name) for asset in obj.assets.all() if asset.file_name]

    class Meta:
        model = models.NewsContent
        fields = (
            'news_content_id',
            'title',
            'text',
            'view_data',
            'main_asset_url',
            'assets_url',
            'created_date',
            'created_by_id',
            'updated_date',
            'updated_by_id',
        )
