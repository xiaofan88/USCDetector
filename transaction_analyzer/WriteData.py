import os

import Log
import json

def checkDir(mypath):
    if not os.path.exists(mypath):
        os.makedirs(mypath)

def writeIn(jsonData, path):
    try:
        # mypath = f'Files/Old Contracts'

        Log.Logger(f'{path}.json', level='info').logger.info(str(jsonData))

    except Exception as msg:
        Log.Logger('error.log', level='error', fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s').logger.error(msg)

def write_in_path(json_data, path):

    try:
        # mypath = f'Files/Old Contracts'

        Log.Logger(f'{path}.json', level='info').logger.info(str(json_data))

    except Exception as msg:
        Log.Logger('error.log', level='error', fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s').logger.error(msg)