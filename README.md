# amazon_spider


Scrapes product data form specified E-commerce website and looks up similar products on Amazon.

By default scrapes 5 amazon pagination pages.

Results are save as json, similar products are sorted by price, lower first.


How to use:

`scrapy crawl hun73r -a brand='{brand_name}' -a product_type={product_type} -a screenSize={screenSize}`

All arguments aren't necessary, the brand is enough to play around with it.

There is a sample file `scrapedData74.json` to look at. Searched for Apple brand.
