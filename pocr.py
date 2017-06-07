import pygsheets
import PIL
from pytesseract import image_to_string
from PIL import Image
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    DIRECTORY_TO_WATCH = "/Users/andrerand/Documents/ZZ_Local-SFDW-POCR/ZZ_Local_Images_Do_Not_Delete"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Program Terminated")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            
            # Call function to check whether the file is a valid image format. 
            image_path = event.src_path
            is_valid_image = check_valid_image_format(image_path)    
            
            # If file is a valid image format, run the OCR process and push to Google Sheet.
            if is_valid_image:
                text = run_ocr_process(image_path)
                push_to_google_sheet(text)
    

def check_valid_image_format(image_path):
    valid_image_formats = (".bmp",".BMP",".gif",".GIF",".jpg",".JPG",".jpeg",".JPEG",".png",".PNG",".raw",".RAW",".tif",".TIF",".tiff",".TIFF",".svg",".SVG")
 
    return(image_path.endswith(valid_image_formats))

def run_ocr_process(image_path):
    # Open the Image
    image = Image.open(image_path) 
        
    # Convert the Image to Text
    text = image_to_string(image)
    
    return text
    
def push_to_google_sheet(text):
    gc = pygsheets.authorize(service_file='/Users/andrerand/Documents/ZZ_Local-SFDW-POCR/ZZ_Google_JSON_Do_Not_Delete/service_creds.json')
    sh = gc.open('SFDW POCR')
    wks = sh.sheet1
    
    text_list = [text]
    wks.insert_rows(1, number=1, values=text_list)

if __name__ == '__main__':
	w = Watcher()
	w.run()