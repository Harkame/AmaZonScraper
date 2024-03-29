# AmazonScraper

## Installation

``` bash

pip install azs

```

OR

clone this repository and

``` bash

pip install -r requirements.txt

python setup.py install

```

## Usage

### Initialization with requests

``` python

from azs import AmazonScraper

scraper = AmazonScraper()

```

### Initialization with undetected-chromedriver

``` python

from azs import AmazonScraper
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver.v2 as uc

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = uc.Chrome(options=options)

scraper = AmazonScraper(driver=driver)

```

### Initialization with Selenium

``` python

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver =webdriver.Chrome(executable_path='D:\\chromedriver.exe', options=options)

scraper = AmazonScraper(driver=driver)

```

### Get a product

``` python

product = scraper.get_product("https://www.amazon.fr/gp/product/B08VH8C3WZ")
print(str(product))

"""

Title : Western Digital WD Red Plus 3.5" 4000 Go Série ATA III
Price : 119.13 €
Evaluation : 4.6
Evaluation count : 1
Saving percentage : 10

"""
```