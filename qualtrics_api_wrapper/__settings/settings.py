#%%
import os
from datetime import datetime
import pickle
from qualtrics.__admin.internal_functions import save_settings, read_settings, _test_type
from qualtrics.__admin.__decorators import who

class settings:

    """Configures the authentication
    
    Parameters
    ----------
    api_token: account holder api_token
    data_center: account holder domain
    directory: account holder Pool Id

    Features
    --------
    You can reset values as needed
    
    Returns
    -------
    Stores authenication codes for later use
    """

    def __init__(self, api_token: str = '', data_center: str = '', directory_id: str = '', owner_id: str = '') -> 'configures settings for qualtrics':
        _test_type(api_token, str)
        _test_type(data_center, str)
        _test_type(owner_id, str)
        _test_type(directory_id, str)

        self._api_token = api_token
        self._data_center = data_center
        self._directory_id = directory_id
        self._owner_id = owner_id

        self._storage = {'API Token' : self._api_token, 'Data Center': self._data_center,
                         'Directory Id': self._directory_id, 'Owner Id': self._owner_id}
    
        save_settings('wb', self._storage, 'settings')

    def __repr__(self):
        return 'Qualtrics API settings: ' + str(self._storage)
    
    @property 
    def settings(self):
        return self._storage

    def set_api_token(self, api_token: str) -> 'Updates API Token':
        _test_type(api_token, str)

        self._api_token = api_token
        self._storage = {'API Token' : self._api_token, 'Data Center': self._data_center,
                         'Directory Id': self._directory_id, 'Owner Id': self._owner_id}

        save_settings('wb', self._storage, 'settings')

    def set_data_center(self, data_center: str) -> 'Updates API Token':
        _test_type(data_center, str)

        self._data_center = data_center
        self._storage = {'API Token' : self._api_token, 'Data Center': self._data_center,
                         'Directory Id': self._directory_id, 'Owner Id': self._owner_id}

        save_settings('wb', self._storage, 'settings')

    def set_directory_id(self, directory_id):
        _test_type(directory_id, str)

        self._directory_id = directory_id
        self._storage = {'API Token' : self._api_token, 'Data Center': self._data_center,
                         'Directory Id': self._directory_id, 'Owner Id': self._owner_id}

        save_settings('wb', self._storage, 'settings')

    def set_owner_id(self, owner_id):
        _test_type(owner_id, str)

        self._owner_id = owner_id
        self._storage = {'API Token' : self._api_token, 'Data Center': self._data_center,
                         'Directory Id': self._directory_id, 'Owner Id': self._owner_id}
        
        save_settings('wb', self._storage, 'settings')
         

read_dict = pickle.load(read_settings('rb', 'settings'))

qualtrics_settings = settings(read_dict['API Token'], read_dict['Data Center'], read_dict['Directory Id'], read_dict['Owner Id'])

headers = {
            "content-type": "application/json",
            "x-api-token": qualtrics_settings.settings['API Token'],
            }

def __welcome_message(dict_key: str):
    
    if qualtrics_settings._storage[dict_key] == 'None':
    
        input_api = input("""Welcome to the Qualtrics API Wrapper!
    
        To get started, you will need to input a(n) {} to 
        authenticate your access to your Qualtrics account. This
        
        Would you like to input this now? (Y/N)
        """.format(dict_key))

        if input_api.lower() not in 'yn':

            print('\nInvalid Entry: Enter Y or N\n')
            
            __welcome_message(dict_key)
        
        if input_api.lower() == 'y':
            
            dict_value = input(f'You may now enter your {dict_key}:  ')

            _test_type(dict_key, str)

            qualtrics_settings._storage[dict_key] = dict_value

            save_settings('wb', qualtrics_settings._storage, 'settings')

            print(f'{dict_key} successfully saved.')
        
        else:

            print("""\t\tThat ok! No need to enter now. However to access the functionality
                    of this package, you will need to enter a(n) {} in order to connect 
                    with your Qualtrics account's API. 

                    You can add your information later using one of these functions:

                        qualtrics.qualtrics_settings.set_api_token(API TOKEN: str)

                        qualtrics.qualtrics_settings.set_data_center(DATA CENTER: str)

                        qualtrics.qualtrics_settings.set_owner_id(OWNER ID: str)

                        qualtrics.qualtrics_settings.set_directory_id(DIRECTORY ID: str)

            """.format(dict_key))
# %%
