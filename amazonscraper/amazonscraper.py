import requests
from bs4 import BeautifulSoup
import logging
import os
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from win10toast import ToastNotifier
import webbrowser

DEFAULT_CONFIG_FILE = os.path.join(".", "config.yml")
AMAZON_TLD = "fr"

AMAZON_BASE_PRODUCT_URL = f"https://www.amazon.{AMAZON_TLD}/dp/"
logger = logging.getLogger(__name__)

DEFAULT_PORT = 587
DEFAULT_SMTP_SERVER = "smtp.gmail.com"

DEFAULT_SLEEP = 3600
DEFAULT_ITERATION_SLEEP = 10

DEFAULT_CREDENTIAL = "credential.json"

"""
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Transfer-Encoding": "chunked",
    "Connection": "keep-alive",
    "Server": "Server",
    "Date": "Tue, 23 Jun 2020 11:55:44 GMT",
    "Accept-CH": "ect,rtt,downlink",
    "Accept-CH-Lifetime": "86400",
    "Cache-Control": "no-cache, no-transform",
}
"""
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


class AmazonScraper:
    def __init__(self):
        self.session = requests.session()

    def get_product(self, product_code):
        url = f"{AMAZON_BASE_PRODUCT_URL}{product_code}"

        logger.debug("url : %s", url)

        page = BeautifulSoup(self.session.get(url, headers=headers).content, "lxml")

        product = Product()
        product.url = url

        product_title_tag = page.find(id="titleSection")

        if product_title_tag is None:
            logger.debug("spam detected")
            time.sleep(15)  # spam detected
            return

        image = page.find("img", {"id": "landingImage"})["src"]

        product.title = product_title_tag.text.strip()

        price_tag = page.find(id="priceblock_ourprice")

        if price_tag is None:
            price_tag = page.find(id="priceblock_dealprice")

        if price_tag is None:
            unqualified_buy_box_tag = page.find(id="unqualifiedBuyBox")

            if unqualified_buy_box_tag is not None:
                price_tag = unqualified_buy_box_tag.find(
                    "span", {"class": "a-color-price"}
                )

        if price_tag is None:
            price_tag = page.select(".swatchElement span span span span span")[0]

        if price_tag is not None:
            price = price_tag.text.strip()
            print(price)
            product.price = price_tag.text.strip()

        return product


class Product:
    def __init__(self):
        self.title = None
        self.code = None
        self.url = None
        self.price = 0.0

    def __str__(self):
        to_string = ""
        to_string += "Title :"
        to_string += self.title
        to_string += os.linesep
        to_string += "Price :"
        to_string += str(self.price)
        to_string += os.linesep
        return to_string


if __name__ == "__main__":
    scraper = AmazonScraper()
    product = scraper.get_product("B07YFW75X9")
    print(str(product))
