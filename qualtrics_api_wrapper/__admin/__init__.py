#%%

from qualtrics.__admin.internal_functions import mailing_list, save_settings, read_settings, _in_codes, find_args, _test_type, _is_float, _is_path, _is_file
from qualtrics.__admin.external_functions import generate_validation, reload_codes, add_survey, replacer
from qualtrics.__admin import __exceptions
from qualtrics.__admin.__decorators import time_taken, who

Qualtrics_Codes = reload_codes() 
mailing_list = reload_codes('mailing_list')

def search_codes(name: str) -> 'returns all matched codes':
    matches = [code for code in Qualtrics_Codes if name.lower() in code.lower()]
    return sorted(matches)



#%%