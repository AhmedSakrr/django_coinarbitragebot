import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from time import perf_counter
from scraper.all_coin_scraper import AllCoinScraper
from scraper.crawler import Crawler
from core.models import Coin


def coin_scraping(max_crawl_pages):
    max_level_of_crawl = 1
    start_time = perf_counter()
    all_coin_url = [{'url': 'https://coinarbitragebot.com/coins.php?all_coins'}]
    scraped_data = []
    Crawler.start_concurrent_crawling(max_crawl_pages,
                                        max_level_of_crawl,
                                        (AllCoinScraper,),
                                        scraped_data,
                                        all_coin_url,
                                        10,
                                        Coin)

    try:
        Coin.objects.bulk_create(scraped_data)
    except Exception as e:
        print(str(e))
        pass

    end_time = perf_counter()
    content = {'total_time_of_crawling_scraping': end_time - start_time,
               'average_time_per_page': (end_time - start_time) / max_crawl_pages,
               'max_crawl_pages': max_crawl_pages,
               'max_level_of_crawl': max_level_of_crawl,
               }
    print(content)


if __name__ == '__main__':
    crawl_pages = 1
    coin_scraping(crawl_pages)
    print('Scarping finished')
