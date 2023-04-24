import httpx
from abc import ABC, abstractmethod

from urls import *


class Scraper(ABC):
    @abstractmethod
    def __init__(self,):
        self._url = None
        self._raw_data = None
        self._price_dict = None

    @abstractmethod
    def _get_data(self,):
        '''
        Gets the raw data from the url
        '''
        pass

    @abstractmethod
    def _parse_data(self,):
        '''
        Parses the raw data into a fuel price dictionary
        '''
        pass

    @abstractmethod
    def prices(self,) -> dict:
        '''
        Returns the fuel price dictionary

        Returns:
            prices (dict): The fuel price dictionary
        '''
        pass

class ShellScraper(Scraper):
    def __init__(self,):
        super().__init__()
    
    def _get_data(self,):
        pass

    def _parse_data(self,):
        pass

    def prices(self,):
        pass

class CaltexScraper(Scraper):
    def __init__(self,):
        super().__init__()
    
    def _get_data(self,):
        pass

    def _parse_data(self,):
        pass

    def prices(self,):
        pass

class EngenScraper(Scraper):
    def __init__(self,):
        super().__init__()
        self._url = ENGEN

        self._get_data()
        self._parse_data()
    
    def _get_data(self,):
        self._raw_data = httpx.get(self._url)
        if self._raw_data.status_code != 200:
            raise Exception(f'Could not get data from {self._url}')

    def _parse_data(self,):
        data = self._raw_data.json()['response']['data']['prices']
        price_dict = {}
        for item in data:
            if 'coastal' in item.values():
                price_dict[item['fuel_type']] = f"{item['currency']}{item['price']}"
        self._price_dict = price_dict

    def prices(self,):
        return self._price_dict