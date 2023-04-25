from scrapers import (ShellScraper,
                      EngenScraper,
                      CaltexScraper,)


def display_prices(prices: list):
    pass


def main():
    shell = ShellScraper()
    engen = EngenScraper()
    caltex = CaltexScraper()

    prices = []
    prices.append(shell.get_prices())
    prices.append(engen.get_prices())
    prices.append(caltex.get_prices())

    display_prices(prices)


if __name__ == '__main__':
    main()