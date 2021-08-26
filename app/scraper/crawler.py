from concurrent.futures import ProcessPoolExecutor
from .web_page_parser import DevzillasWebPageParser
import concurrent.futures
from concurrent.futures import wait, ALL_COMPLETED

session = None


class Crawler:

    @staticmethod
    def start_concurrent_crawling(max_crawl_pages, max_level_of_crawl, parsers, out_parsed_data_in_levels, urls,
                                  max_workers, model):
        Crawler.start_crawling(max_crawl_pages,
                               max_level_of_crawl,
                               parsers,
                               out_parsed_data_in_levels,
                               urls,
                               max_workers,
                               model
                               )

    @staticmethod
    def start_crawling(
            max_crawl_pages,
            max_level_of_crawl,
            parsers,
            out_parsed_data_in_levels,
            urls_in, max_workers,
            model
    ):
        # if max_crawl_pages > 30 and settings.DEBUG:
        #     max_crawl_pages = 30
        if len(parsers) < max_level_of_crawl and max_level_of_crawl > 0:
            raise ValueError("parsers len must be equal to max level of crawl")

        for level in range(max_level_of_crawl):
            if issubclass(parsers[level], DevzillasWebPageParser):
                if urls_in:
                    urls = urls_in
                else:
                    urls = out_parsed_data_in_levels[level - 1] if level > 0 else None
                parser = parsers[level]
                parsed_data_in_this_level = []

                Crawler.start_crawling_urls(
                    max_crawl_pages,
                    urls,
                    parser,
                    parsed_data_in_this_level,
                    max_workers,
                    model
                )
                # completed, pending = await asyncio.wait(blocking_tasks)
                out_parsed_data_in_levels.extend(parsed_data_in_this_level)
            else:
                print(level, max_level_of_crawl)
                print(parsers)
                raise TypeError('all parsers must inherited of WebPageParser')

    @staticmethod
    def start_crawling_urls(
            max_crawl_pages,
            urls,
            parser,
            out_parsed_data_in_levels,
            max_workers,
            model
    ):
        if not issubclass(parser, DevzillasWebPageParser):
            raise TypeError('parser have to inherited of WebPageParser')

        _parser = parser
        drivers = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for _ in range(min(_parser.urls_len(urls), max_workers)):
                drivers.append(
                    executor.submit(_parser.get_driver)
                )

        wait(drivers, return_when=ALL_COMPLETED)

        futures = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for index in range(min(_parser.urls_len(urls), max_crawl_pages)):
                futures.append(
                    executor.submit(
                        parser.pars,
                        index,
                        urls,
                        drivers,
                        max_workers,
                        out_parsed_data_in_levels,
                        model
                    )
                )

        wait(futures, return_when=ALL_COMPLETED)
        for driver in drivers:
            driver.result().close()
