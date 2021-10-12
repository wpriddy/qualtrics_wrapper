#%%
from qualtrics.__settings import qualtrics_settings, headers
from qualtrics.__admin import _in_codes, mailing_list, Qualtrics_Codes, replacer, save_settings, read_settings, mailing_list, _test_type, _is_path
import requests as r
import json
from datetime import datetime
import pandas as pd
# %%
data_center = qualtrics_settings.settings['Data Center']
owner_id = qualtrics_settings.settings['Owner Id']


def generate_mailing_list():
    baseurl = f'https://{data_center}.qualtrics.com/API/v3/mailinglists'
    lists = {}

    while baseurl is not None:

        """Pulls Surveys from the Past Number of Designated Years"""
        pull = {_list['name'] : {'id': _list['id'], 'category': _list['category']}
                for _list in json.loads(r.get(baseurl, headers=headers).content.decode('utf-8'))['result']['elements']}

        """Updates Dictionary"""
        lists = {**lists, **pull}

        """Gets Next Offset - API Update in the Works to be Able to Pull All"""
        baseurl = json.loads(r.get(baseurl, headers=headers).content.decode('utf-8'))['result']['nextPage']
    
    save_settings('wb', contacts, 'mailing_list')

    return lists
 

class get_mailing_list():

    def __init__(self, list_name):
        _test_type(list_name, str)
        _in_codes(list_name, mailing_list)
        

        self._listData = mailing_list[list_name]
        self._listId = mailing_list[list_name]['id']
        self._list_name = list_name

        self._baseurl = f'https://{data_center}.qualtrics.com/API/v3/mailinglists/{self._listId}/contacts'
        self._updateurl = f'https://{data_center}.qualtrics.com/API/v3/mailinglists/{self._listId}/contacts/'

    
    def get_contacts(self):
        
        self._contacts = {}    
        
        while self._baseurl is not None:

            call = json.loads(r.get(self._baseurl, headers=headers).content.decode('utf-8'))['result']['elements']

            """Pulls Surveys from the Past Number of Designated Years"""
            self._keys = ['firstName', 'lastName', 'email', 'embeddedData', 'externalDataReference', 'unsubscribed', 'id']
            pull = {}

            for enum, _list in enumerate(call):
                num = str(enum) + '. '
                try:
                    name = num + _list['firstName'] + ' ' + _list['lastName']
                except TypeError:
                    try:
                        name = num + _list['firstName']
                    except:
                        #TODO potential for more test cases
                        print(_list['firstName'], _list['lastName'])
                finally:
                    pull[name] = {}
                    for key in self._keys:
                        pull[name][key] = _list[key]

            """Updates Dictionary"""
            self._contacts = {**self._contacts, **pull}

            """Gets Next Offset - API Update in the Works to be Able to Pull All"""
            self._baseurl = json.loads(r.get(self._baseurl, headers=headers).content.decode('utf-8'))['result']['nextPage']
            
        return self._contacts

    @property
    def contacts(self):
        return self._contacts

# %%
