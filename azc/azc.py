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
    def __init__(self):
        self.session = requests.session()

    def get_product(self, product_code):
        url = f"{AMAZON_BASE_PRODUCT_URL}{product_code}"
        print(url)

        headers = {
            "User-Agent": UserAgent().random
        }

        page = BeautifulSoup(self.session.get(url, headers=headers).content, "lxml")

        product = Product()
        product.url = url

        product_title_tag = page.find(id="titleSection")

        if product_title_tag is None:
            logger.debug("spam detected")
            time.sleep(15)  # spam detected
            return

        image = page.find("img", {"id": "landingImage"})["src"]

        price_block = page.find('span', {'class' : 'priceToPay'})

        product.title = product_title_tag.text.strip()

        tmp_price = price_block.find("span", {"class": "a-price-whole"}).text
        tmp_price += price_block.find("span", {"class": "a-price-fraction"}).text

        tmp_price = tmp_price.replace(',', '.')
        print(tmp_price)

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

    def __str__(self):
        to_string = ""
        to_string += "Title : "
        to_string += self.title
        to_string += os.linesep
        to_string += "Price : "
        to_string += str(self.price) + " " + self.price_symbolg
        to_string += os.linesep
        return to_string


if __name__ == "__main__":
    scraper = AmazonScraper()
    product = scraper.get_product("B08VH8C3WZ")
    print(str(product))
