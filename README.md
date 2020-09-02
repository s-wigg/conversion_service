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
as form-data with key "pdf". Output will be JSON representing an
object with a single member named "images" listing the paths to the
images.
