import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from time import perf_counter

from scraper.predict_scraper import PredictScraper
from scraper.crawler import Crawler
from core.models import Coin
from core.models import Predict


def predict_scraping(max_crawl_pages):
    max_level_of_crawl = 1
    scraped_data = []
    start_time = perf_counter()

    pool = list(Coin.objects.filter(status=1).values())[:50]

    for item in pool:
        item.update({"batch_number": 1})
    try:
        Crawler.start_concurrent_crawling(
            max_crawl_pages,
            max_level_of_crawl,
            (PredictScraper,),
            scraped_data,
            pool,
            20,
            Predict
        )

        # bulk = []
        for item in scraped_data:
            predict = Predict.objects.create(**item)
            predict.save()
            # bulk.append(predict)

        # Predict.objects.bulk_create(bulk)
    except Exception as e:
        print(str(e))

    end_time = perf_counter()
    content = {'total_time_of_crawling_scraping': end_time - start_time,
               'average_time_per_page': (end_time - start_time) / len(pool),
               'max_crawl_pages': max_crawl_pages,
               'max_level_of_crawl': max_level_of_crawl,
               }
    print(content)


if __name__ == '__main__':
    crawl_pages = 1000
    predict_scraping(crawl_pages)
    print('Scarping finished')
