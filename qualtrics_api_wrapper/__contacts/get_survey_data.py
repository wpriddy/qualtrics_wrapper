
from qualtrics.__settings import qualtrics_settings, headers
from qualtrics.__admin import _in_codes, Qualtrics_Codes, replacer, _test_type, _is_path
import requests as r
import json
from datetime import datetime
import pandas as pd

data_center = qualtrics_settings.settings['Data Center']

Inverted_Qualtrics_Codes = dict(map(reversed, Qualtrics_Codes.items()))

def date_converter(date: str) -> 'cleaned up date':
    strptime = '%Y-%m-%d %H:%M:%S'
    date = datetime.strptime(replacer(date, ' ', 'T', 'Z'), strptime)
    return '-'.join(map(lambda x: str(x), [str(date.month), str(date.day), str(date.year)]))

class survey_distributions:
    """
    Gathers all distributions of a survey and allows 
    access to distribution history metadata and participant links

    Feature
    ---------
    distribution_history():
        Gathers all past distributions metadata in dictionary
        Must be run before get_links()

        Returns
        -------
        {} if no distributions otherwise returns metadata

    get_links():
        Generates a Pandas DataFrame with participants and 
        their survey links

        Must be run after distribution_history()

        Returns
        -------
        Pandas DataFrame if there are distributions
    """
    
    def __init__(self, survey_name):
        _test_type(survey_name, str)
        _in_codes(survey_name)

        self._survey_code = Qualtrics_Codes[survey_name]
    
    def __repr__(self):
        return 'Survey Distributions: ' + Inverted_Qualtrics_Codes[self._survey_code]

    def distribution_history(self) -> 'Returns survey distribution history':
        url = f'https://{data_center}.qualtrics.com/API/v3/distributions?offset=0&surveyId={self._survey_code}'
        response = json.loads(r.get(url, headers=headers).content.decode('utf-8'))['result']['elements']
        
        self._history = {}
        for enum, distribution in enumerate(response):
            try:
                self._history[str(enum + 1) + '. ' + distribution['headers']['subject']] = {'survey': Inverted_Qualtrics_Codes[distribution['surveyLink']['surveyId']],
                                                    'distributionId': distribution['id'],
                                                    'mailingId': distribution['recipients']['mailingListId'],
                                                    'type': distribution['requestType'], 
                                                    'date': date_converter(distribution['sendDate']), 
                                                    'user': distribution['ownerId'],
                                                    'stats': distribution['stats']}
            except KeyError:
                self._history[str(enum + 1) + '. NO SUBJECT'] = {'survey': Inverted_Qualtrics_Codes[distribution['surveyLink']['surveyId']],
                                                    'distributionId': distribution['id'],
                                                    'type': distribution['requestType'], 
                                                    'date': date_converter(distribution['sendDate']), 
                                                    'user': distribution['ownerId'],
                                                    'stats': distribution['stats']}           
            
            if distribution['requestType'] ==  'Invite':
                self._initial_distribution = distribution['id']

        return self._history

    @property
    def history(self):
        return self._history

    def get_links(self) -> 'Returns Excel File':
        try:
            url = f'https://{data_center}.qualtrics.com/API/v3/distributions/{self._initial_distribution}/links?surveyId={self._survey_code}'
            response = json.loads(r.get(url, headers=headers).content.decode('utf-8'))['result']['elements']

            self._contacts = {}
            while url is not None:
    
                """Pulls Surveys from the Past Number of Designated Years"""
                pull = {contact['email'] : {'name': str(contact['firstName']) + ' ' + str(contact['lastName']), 'link': contact['link'], 'optOut': contact['unsubscribed']} for contact in json.loads(r.get(url, headers=headers)\
                    .content.decode('utf-8'))['result']['elements']}

                """Updates Dictionary"""
                self._contacts = {**self._contacts, **pull}

                """Gets Next Offset - API Update in the Works to be Able to Pull All"""
                url = json.loads(r.get(url, headers=headers).content.decode('utf-8'))['result']['nextPage']

        except AttributeError:
            raise Exception('distribution_history must be run first to provide necessary information and survey must have appropriate distribution history')
        return self._contacts

    @property
    def links(self):
        data = pd.DataFrame(self._contacts).T.reset_index()
        data.columns = ['email', 'name', 'link', 'optOut']
        return data
