# %%
import os
import pickle
import inspect
# %%

path = os.path.join(os.path.dirname(__file__))

def _is_path(save_path) -> 'Checks if input is a valid file path':
    if not os.path.isdir(save_path):
        raise FileNotFoundError(f'{save_path} is not a valid file path')


def save_settings(how: str, what: 'obj', where: 'file_name', path: str = path) -> "write pickle file":
    """
    Saves a pickled file in the 'path' variable.

    Parameters
    ----------
    how: the type of action to take place on this file (i.e 'rb' or 'wb')
    what: the object you want to save
    where: specify the name for the pickle file
    """
    _is_path(path)
    hard_settings = open(path + r'/{}.pickle'.format(where), how)
    pickle.dump(what, hard_settings)
    hard_settings.close()


def read_settings(how: str, what: 'path', path: str = path) -> 'reads pickle file':
    """
    Reads a pickled file from the 'path' variable.
    
    Parameters
    ----------
    how: the type of action to take place on this file
    what: the file you want to open

    Returns
    -------
    Open pickle file for loading
    """
    _is_path(path)
    return open(path + r'\{}.pickle'.format(what), how)


Qualtrics_Codes = pickle.load(read_settings('rb', 'Qualtrics_Codes'))
mailing_list = pickle.load(read_settings('rb', 'mailing_list'))


def _in_codes(survey_name, codes=Qualtrics_Codes) -> 'validates code':
    if survey_name not in codes:
        raise KeyError('survey_name must be in saved files.')


def find_args(obj: 'function or class') -> 'list of function/class arguments':
    try: 
        print(obj.__code__.co_varnames)
    except:
        try:
            print(inspect.signature(obj.__init__))
        except:
            raise TypeError('Function or Class required')

# Internal Variables
"""Path for Qualtrics_Codes"""
path = os.path.join(os.path.dirname(__file__))


# internal functions
def _test_type(object, expected_type: type) -> 'Checks var type':
    """
    Checks the type of a variable and throws error if not true
        
    Parameters
    ----------
    object: the object to test type
    expected_type: the type expected of the object

    Returns
    ---------
    Error if the type is not expected
    """
    if not isinstance(object, expected_type):
        raise TypeError('object must be a {} not {}'.format(expected_type.__name__, type(object).__name__, object))

def _is_float(*args):

    try:
        for arg in args:
            float(arg)
        
    except ValueError:

        return False
    
    return True

def _is_file(source: str, file_type: str):

    if os.path.isfile(source) and file_type == source.split('.')[-1]:
        pass
    else:
        raise Exception(f"Path is not file type '{file_type}'")
#%%