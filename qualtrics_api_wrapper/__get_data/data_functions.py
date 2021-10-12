# %%
from qualtrics.__settings import qualtrics_settings
import requests as r
import pandas as pd
import zipfile
import io
import time
import pickle
import sys
from datetime import datetime
import json


def data(baseUrl: str, save_path: 'filepath', survey_name: str, file_format: str, headers: dict, keep_code: bool) -> pd.DataFrame:
    """Pulls the data into the designated filepath""".title()

    progress_status = 'in Progress'
    request_response = r.request("POST", baseUrl, data=file_format, headers=headers)
    progressId = request_response.json()["result"]["progressId"]

    """checks progress of download"""
    while progress_status != "complete" and progress_status != "failed":
        check_url = baseUrl + progressId
        check_request = r.request("GET", check_url, headers=headers)
        progress_status = check_request.json()["result"]["status"]
        
    print(progress_status.title())

    """gets file"""
    fileId = check_request.json()["result"]["fileId"]
    download_url = baseUrl + fileId + '/file'
    download_request = r.request("GET", download_url, headers=headers, stream=True)

    """saves file"""
    _file = zipfile.ZipFile(io.BytesIO(download_request.content))

    """reads and minor transformations"""
    if keep_code:
        dataFrame = pd.read_csv(_file.open(f'{survey_name}.csv'))
        dataFrame = dataFrame.drop([0, 1], axis=0).reset_index(drop=True)
    else:
        dataFrame = pd.read_csv(_file.open(f'{survey_name}' + '.csv'), header=1)
        dataFrame.columns = [i.replace('\n', ' ') for i in dataFrame.columns]
        dataFrame = dataFrame.drop([0, 1], axis=0).reset_index(drop=True)


    """Convert text to numbers"""
    for column in dataFrame.columns:
        for row in range(len(dataFrame[column])):
            try:
                dataFrame[column][row] = dataFrame[column][row].replace(',', '_')      
                dataFrame[column][row] = float(dataFrame[column][row])
            except (AttributeError, ValueError):
                pass
    
    return dataFrame
    




# %%
