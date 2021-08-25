from .web_page_parser import DevzillasWebPageParser
from bs4 import BeautifulSoup
from .table_data_scraper import scrape_table


class AllCoinScraper(DevzillasWebPageParser):
    def __init__(self):
        pass

    @staticmethod
    def urls_len(urls):
        return len(urls)

    @staticmethod
    def get_url(urls, index):
        return urls[index]['url']

    @staticmethod
    def get_parameters(urls, index):
        return urls[index]

    @staticmethod
    def pars(
            index,
             urls,
            drivers,
            max_workers,
            out_parsed_data_in_levels,
            model
    ):
        url = AllCoinScraper.get_url(urls, index)
        driver = drivers[index % max_workers].result()

        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, features="html.parser")
        all_coins_table = soup.find("table", {"class": "table"})
        rows = scrape_table(all_coins_table,model)
        out_parsed_data_in_levels.extend(rows)
