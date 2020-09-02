Requirements:

* pdftoppm installed (poppler-utils pkg for linux)
* pip (python package manager)

Installation:

    <set up mongodb>
    <install pdftoppm>
    python3 -m venv <directory for virtual env>
    pip install -r requirements.txt

Running:

With the virtual environment active, change to the root directory and
run `python manage.py runserver`.

Use:

To test service using Postman, upload a file using POST, specify body
as form-data with key "pdf". You can add as many PDFs as you want. They should each have the key "pdf".

Sample Output from /convert
===============

JSON
----

```json
   "data": [
      {
         "id": "1039f1a0-7b32-4b48-8d5b-5de9f9ddb48b",
         "image_urls": [
            "image/1039f1a0-7b32-4b48-8d5b-5de9f9ddb48b-1",
            "image/1039f1a0-7b32-4b48-8d5b-5de9f9ddb48b-2"
         ],
         "file_name": "sample.pdf"
      },
      {
         "id": "7416fa20-90e5-4d2b-9bdb-b07a9bd87f54",
         "image_urls": [
            "image/7416fa20-90e5-4d2b-9bdb-b07a9bd87f54-1"
         ],
         "file_name": "sample2.pdf"
      }
   ]
}
```
