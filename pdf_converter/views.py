# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pdf_converter.task.convert_task import ConvertTask
from pdf_converter.converter.pdf_converter import PDFConverter
from django.utils.decorators import method_decorator
from django.views import View
from pymongo import MongoClient
from pdf_converter.models import ConverterResponse
import json
from django.core.exceptions import SuspiciousOperation
import gridfs

# Run local conversion of PDF file and insert output PNG into DB.
# Respond with image URLs
class ConvertController(View):

    def __init__(self):
        self.converter = PDFConverter()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ConvertController, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist("pdf")
        if len(files) == 0:
            raise Exception("Must use \'pdf\' as key for each file, or no files to convert were provided")

        responses = []
        for file in files:
            file_name = str(file)
            last_three_char = file_name[(len(file_name) - 3): (len(file_name))]
            if last_three_char.lower() != "pdf":
                print(f"File {file_name} does not appear to be a PDF -- skipping")
                continue
            pdf_data = file.read()
            task = ConvertTask(pdf_data)
            image_file_urls = self.converter.do_convert(task)
            response = ConverterResponse(task.id, file_name, image_file_urls)
            # return the names of what will (hopefully) be in the db before customer accesses URL
            responses.append(response.__dict__)

        return JsonResponse({"data": responses})

# Respond to GET requests for images by accessing MongoDB using GridFS
class ImageController(View):

    def __init__(self):
        self.db_client = MongoClient()
        self.db = self.db_client['pdf_converter']
        self.image_fs = gridfs.GridFS(self.db, collection='image_collection')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ImageController, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # parse path to get resource id.
        # TODO: Add this functionality in url router
        image_id = request.path.split("/")[-1]
        image_data = self.image_fs.get(image_id)
        return HttpResponse(image_data, content_type="image/jpeg")
