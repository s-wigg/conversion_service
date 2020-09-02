import subprocess
import uuid
import random
import threading
import glob
import os
import errno

import bson

from ..task.convert_task import ConvertTask
from ..db.writer import MongoDBWriter

class PDFConverter:
    def __init__(self):
        self.db_writer = MongoDBWriter()

    # write pdf binary data to tmp file, convert it using subprocess.call(pdftoppm), then take output png data and store in db
    def do_convert(self, task):
        command = "pdftoppm"
        mode = "-png"
        task_id = str(task.id)
        tmp_folder = "tmp/"
        task_entry_path = tmp_folder + task_id + ".pdf"

        # pdftoppm -png tmp/<task_id>.pdf tmp/<task_id>
        command_strings = [command, mode, task_entry_path, "tmp/" + task_id]
        try:
            os.makedirs(os.path.dirname(tmp_folder))
        except OSError as ex:
            if not os.path.isdir(tmp_folder) and ex.errno != errno.EEXIST:
                raise

        pdf_data = task.pdf_data
        with open(task_entry_path, "wb+") as pdf:
            pdf.write(pdf_data)
            pdf.close()

        subprocess.call(command_strings)

        output_png_names = glob.glob("tmp/" + task_id + "*.png")

        pretty_file_names = []
        image_urls = []
        for name in output_png_names:
            # remove path prefix and file extension from filename
            # TODO: make this not gross
            pretty_name = name.split("/")[-1].split(".")[0]
            pretty_file_names.append(pretty_name)
            image_urls.append("image/" + pretty_name)
        os.remove(task_entry_path)

        db_writer_png_input = []
        for filename in output_png_names:
            with open(filename, "rb") as png:
                data = png.read()
                db_writer_png_input.append(data)
                png.close()
            os.remove(filename)

        # process in another thread. (very) optimistically provide URLs back to user before the entries are written to DB
        thread = threading.Thread(target=self.write_data_to_db, args=(task_id, pdf_data, pretty_file_names, db_writer_png_input))
        thread.daemon = True
        thread.start()

        return image_urls

    def write_data_to_db(self, task_id, pdf_data, png_file_names, image_data_list):
        self.db_writer.write_images(png_file_names, image_data_list)
