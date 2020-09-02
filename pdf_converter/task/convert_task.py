import uuid

class ConvertTask:
    def __init__(self, pdf_data):
        self.id = uuid.uuid4()
        self.pdf_data = pdf_data

