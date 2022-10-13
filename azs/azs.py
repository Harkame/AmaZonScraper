import requests
from bs4 import BeautifulSoup
import logging
import os
import time
from fake_useragent import UserAgent
import re

DEFAULT_CONFIG_FILE = os.path.join(".", "config.yml")
AMAZON_TLD = "fr"

AMAZON_BASE_PRODUCT_URL = f"https://www.amazon.{AMAZON_TLD}/dp/"
logger = logging.getLogger(__name__)

DEFAULT_CREDENTIAL = "credential.json"


class AmazonScraper:
    def __init__(self, session=None, driver=None):
        if session is None:
            self.session = requests.session()
        else:
            self.session = session

        self.driver = driver

    def __get_product_page__(self, product_url):
        url = f"{product_url}"

        headers = {
            "User-Agent": UserAgent().random
        }

        page = BeautifulSoup(self.session.get(url, headers=headers).content, "lxml")

        return page

    def get_product(self, product_url):

        page = self.__get_product_page__(product_url)

        product = Product()
        product.url = product_url

        product_title_tag = product_url.find(id="titleSection")

        if product_title_tag is None:
            logger.debug("spam detected")
            time.sleep(15)  # spam detected
            return

        tmp_evaluation = page.find('span', {'id': 'acrPopover'}).text
        product.evaluation = float(re.findall(r'\d+,\d+', tmp_evaluation)[0].replace(',', '.'))

        tmp_evaluationss_count = page.find('span', {'id': 'acrCustomerReviewText'}).text
        product.evaluations_count = int(re.findall(r'\d+', tmp_evaluationss_count)[0])

        tmp_saving_percentage = page.find('span', {'class' : 'savingsPercentage'}).text
        product.saving_percentage = int(re.findall(r'\d+', tmp_saving_percentage)[0])


        price_block = page.find('span', {'class' : 'priceToPay'})

        product.title = product_title_tag.text.strip()

        tmp_price = price_block.find("span", {"class": "a-price-whole"}).text
        tmp_price += price_block.find("span", {"class": "a-price-fraction"}).text

        tmp_price = tmp_price.replace(',', '.')
        product.price = float(tmp_price)

        product.price_symbol = price_block.find("span", {"class": "a-price-symbol"}).text

        return product


class Product:
    def __init__(self):
        self.title = None
        self.code = None
        self.url = None
        self.price = 0.0
        self.price_symbol = None
        self.evaluation = 0.0
        self.evaluations_count = 0
        self.saving_percentage = 0.0

    def __str__(self):
        to_string = ""
        to_string += "Title : "
        to_string += self.title
        to_string += os.linesep
        to_string += "Price : "
        to_string += str(self.price) + " " + self.price_symbol
        to_string += os.linesep
        to_string += "Evaluation : "
        to_string += str(self.evaluation)
        to_string += os.linesep
        to_string += "Evaluation count : "
        to_string += str(self.evaluations_count)
        to_string += os.linesep
        to_string += "Saving percentage : "
        to_string += str(self.saving_percentage)
        to_string += os.linesep

        return to_string


if __name__ == "__main__":
    scraper = AmazonScraper()
    product = scraper.get_product('https://www.amazon.fr/gp/product/B08VH8C3WZ')
    print(str(product))
