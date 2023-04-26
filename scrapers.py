import httpx
import logging
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as BS

from urls import (ENGEN,
                  SHELL,
                  CALTEX)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='scraping_log.log', encoding='utf-8', level=logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


class Scraper(ABC):
    @abstractmethod
    def __init__(self,):
        self._url = None
        self._raw_data = None

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
    def get_prices(self,) -> dict:
        '''
        Returns the fuel price dictionary

        Returns:
            prices (dict): The fuel price dictionary
        '''
        pass

class ShellScraper(Scraper):
    def __init__(self,):
        super().__init__()
        self._url = SHELL
        self._coastal_fuel_prices = {}
        self._inland_fuel_prices = {}

    
    def _get_data(self,):
        '''
        Gets the raw HTML data from the Shell website
        '''
        self._raw_data = httpx.get(self._url)
        if self._raw_data.status_code != 200:
            raise Exception(f'Could not get data from {self._url}')


    def _parse_data(self,):
        soup = BS(self._raw_data.text, 'lxml')
        fuel_table_inland = soup.find_all('table', class_='tg')[0] # First table is the inland table
        fuel_table_coastal = soup.find_all('table', class_='tg')[1] # Second table is the coastal table
        
        inland_fuel_types = fuel_table_inland.find_all(name='td', class_='tg-432b')
        coastal_fuel_types = fuel_table_coastal.find_all(name='td', class_='tg-d3q2')

        inland_fuel_prices = fuel_table_inland.find_all(name='td', class_='tg-4qlf')
        coastal_fuel_prices = fuel_table_coastal.find_all(name='td', class_='tg-818t')

        inland_fuel_types = map(lambda x:x.text, inland_fuel_types)
        coastal_fuel_types = map(lambda x:x.text, coastal_fuel_types)
        
        inland_fuel_prices = map(lambda x:x.text, inland_fuel_prices)
        coastal_fuel_prices = map(lambda x:x.text, coastal_fuel_prices)

        for fuel_type, fuel_price in zip(inland_fuel_types, inland_fuel_prices):
            if fuel_type and fuel_price:
                self._inland_fuel_prices[fuel_type] = fuel_price

        for fuel_type, fuel_price in zip(coastal_fuel_types, coastal_fuel_prices):
            if fuel_type and fuel_price:
                self._coastal_fuel_prices[fuel_type] = fuel_price
    

    def get_data(self,):
        '''
        Requests data from the Shell website API and stores it in fuel price dictionaries

        Args:
            None

        Returns:
            None
        '''
        try:
            self._get_data()
        except Exception as err:
            self._inland_fuel_prices = None
            self._coastal_fuel_prices = None
            logger.error(err)
        else:
            self._parse_data()

    def get_prices(self,):
        '''
        Returns a list of usable fuel price dictionaries

        Args:
            None

        Returns:
            list[dict, dict]: The coastal fuel price dictionary and the inland fuel price dictionary
        '''
        return [self._coastal_fuel_prices, self._inland_fuel_prices]

class CaltexScraper(Scraper):
    def __init__(self,):
        super().__init__()
    
    def _get_data(self,):
        pass

    def _parse_data(self,):
        pass

    def get_prices(self,):
        pass

class EngenScraper(Scraper):
    def __init__(self,):
        super().__init__()
        self._url = ENGEN
        self._coastal_fuel_prices = {}
        self._inland_fuel_prices = {}
        

    def _get_data(self,) -> None:
        '''
        Gets the raw json data from the Engen API

        Raises:
            Exception: If could not retrieve data from API
        '''
        self._raw_data = httpx.get(self._url)
        if self._raw_data.status_code != 200:
            raise Exception(f'Could not get data from {self._url}')


    def _parse_data(self,) -> None:
        '''
        Parses the data into usable fuel price dictionaries

        Args:
            None
        
        Returns:
            None
        '''
        data = self._raw_data.json()['response']['data']['prices']
        for item in data:
            if 'coastal' in item.values():
                self._coastal_fuel_prices[item['fuel_type']] = f"{item['currency']}{item['price']}"
            elif 'inland' in item.values():
                self._inland_fuel_prices[item['fuel_type']] = f"{item['currency']}{item['price']}"


    def get_data(self,) -> None:
        '''
        Requests data from the Engen API and stores it in fuel price dictionaries

        Args:
            None

        Returns:
            None
        '''
        try:
            self._get_data()
        except Exception as err:
            self._inland_fuel_prices = None
            self._coastal_fuel_prices = None
            logger.error(err)
        else:
            self._parse_data()


    def get_prices(self,) -> list[dict, dict]:
        '''
        Returns a list of usable fuel price dictionaries

        Args:
            None

        Returns:
            list[dict, dict]: The coastal fuel price dictionary and the inland fuel price dictionary
        '''
        return [self._coastal_fuel_prices, self._inland_fuel_prices]