from .scrapers import (ShellScraper,
                      EngenScraper,
                      CaltexScraper,)


def display_prices(prices: list):
    pass


def main():
    shell = ShellScraper()
    engen = EngenScraper()
    caltex = CaltexScraper()

    prices = []
    prices.append(shell.prices())
    prices.append(engen.prices())
    prices.append(caltex.prices())

    display_prices(prices)


if __name__ == '__main__':
    main()