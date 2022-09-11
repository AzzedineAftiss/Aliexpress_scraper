import scrapy
from docx import Document
from htmldocx import HtmlToDocx
import uuid
from AliExpress.items import   AliexpressItem
from scrapy.loader import ItemLoader
from scrapy.http import Request
class AliExpressScraper(scrapy.Spider):

    name = "aliexpress_scraper"
    start_urls = ["https://www.aliexpress.com/af/category/200010058.html?categoryBrowse=y&origin=n&CatId=200010058&spm=a2g0o.home.108.18.650c2145CobYJm&catName=backpacks"]


    def  parse(self, response, **kwargs):

        next_urls = response.request.meta.get("next_urls")
        print("urls length : ", len(next_urls))
        # print(response.body)
        links = response.xpath('//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[2]/a/@href').getall()

        # for link in links:
            # product_title_text //div/div[2]/div/div[2]/div[1]/h1
            #
            # yield response.follow(link, callback=self.parse_products, meta={"request_flag": "page_product"})

        for next_url in next_urls:
            # print("azzedine : open")
            # print("next_url : ", next_url)
            # print("next_url : ", next_url)
            yield response.follow(url=next_url, callback=self.parse_page_products, meta={"request_flag": "page_product"})





        #
        # print("links : ", links)
        # for link in links:
        #     yield  {
        #         'link' : link,
        #         'len1' : response.meta.get("len_links1"),
        #         'len2': response.meta.get("len_links2")
    #     }

    def parse_products(self, response):
        ali_express_item = ItemLoader(AliexpressItem(), response)

        # ali_express_item.default_output_processor = scrapy.loader.processors.TakeFirst()
        # product_title = response.xpath("//div/div[2]/div/div[2]/div[1]/h1/text()").get()
        ali_express_item.add_xpath("product_title", "//div/div[2]/div/div[2]/div[1]/h1/text()")
        if not ali_express_item.get_output_value('product_title'):
            ali_express_item.add_value("product_title", "N/A")
        product_price = response.xpath('//div/div[2]/div/div[2]/div[3]/div[2]/div[1]/span[@class="uniform-banner-box-price"]/text()').get()
        ali_express_item.add_xpath("product_price", "//div/div[2]/div/div[2]/div[3]/div[2]/div[1]/span[@class='uniform-banner-box-price']/text()")

        if not ali_express_item.get_output_value('product_price'):
            # product_price = response.xpath('//div/div[2]/div/div[2]/div[3]/div[1]/span[@class="product-price-value"]/text()').get()
            ali_express_item.add_xpath("product_price", "//*[@id='root']/div/div[2]/div/div[2]/div/div[1]/span[@class='product-price-value']/text()")
        if not ali_express_item.get_output_value('product_price'):
            ali_express_item.add_value("product_price", "N/A")
        # product_orders_nbr = response.xpath('//div/div[2]/div[3]/div[2]/div[1]/span[@class="uniform-banner-box-price"]/text()').get()
        ali_express_item.add_xpath("product_orders_nbr", "//div/div[2]/div[3]/div[2]/div[1]/span[@class='uniform-banner-box-price']/text()") # .get(default='not-found')

        if not ali_express_item.get_output_value('product_orders_nbr'):
            ali_express_item.add_value("product_orders_nbr", "N/A")

        # product_Reviews_nbr = response.xpath('//div/div[2]/div/div[2]/div[2]/span[@class="product-reviewer-reviews black-link"]/text()').get()
        ali_express_item.add_xpath("product_Reviews_nbr", "//div/div[2]/div/div[2]/div[2]/span[@class='product-reviewer-reviews black-link']/text()") #.get(default='not-found')

        if not ali_express_item.get_output_value('product_Reviews_nbr'):
            ali_express_item.add_value("product_Reviews_nbr", "N/A")
        # product_description_html = response.xpath('//*[@id="product-description"]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[3]').get()



        # document = Document()
        # new_parser = HtmlToDocx()
        # # do stuff to document
        #
        # html = '<h1>Hello world</h1>'
        # new_parser.add_html_to_document(product_description_html, document)
        #
        # # do more stuff to document
        # document.save(uuid.uuid1())

        yield ali_express_item.load_item()
        # yield {
        #     'product_title' : product_title,
        #     'product_price' : product_price,
        #     'product_orders_number' : product_orders_nbr,
        #     'product_Reviews_number' : product_Reviews_nbr
        #     # "product_description": product_description
        # }

    def parse_page_products(self, response):
        links = response.xpath('//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[2]/a/@href').getall()
        link = links[0]
        for link in links:
            # product_title_text //div/div[2]/div/div[2]/div[1]/h1

            yield response.follow(link, callback=self.parse_products, meta={"request_flag": "page_product"})

        yield response.follow(link, callback=self.parse_products, meta={"request_flag": "page_product"})