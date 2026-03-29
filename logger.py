#log all the movemement

import logging
from pathlib import Path
from datetime import datetime

def setup_logger()->logging.Logger:
    log_dir=Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger=logging.getLogger("file_organizer")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger
    
    file_handler=logging.FileHandler(log_dir/"act.log")
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    logger.addHandler(file_handler)
    return logger

def log_move(src_file:str, tar_fol:str):
    #Success move
    logger = setup_logger()
    logger.info(f"Moved {src_file} → {tar_fol}/")

def log_skip(src_file:str, why:str):
    #Skipped move
    logger = setup_logger()
    logger.info(f"Skipped {src_file} ({why})")

