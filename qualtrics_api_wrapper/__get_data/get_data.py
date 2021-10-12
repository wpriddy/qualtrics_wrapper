#%%
from qualtrics.__settings import qualtrics_settings, headers
from qualtrics.__admin import save_settings, read_settings, _in_codes, Qualtrics_Codes, _test_type, _is_path, time_taken
from qualtrics.__admin.internal_functions import path
from qualtrics.__get_data.data_functions import data
import pandas as pd


# %%

class get_qualtrics_data:
    """
    Creates the qualtrics object that houses 
    the properties of the data pull
    
    Params
    ------
    survey_name: the name of the survey as stated in qualtrics
    save_path: the folder where you would like the data to be saved
    file_name: the name of the file to be written
    Optional[sheet_name]: the sheet name for the file to be written
    Optional[partials]: True == only pull the data of those in-progress

    Features
    --------
    pull(write = False): 
        Pulls the data without writing to disk

        Params
        ------
        write: 
            True == write excel file
            False == pandas DataFrame         

    bypass():
        Allows user to pull survey data based 
        solely on name

        Params
        ------
        survey_name: the name of the survey as stated in qualtrics
    
    participation(write = False):
        Pulls the in-progress and completed survey data. 
        If written, data is in two seperate sheets. 

        Params:
        write: 
            True == write excel file
            False == pandas DataFrame 
    
    Returns
    -------
    Pandas DataFrames 

    """
    def __init__(self, survey_name: str, save_path: 'file path', file_name: str, sheet_name: str = '', partials: bool = False, keep_code: bool = False) -> 'Qualtrics Object':
        
        _in_codes(survey_name)

        self._survey_name = survey_name

        self._baseurl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(qualtrics_settings.settings['Data Center'], Qualtrics_Codes[self._survey_name])
        
        _is_path(save_path)

        self._save_path = save_path

        _test_type(file_name, str)
        self._file_name = file_name

        _test_type(sheet_name, str)
        if len(sheet_name) < 31:
            self._sheet_name = sheet_name
        else:
            raise ValueError('sheet_name must be less than 31 characters not {} characters'.format(len(sheet_name)))

        _test_type(partials, bool)
        if not partials:
            self._file_format = '{"format":"csv", "useLabels":"True"}'
        else:
            self._file_format = '{"format":"csv", "useLabels":"True", "exportResponsesInProgress":"True"}'

        _test_type(keep_code, bool)

        self._keep_code = keep_code
        
        self._headers = headers

    """Prints Representation of the Object"""
    def __repr__(self):
        return "Qualtrics Object(\n\t" + f'{self._survey_name=},\n\t{self._save_path=},\n\t{self._file_name=},\n\t{self._sheet_name=}' + ")"

    @time_taken
    def pull(self, write: bool = False) -> 'Qualtrics DataFrame':
        self.data = data(self._baseurl, self._save_path, self._survey_name, self._file_format, self._headers, self._keep_code)
        
        if write:
            writer = pd.ExcelWriter(self._save_path + '\\' + self._file_name + '.xlsx', engine = 'xlsxwriter')
            self.data.to_excel(writer, sheet_name = self._sheet_name, index=False)
            writer.save()

        return self.data

    def participation(self, write: bool = False) -> 'Participation DataFrame':
        _full_format = '{"format":"csv", "useLabels":"True"}'
        _partial_format = '{"format":"csv", "useLabels":"True", "exportResponsesInProgress":"True"}'
        
        _partial_data = data(self._baseurl, self._save_path, self._survey_name, _partial_format, self._headers, self._keep_code)
        _full_data = data(self._baseurl, self._save_path, self._survey_name, _full_format, self._headers, self._keep_code)
        self.data = pd.concat([_partial_data, _full_data])

        if write:
            writer = pd.ExcelWriter(self._save_path + '\\' + self._file_name + ' Participation.xlsx', engine = 'xlsxwriter')
            _full_data.to_excel(writer, sheet_name = 'Complete Data', index = False)
            _partial_data.to_excel(writer, sheet_name = 'Incomplete Data', index = False)
            writer.save()

        return self.data

    @classmethod
    def bypass(cls, survey: 'Qualtrics Code', keep_labels: bool = False) -> 'Pandas DataFrame':
        obj = cls(survey_name = survey, save_path = path, file_name = 'temp', sheet_name = 'temp', partials = False, keep_code = keep_labels)
        data = obj.pull(write=False)

        return data


# %%
