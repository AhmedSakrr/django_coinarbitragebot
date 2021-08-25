from .web_page_parser import DevzillasWebPageParser
from bs4 import BeautifulSoup
from lxml import etree
import requests
import time


class PredictScraper(DevzillasWebPageParser):
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
    def to_number(string):
        try:
            return float(str(string).replace('%', '').strip())
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def get_number(string):
        try:
            n = str(string).replace('%', '').strip()
            n = n[n.find('('):].replace(')', '').replace('(', '')
            return float(n)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def get_xpath(tree, xpath):
        try:
            return (tree.xpath(xpath)[0].text)
        except Exception as e:
            print(xpath, str(e))
            return ''

    @staticmethod
    def pars(
            index,
            urls,
            drivers,
            max_workers,
            out_parsed_data_in_levels,
            model
    ):
        try:
            url = PredictScraper.get_url(urls, index)
            # parameters = AllCoinScraper.get_parameters(urls, index)
            driver = drivers[index % max_workers].result()
            print(f'Load page {index}')
            driver.get(url)
            print(f'wait a few seconds for page {index}')
            time.sleep(3)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, features="html.parser")
            tree = etree.HTML(str(soup))

            price_change_one_hour = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[2]/div[2]/div/div[1]/span/b'
            )
            price_change_one_day = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[2]/div[2]/div/div[2]/span/b'
            )
            price_change_seven_days = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[2]/div[2]/div/div[3]/span/b'
            )
            price_change_one_month = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[2]/div[2]/div/div[4]/span/b'
            )
            price_change_one_year = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[2]/div[2]/div/div[5]/span/b'
            )
            price_change_since_ath = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[2]/div[2]/div/div[6]/span/b'
            )

            price_prediction_one_day = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[3]/div[1]/div/div[2]/div/b'
            )
            price_prediction_one_month = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[3]/div[2]/div/div[2]/div/b'
            )
            price_prediction_one_year = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[3]/div[3]/div/div[2]/div/b'
            )
            price_forecast_one = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[3]/div[4]/div/div[2]/div[2]/b'
            )
            price_forecast_two = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[3]/div[4]/div/div[2]/div[4]/b'
            )
            price_forecast_three = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[3]/div[4]/div/div[2]/div[6]/b'
            )
            price_forecast_four = PredictScraper.get_xpath(
                tree,
                '/html/body/div[3]/div/div[3]/div[4]/div/div[2]/div[8]/b'
            )

            try:

                print(f'switch tp iframe for page {index}')
                iframe = driver.find_element_by_xpath('//*[@id="tvtech"]/iframe')
                driver.switch_to.frame(iframe)
                print(f'wait a few seconds to switch for page {index}')
                time.sleep(2)

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, features="html.parser")
                tree = etree.HTML(str(soup))
            except Exception as e:
                print(url)
                print(e)

            sell = PredictScraper.get_xpath(
                tree,
                '/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[1]/span[1]'
            )
            neutral = PredictScraper.get_xpath(
                tree,
                '/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/span[1]'
            )
            buy = PredictScraper.get_xpath(
                tree,
                '/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[3]/span[1]'
            )

            predict = {
                'coin_id': urls[index]['id'],
                'batch_number': urls[index]['batch_number'],
                'price_change_one_hour': PredictScraper.to_number(price_change_one_hour),
                'price_change_one_day': PredictScraper.to_number(price_change_one_day),
                'price_change_seven_days': PredictScraper.to_number(price_change_seven_days),
                'price_change_one_month': PredictScraper.to_number(price_change_one_month),
                'price_change_one_year': PredictScraper.to_number(price_change_one_year),
                'price_change_since_ath': PredictScraper.to_number(price_change_since_ath),
                'price_prediction_one_day': PredictScraper.get_number(price_prediction_one_day),
                'price_prediction_one_month': PredictScraper.get_number(price_prediction_one_month),
                'price_prediction_one_year': PredictScraper.get_number(price_prediction_one_year),
                'price_forecast_one': PredictScraper.get_number(price_forecast_one),
                'price_forecast_two': PredictScraper.get_number(price_forecast_two),
                'price_forecast_three': PredictScraper.get_number(price_forecast_three),
                'price_forecast_four': PredictScraper.get_number(price_forecast_four),
                'sell': PredictScraper.to_number(sell),
                'neutral': PredictScraper.to_number(neutral),
                'buy': PredictScraper.to_number(buy)}

            out_parsed_data_in_levels.append(predict)
            print(f'Scraping  of page {index} finished.  ')
        except Exception as e:
            print(url)
            print(str(e))

    @staticmethod
    def pars1(index, urls, drivers, max_workers, out_parsed_data_in_levels):
        url = PredictScraper.get_url(urls, index)
        # parameters = AllCoinScraper.get_parameters(urls, index)
        driver = drivers[index % max_workers].result()

        page_source = requests.get(url)
        page_source = page_source.text

        soup = BeautifulSoup(page_source, features="html.parser")
        tree = etree.HTML(str(soup))

        price_change_one_hour = tree.xpath('/html/body/div[3]/div/div[2]/div[2]/div/div[1]/span/b')[0].text
        price_change_one_day = tree.xpath('/html/body/div[3]/div/div[2]/div[2]/div/div[2]/span/b')[0].text
        price_change_seven_days = tree.xpath('/html/body/div[3]/div/div[2]/div[2]/div/div[3]/span/b')[0].text
        price_change_one_month = tree.xpath('/html/body/div[3]/div/div[2]/div[2]/div/div[4]/span/b')[0].text
        price_change_one_year = tree.xpath('/html/body/div[3]/div/div[2]/div[2]/div/div[5]/span/b')[0].text
        price_change_since_ath_ = tree.xpath('/html/body/div[3]/div/div[2]/div[2]/div/div[6]/span/b')[0].text

        price_prediction_one_day = tree.xpath('/html/body/div[3]/div/div[3]/div[1]/div/div[2]/div/b')[0].text
        price_prediction_one_month = tree.xpath('/html/body/div[3]/div/div[3]/div[2]/div/div[2]/div/b')[0].text
        price_prediction_one_year = tree.xpath('/html/body/div[3]/div/div[3]/div[3]/div/div[2]/div/b')[0].text
        price_forecast_one = tree.xpath('/html/body/div[3]/div/div[3]/div[4]/div/div[2]/div[2]/b')[0].text
        price_forecast_two = tree.xpath('/html/body/div[3]/div/div[3]/div[4]/div/div[2]/div[4]/b')[0].text
        price_forecast_three = tree.xpath('/html/body/div[3]/div/div[3]/div[4]/div/div[2]/div[6]/b')[0].text
        price_forecast_four = tree.xpath('/html/body/div[3]/div/div[3]/div[4]/div/div[2]/div[8]/b')[0].text



        iframe = tree.xpath('//*[@id="tvtech"]/iframe')
        src = iframe['src']
        page_source = requests.get(src)
        page_source = page_source.text

        soup = BeautifulSoup(page_source, features="html.parser")
        tree = etree.HTML(str(soup))
        sell = tree.xpath('/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[1]/span[1]').text
        neutral = tree.xpath('/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[2]/span[1]').text
        buy = tree.xpath('/html/body/div[1]/div[2]/div/div/div/div/div[3]/div[3]/span[1]').text



        result = [{'price_change_one_hour': price_change_one_hour,
                   'price_change_one_day': price_change_one_day,
                   'price_change_seven_days': price_change_seven_days,
                   'price_change_one_month': price_change_one_month,
                   'price_change_one_year': price_change_one_year,
                   'price_change_since_ath_': price_change_since_ath_,
                   'price_prediction_one_day': price_prediction_one_day,
                   'price_prediction_one_month': price_prediction_one_month,
                   'price_prediction_one_year': price_prediction_one_year,
                   'price_forecast_one': price_forecast_one,
                   'price_forecast_two': price_forecast_two,
                   'price_forecast_three': price_forecast_three,
                   'price_forecast_four': price_forecast_four,
                   'sell': sell,
                   'neutral': neutral,
                   'buy': buy

                   }, ]

        out_parsed_data_in_levels.extend(result)
        print(f'Scraping  of page {index} finished.  ')

