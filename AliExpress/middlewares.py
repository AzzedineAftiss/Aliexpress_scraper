# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class AliexpressSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AliexpressDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        # options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-gpu")
        # desired_capabilities = options.to_capabilities()
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=desired_capabilities ) # , desired_capabilities=desired_capabilities,

        # For Heroku deployement :
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)




    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def get_all_page_urls(self, page_url, next_btn):
        all_urls = [page_url]
        prop = next_btn.get_property('disabled')
        #
        next_btn.click()
        scroll_step = 100

        # while True : # for i in range(5):

        while True:  # i < 40:

            time.sleep(0.5)

            try:
                next_ = self.driver.find_element(By.XPATH, "//div/div/div[2]/div[2]/div/div[3]/div/div[1]/div/button[2]")
                if next_ is not None:

                    break
            except:
                self.driver.execute_script(f'''window.scrollTo(0,{scroll_step})''')

            scroll_step = scroll_step + 100

        while True:  # i < 40:

            time.sleep(0.5)

            try:
                next_ = self.driver.find_element(By.XPATH, "//div/div/div[2]/div[2]/div/div[3]/div/div[1]/div/button[2]")
                prop = next_.get_property('disabled')
                if prop:
                    break
                next_.click()

                next_url = self.driver.current_url

                all_urls.append(next_url)
            except:
               print("next button doesn't exist!!!")





        # prop = next_.get_property('disabled')

            # if not prop:
            #     break



            next_button_flag = "open"

        return all_urls

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        url_flag = request.meta.get("request_flag")
        if url_flag == "page_product":
            self.driver.get(request.url)
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            scroll_step = 200
            i = 0
            while True:  # i < 40:
                # time.sleep(0.5)
                try:
                    recommended_seller = self.driver.find_element(By.XPATH, "//*[@id='product-detail']/div[3]/div[1]/div/span")
                    app_store = self.driver.find_element(By.XPATH, "//div[4]/a[1]")
                    print(f"app_store : {app_store}")
                    print(f"recommended_seller : {recommended_seller}")
                    if recommended_seller is not None or app_store is not None:
                        break
                except:
                    self.driver.execute_script(f'''window.scrollTo(0,{scroll_step})''')

                # last_height = new_height
                scroll_step = scroll_step + 200

                i = i + 1
                if i == 200:
                    break
            # element_clk = self.driver.find_element(By.XPATH, '//*[@id="product-detail"]/div[2]/div/div[1]/ul/li[1]')
            # element_clk.click()
            time.sleep(2)
            body = str.encode(self.driver.page_source)
            return HtmlResponse(
                self.driver.current_url,
                body=body,
                encoding='utf-8',
                request=request,
            )



        else:
            self.driver.get(request.url)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, '_3t7zg'))
            )

            # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(10)
            WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[1]/div/div[2]/div[2]/div/div[2]/a")))

            # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            # while True:
            #     try :
            #         next = self.driver.find_element("xpath", '//*[@id="root"]/div[1]/div/div[2]/div[2]/div/div[3]/div/div[1]/div/button[2]')
            #         if next is not None:
            #             break
            #     except:
            #         self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            # print("Next founded !!")
            # Get scroll height
            # last_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_step = 100
            # self.driver.execute_script("var scroll_step = 500")
            # i = 0
            while True: # i < 40:

                time.sleep(0.5)

                try:
                    next_ = self.driver.find_element(By.XPATH, "//div[1]/div/div[2]/div[2]/div/div[3]/div/div[1]/div/button[2]")
                    if next_ is not None:
                        break
                except:
                    self.driver.execute_script(f'''window.scrollTo(0,{scroll_step})''')

                scroll_step = scroll_step + 100


            time.sleep(2)
            body = str.encode(self.driver.page_source)
            links1 = self.driver.find_elements("xpath", '//div[1]/div/div[2]/div[2]/div/div[2]/a[@href]')
            links2 = self.driver.execute_script('return document.querySelectorAll("div.main-content > div.right-menu > div > div.JIIxO > a")')
            # print("len links azzedine : ", len(links))
            # Expose the driver via the "meta" attribute
            # request.meta.update({'driver': self.driver, "bodies": bodies})
            request.meta.update({'len_links1': len(links1), 'len_links2' : len(links2)})

            # next_button = response.xpath("")
            next_button = self.driver.find_element(By.XPATH, "//*[@id='root']/div[1]/div/div[2]/div[2]/div/div[3]/div/div[1]/div/button[2]")

            next_url = self.driver.current_url

            next_page_urls = self.get_all_page_urls( next_url, next_)

            # while next_url!="none": # i < 40:
            #
            #     time.sleep(0.5)
            #
            #     try:
            #         next_button = self.driver.find_element(By.XPATH, "//div[1]/div/div[2]/div[2]/div/div[3]/div/div[1]/div/button[2]")
            #
            #         if next_url is not None:
            #             prop = next_url.get_property('disabled')
            #             if not prop:
            #                 next_url = self.driver.current_url
            #                 next_page_urls.append(next_url)
            #                 next_button_flag = "open"
            #
            #                 next_button.click()
            #             else:
            #                 break
            #         else:
            #             break
            #     except:
            #         self.driver.execute_script(f'''window.scrollTo(0,{scroll_step})''')
            #
            #
            #
            #
            #
            #     scroll_step = scroll_step + 100
            #






            request.meta.update({ "next_urls" : next_page_urls})

            # if next_button is not None and next_button.is_enabled():
            #     yield HtmlResponse(
            #     self.driver.current_url,
            #     body=body,
            #     encoding='utf-8',
            #     request=request,
            # )
            # else:
            return HtmlResponse(
                    self.driver.current_url,
                    body=body,
                    encoding='utf-8',
                    request=request,
                )
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
