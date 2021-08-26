# web page parser
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from abc import ABC


class DevzillasWebPageParser(ABC):

    @staticmethod
    def get_driver():
        options = Options()
        options.headless = True
        prefs = {
            'cookies': 2, 'images': 2, 'javascript': 2,
            'plugins': 2, 'popups': 2, 'geolocation': 2,
            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
            'durable_storage': 2}
        options.add_experimental_option("prefs", prefs)
        #
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        # driver.implicitly_wait(20)

        return driver

    @staticmethod
    def urls_len(urls):
        return len(urls)

    @staticmethod
    def get_url(urls, index):
        return urls[index]

    @staticmethod
    def get_parameters(urls, index):
        return urls[index]

    @staticmethod
    def pars(driver, url, out_parsed_data_in_levels, parameters):
        raise Exception('parse method is undefined.')

    @staticmethod
    def get_value_by_xpath_attribute(driver, attribute, xpath, try_condition, try_count, wait):
        counter = 0
        while counter < try_count:
            driver.implicitly_wait(wait)
            try:
                elem = driver.find_element_by_xpath(xpath)
                result = elem.get_attribute(attribute)
            except Exception as err:
                counter += 1
                print(f"method : {__name__} has error {str(counter)} times. error is {err}")
                continue

            if result not in try_condition:
                return result
            counter += 1

    @staticmethod
    def send_keys_by_xpath(driver, xpath, data, try_count, wait):
        counter = 0
        while counter < try_count:
            driver.implicitly_wait(wait)
            # sleep(wait)
            try:
                element = driver.find_element_by_xpath(xpath)
                element.send_keys(data)
                return
            except Exception as err:
                counter += 1
                print(f"method : {__name__} has error {str(counter)} times. error is {err}")
                continue

    @staticmethod
    def click_by_xpath(driver, xpath, try_count, wait):
        counter = 0
        while counter < try_count:
            driver.implicitly_wait(wait)
            # sleep(wait)
            try:
                element = driver.find_element_by_xpath(xpath)
                element.click()
                return
            except Exception as err:
                counter += 1
                print(f"method : {__name__} has error {str(counter)} times. error is {err}")
                continue

    @staticmethod
    def save_data(data):
        file1 = open("data.txt", "a+")
        file1.write(str({data: data}))
        file1.close()

    @staticmethod
    def close_driver(driver):
        driver.close()
