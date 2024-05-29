import pandas as pd
import requests
import os
import datetime
import progressbar
from tqdm import tqdm

import log_manager
import file_manager as FM

# pyinstaller -n "IMAGE_DOWNLOAD_PROGRAM" --clean --onefile main.py

def get_img_hrefs(logger: log_manager.Logger, file_path):
    img_hrefs = []
    img_names = []

    data = pd.read_csv(file_path)
    img_hrefs = data["URL"]
    img_names = data["NAME"]

    logger.log_info(f"총 {len(img_hrefs)}개의 이미지 링크를 발견 하였습니다!")

    return img_hrefs, img_names

def download_image(logger: log_manager.Logger, img_url, img_name, img_path, download_cnt, proxy=None):
    if proxy:
        proxy_str = f"{proxy[0]}:{proxy[1]}:{proxy[2]}:{proxy[3]}"
        r = requests.get(img_url,headers={'User-Agent': 'Mozilla/5.0'}, timeout=20, proxies={'http':proxy_str,'https':proxy_str})
    else:
        r = requests.get(img_url,headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
    with open(f"{img_path}/{img_name}", "wb") as outfile:
        outfile.write(r.content)
    return
if __name__ == '__main__':
    file_manager = FM.FileManager()
    logger = log_manager.Logger(log_manager.LogType.BUILD)

    file_manager.create_dir("./output")
    now = datetime.datetime.now()
    year = f"{now.year}"
    month = "%02d" % now.month
    day = "%02d" % now.day
    hour = "%02d" % now.hour
    minute = "%02d" % now.minute

    output_name = f"{year}{month}{day}{hour}{minute}"
    output_path = f"./output/{output_name}"
    file_manager.create_dir(output_path)

    input_path = "./input.csv"
    img_hrefs, img_names = get_img_hrefs(logger, input_path)

    img_cnt = len(img_hrefs)

    logger.log_info(f"총 {img_cnt}개의 이미지 다운로드를 시작합니다.")
    progress_bar = progressbar.ProgressBar(maxval=img_cnt).start()

    pbar = tqdm(range(img_cnt), unit = 'download')
    for i in pbar:
        download_image(logger=logger, img_url=img_hrefs[i], img_name=img_names[i].replace("/","-"), img_path=output_path, download_cnt=0)
        progress_bar.update(i)
    
