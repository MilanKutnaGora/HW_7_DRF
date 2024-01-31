import re

from rest_framework.exceptions import ValidationError


class UrlValidator:

    def __init__(self, url):
        self.url = url

    def __call__(self, value):
        tmp_val = dict(value).get(self.url)
        if "youtube.com" not in tmp_val:
            raise ValidationError('URL is forbidden')