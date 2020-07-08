# AmazonScraper

Yet another amazon scraper

## Installation

``` shell

pip install amazon_scraper

```

## Usage

### initialization

``` python

scraper = AmazonScraper()

```

### Get product

``` python

product = scraper.get_product("")

print(str(product))

```

### Search products

``` python

products = scraper.search("walking dead")

```