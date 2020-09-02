from pymongo import MongoClient
import gridfs

# Access local MongoDB server with default settings.
# TODO: Use shared MongoDB cluster
class MongoDBWriter():
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['pdf_converter']
        self.image_fs = gridfs.GridFS(self.db, collection='image_collection')
        self.pdf_fs = gridfs.GridFS(self.db, collection='pdf_collection')

    def write_images(self, filenames, data):
        for x in range(0, len(filenames)):
            # remove path prefix from filename
            filename = filenames[x]
            file_data = data[x]
            res = self.image_fs.put(file_data, _id=filename)
            #res = self.image_collection.insert_one({"_id": filename, "data": file_data})
            print("id is " + filename)

    def write_pdf(self, filename, data):
        res = self.pdf_fs.put(data, _id=filename)
        #res = self.pdf_collection.insert_one({"_id": filename, "data": data})
        print("id is " + filename)
