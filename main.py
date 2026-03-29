import json
from pathlib import Path
import shutil
import organizer

if __name__ == "__main__":
    config = organizer.load_config()
    test_file = Path(r"C:\\Users\\Carey Lee\\Carey\\Python_Automation_File_test_location\ABC_notes1.pdf")
    organizer.move(test_file, config)