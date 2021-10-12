#%%
from qualtrics.__settings import headers, qualtrics_settings
from qualtrics.__admin import _in_codes, Qualtrics_Codes, _test_type
import requests as r

data_center = qualtrics_settings.settings['Data Center']
ownerId = qualtrics_settings.settings['Owner Id']

class manage_survey:
    """
    Allows admin level changes to surveys including:
        Changing Survey Name
        Activating or Closing Survey
        Changing Survey Expiration
    
    Params
    ------
    survey_name: the name of the survey as stated in qualtrics

    Features
    --------
    update_survey():
        function to provide updates to provided survey

        Params
        ------
        kwargs: list of acceptable changes to survey       
    """

    def __init__(self, survey_name):
        
        _test_type(survey_name, str)
        _in_codes(survey_name)

        self._surveyId = Qualtrics_Codes[survey_name]
        self._survey_name = survey_name

        self._payload = {'{\"name\":\"': self._survey_name, '\",\"isActive\":': 'true', 
        ',\"expiration\":{\"startDate\":\"': '2020-01-01', 'T12:30:00Z\",\"endDate\":\"': '2020-09-29',
        'T19:30:00Z\"},\"ownerId\":\"': ownerId, '': '\"}"'}

        self._baseurl = f'https://{data_center}.qualtrics.com/API/v3/surveys/{self._surveyId}'

    def __repr__(self):
        return f'Survey Management: {self._survey_name}'

    def update_survey(self, **kwargs) -> 'Updates Survey Information':
        
        for key, value in kwargs.items():
            _test_type(key, str)
            _test_type(value, str)

            if key in (name := '{\"name\":\"'):
                self._payload[name] = value
            
            elif key in (Active := '\",\"isActive\":'):
                self._payload[Active] = value

            elif key in (start := ',\"expiration\":{\"startDate\":\"'):
                self._payload[start] = value 
            
            elif key in (end := 'T12:30:00Z\",\"endDate\":\"'):
                self._payload[end] = value
            else:
                raise KeyError('kwargs must be in ["name", "Active", "startDate", "endDate"]')

        self._json_str = ''.join([key + value for key, value in self._payload.items()])
        response = r.put(self._baseurl, headers=headers, data = self._json_str)
        
        if '200 - OK' in str(response.content):
            print('Successful Update')
        else:
            raise Exception('Failed to Update')



# %%

# %%
