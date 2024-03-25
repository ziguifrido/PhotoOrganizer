import os
import shutil
from PIL import Image
from datetime import datetime

class PhotoOrganizer:
    DATETIME_EXIF_ID = 36867
    extensions = ['jpg', 'jpeg', 'png']

    def get_date(self, file):
        photo = Image.open(file)
        info = photo.getexif()

        if self.DATETIME_EXIF_ID in info:
            date = info[self.DATETIME_EXIF_ID]
            date = datetime.strptime(date, '%Y:%m::%d %H:%M:%S')
        else:
            date = datetime.fromtimestamp(os.path.getmtime(file))

        return date
    
    def get_path(self, file):
        date = self.get_date(file)
        return date.strftime('%Y') + '/' + date.strftime('%m') + '/' + date.strftime('%d')

    def move(self, file):
        folder = self.get_path(file)
        if not os.path.exists(folder):
            os.makedirs(folder)
        shutil.move(file, folder + '/' + file)

    def organize(self):
        photos = [
            filename for filename in os.listdir('.') 
                if os.path.isfile(filename) and any(filename.lower().endswith(ext) for ext in self.extensions)
        ]
        for filename in photos:
            self.move(filename)

PO = PhotoOrganizer()
PO.organize()