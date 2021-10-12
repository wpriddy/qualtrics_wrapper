# %%
import os
import pickle
import time
from tqdm import tqdm
import json
import requests as r
from datetime import datetime
from qualtrics.__admin.internal_functions import read_settings, save_settings, _test_type
from qualtrics.__admin.__decorators import time_taken
# %%
qualtrics_settings = pickle.load(read_settings('rb', 'settings'))

headers = {
            "content-type": "application/json",
            "x-api-token": qualtrics_settings['API Token'],
            }

# Internal Variables
"""Path for Qualtrics_Codes"""
path = os.path.join(os.path.dirname(__file__))

# external functions
"""Overwrites previous validation set with new surveys"""
def add_survey(survey_name: str, survey_code: str) -> 'adds survey to Qualtrics_Codes':
    _test_type(survey_name, str)
    _test_type(survey_code, str)
    
    Qualtrics_Codes = reload_codes()

    if (n:=len(survey_code)) != 18: 
        raise Exception(f'survey_code must be 18 characters that starts with SV_ not {n} characters')

    Qualtrics_Codes[survey_name] = survey_code

    save_settings('wb', Qualtrics_Codes, 'Qualtrics_Codes')


def replacer(string, replacement, *args):
    for arg in args:
        string = string.replace(arg, replacement)
    return string[:-1]

@time_taken
def generate_validation() -> 'Pickle File':
    """Generates the validation set of Qualtrics Codes from surveys library"""

    url = 'https://{}.qualtrics.com/API/v3/surveys/'.format(qualtrics_settings['Data Center'])
    
    Qualtrics_Codes = {}

    """Sets the Years"""
    years = [time.localtime().tm_year-1, time.localtime().tm_year]
    strptime = '%Y-%m-%d %H:%M:%S'

    while url is not None:
    
        """Pulls Surveys from the Past Number of Designated Years"""
        pull = {i['name']: i['id'] for i in tqdm(json.loads(r.get(url, headers=headers)
                .content.decode('utf-8'))['result']['elements'], desc="loading validation code set")
                if datetime.strptime(replacer(i['lastModified'], ' ', 'T', 'Z'), strptime).year in years}

        """Updates Dictionary with Relevant Codes"""
        Qualtrics_Codes = {**Qualtrics_Codes, **pull}

        """Gets Next Offset - API Update in the Works to be Able to Pull All"""
        url = json.loads(r.get(url, headers=headers).content.decode('utf-8'))['result']['nextPage']

    save_settings('wb', Qualtrics_Codes, 'Qualtrics_Codes')

    Qualtrics_Codes = reload_codes()


"""Reads DataFrame for Validation"""
def reload_codes(file='Qualtrics_Codes') -> 'loads stored codes':
    if file == 'Qualtrics_Codes':
        Qualtrics_Codes = pickle.load(read_settings('rb', 'Qualtrics_Codes'))
        return Qualtrics_Codes
    else:
        mailing_list = pickle.load(read_settings('rb', 'mailing_list'))
        return mailing_list



#%%