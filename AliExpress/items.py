# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from  scrapy.item import Item, Field
from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
class AliexpressItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    product_title = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    product_price = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    product_orders_nbr = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    product_Reviews_nbr = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
