from abc import ABC, abstractmethod

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
    
    def _get_data(self,):
        pass

    def _parse_data(self,):
        pass

    def prices(self,):
        pass