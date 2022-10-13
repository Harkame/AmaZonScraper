# AmazonScraper

## Installation

``` bash

pip install azc

```

OR

clone this repository and

``` bash

pip install -r requirements.txt

python setup.py install

```

## Usage

### Initialization

``` python

from azc import AmazonScraper

scraper = AmazonScraper()

```

### Get a product

Use the product code

``` python

product = scraper.get_product("B08VH8C3WZ")
print(str(product))

"""

Title : Western Digital WD Red Plus 3.5" 4000 Go Série ATA III
Price : 119.13 €
Evaluation : 4.6
Evaluation count : 1
Saving percentage : 10

"""
```