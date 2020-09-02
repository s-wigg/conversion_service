# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json

# Create your models here.
class ConverterResponse:
    def __init__(self, task_id, file_name, image_urls):
        self.id = str(task_id)
        self.image_urls = image_urls
        self.file_name = file_name
