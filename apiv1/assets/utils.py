from django.conf import settings


def get_asset_url_by_file_name(file_name: str) -> str:
    return settings.AWS_S3_URL.format(bucket_name=settings.AWS_S3_BUCKET_NAME, file_name=file_name)
