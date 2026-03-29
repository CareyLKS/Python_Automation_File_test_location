import json
from pathlib import Path
import shutil
from organizer import move,load_config
from logger import setup_logger, log_skip
import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#use watchdog to do automation

class Download_Handler(FileSystemEventHandler):
    def __init__(self, config):
        self.config=config
        self.d_path=Path(config["downloads_folder"])

    def on_created(self, event):
        #will auto run when new file appear in the dir
        if (event.is_directory): #Ignore create new file
            return 
        f_path=Path(event.src_path)
        time.sleep(2) #asyn func, wait for download
        if f_path.exists():
            if move(f_path,self.config):
                logger=setup_logger()
                logger.info(f"AUto-organized: {f_path.name}")
            else:
                log_skip(f_path,"not valid")
            
def main():
    config=load_config()
    logger=setup_logger()
    
    print("Starting Download Organizer")
    print(f"Watching: {config['downloads_folder']}")
    print("Press Crtl+C to stop")

    event_h=Download_Handler(config)
    obs=Observer()
    obs.schedule(event_h,config['downloads_folder'],recursive=False)
    obs.start()

    try:
        while 1:
            time.sleep(1)

    except KeyboardInterrupt:
        obs.stop()
        logger.info("Stopped")
        print("\n Stopped")

if __name__=="__main__":
    main()


# if __name__ == "__main__":
#     config = load_config()
#     test_file = Path(r"C:\\Users\\Carey Lee\\Carey\\Python_Automation_File_test_location\\ABC_notes1.pdf")
#     move(test_file, config)