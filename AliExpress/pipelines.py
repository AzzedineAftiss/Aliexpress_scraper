# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class AliexpressPipeline:
    def process_item(self, item, spider):
        return item

class AliexpressFirebasePiepline:
    def __init__(self):
        self.cred = credentials.Certificate("AliExpress/aliexpressproducts-2c508-firebase-adminsdk-5fovb-202be87dc2.json")
        firebase_admin.initialize_app(self.cred,
                                      {'databaseURL': "https://aliexpressproducts-2c508-default-rtdb.firebaseio.com"})
        self.ref = db.reference('products/')
        self.i = 0
    def process_item(self, item, spider):
        products_ref = self.ref.child('ali_express')
        products_ref.push({
            f"products{self.i}": {
                'product_title': item["product_title"],
                'product_price': item["product_price"],
                'product_orders_nbr': item["product_orders_nbr"],
                'product_Reviews_nbr': item["product_Reviews_nbr"]
            }
        })
        self.i = self.i + 1
        return item