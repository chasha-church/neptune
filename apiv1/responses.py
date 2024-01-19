import csv

from django.http.response import StreamingHttpResponse


# https://docs.djangoproject.com/en/1.9/howto/outputting-csv/#streaming-large-csv-files
class CSVEcho(object):
    def write(self, value):
        return value


class CSVStreamingHttpResponse(StreamingHttpResponse):
    # TODO: timeout?
    def csv_generator(self, queryset):
        yield self.writer.writerow([key for key in self.headers])
        for serialized_instance in queryset:
            yield self.writer.writerow(
                [serialized_instance.get(field, None) for field in self.headers]
            )

    def __init__(self, headers, queryset=(), writer_settings={}, *args, **kwargs):
        self.headers = headers
        self.writer = csv.writer(CSVEcho(), **writer_settings)
        streaming_content = self.csv_generator(queryset)
        kwargs['content_type'] = 'text/csv'
        super(CSVStreamingHttpResponse, self).__init__(streaming_content, *args, **kwargs)

