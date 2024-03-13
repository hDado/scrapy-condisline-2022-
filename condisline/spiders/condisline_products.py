import scrapy
from scrapy import Request , Spider
from scrapy.shell import inspect_response



class CondislineProductsSpider(Spider):
    name = 'condisline_products'
    base_url = 'https://www.condisline.com'

    def start_requests(self):
        yield Request(url= self.base_url , callback=self.parse_category)


    def parse_category(self, response):
        '''This Method is parsing category links
        :params: response
        return: category
        '''
        main_cat = response.xpath("//span[@class='menu_link']")
        for cat in main_cat:
            categories =[]
            cat_name = cat.xpath('.//a/text()').get()
            categories.append(cat_name)

        for sub in response.xpath("//div[@class='submenu']//li/a"):
            sub_cat_link = self.base_url + sub.xpath(".//@href").get()
            sub_cat_name = sub.xpath(".//text()").get()
            yield Request(url=sub_cat_link, callback=self.parse_sub_category) #meta={'Category': cat_name})


    def parse_sub_category(self, response):
        sub_link_add = response.xpath("//div[h2[text()='VARIEDAD']]/following-sibling::label/input/@id")
        for link in sub_link_add:
            sub_link_final = response.url + "?varId=" + sub_link_add.get()
            for f_link in sub_link_final:
                yield Request(url=sub_link_final, callback= self.parse_products,meta={'var_id': sub_link_add})


    def parse_products(self, response):
        
        #cat_name = response.request.meta['Category']
        p_list = response.xpath("//ul[@id='carousel_articles']/li/article")
        var_id = response.request.meta['var_id']
        for product in p_list:
            yield {
                #'Category': cat_name,
                'product_url' : product.xpath("./a[@class='article_name']/@href").get(),
                'title' : product.xpath("./a/span/text()").get(),
                'calories' : product.xpath("./div[@class='info_container']/span/text()").get() ,
                # # 'price' : product.xpath("./div[@class='article_price_container']/span[@class='article_price']/span/text()").get().strip().split('(')[-1].split(',')[0],
                'price/unit' :  product.xpath("./div[@class='article_price_container']/div[@class='article_pum']/span/text()").get(),
                'product_image': product.xpath("//img[@class='article_image']/@src").get()
                
            }

        if p_list:
              next_page = self.base_url + f"/productlistpaginator?varId={var_id}&page={i}"
              yield Request(url=sub_link_final, callback= self.parse_products)

