import json
from pathlib import Path
import shutil
from typing import Optional
from logger import log_move, log_skip

def load_config() -> dict:
    with open("config.json","r") as f:
        return json.load(f)
    

def get_folder_name(f_name: str, config: dict) -> Optional[str]:
    ori_name=Path(f_name).stem #ignore the file type
    prefix=ori_name.split('_',1)[0] #get the prefix (part before _)
    if ('_' in ori_name):
        return config["course_aliases"].get(prefix,prefix)
    else:
        return None
    
def move(src_path:Path, config:dict, dry:bool = False)->bool:
    if (src_path.suffix.lower() not in config['allowed_format']):
        log_skip(src_path,"Invalid file type")
        return False
    if (src_path.suffix == '.crdownload'):
        log_skip(src_path,"Not finished download")
        return False #Still downloading, don't move it
    folder_name=get_folder_name(src_path, config)
    if not folder_name:
        target=Path(config["downloads_folder"])/'Unsorted' #default unsorted location
    else:
        target=Path(config["downloads_folder"])/folder_name #target folder

    target.mkdir(exist_ok=True) #make new folder when needed
    tar_path = target/src_path.name

    #if duplicate
    cnt=1
    while tar_path.exists():
        stem=src_path.stem
        tar_path=target/f"{stem}_{cnt}{src_path.suffix}"
        cnt+=1
    
    if dry:
        #print(f"Would move: {src_path} → {tar_path}")
        log_move(src_path,tar_path)
        return True
    
    shutil.move(str(src_path), str(tar_path)) #move
    # print(f"Moved: {src_path.name} → {tar_path.name}/")
    log_move(src_path,tar_path)
    return True