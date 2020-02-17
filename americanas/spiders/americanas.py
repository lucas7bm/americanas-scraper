import scrapy, os, time, re
from scrapy.settings.default_settings import FEED_EXPORT_ENCODING

class americanas_spider(scrapy.Spider):
  name = "americanas"
  user_agent = 'test'
  start_urls = []
  query = ''
  pages = 0
  forbidden_words = []

  def __init__(self, query='', pages=0, abv=0.0):
    with open("forbidden-words.txt") as fw:
      for line in fw:
        self.forbidden_words.append(line.replace("\n", ""))

    base_url = 'https://www.americanas.com.br/busca/' + query + '?limite=24&offset='
    self.start_urls = []
    for i in range(int(pages)):
      self.start_urls.append(base_url + str(i*24))
    self.query = query
    self.pages = pages
    self.abv = float(abv)

  def parse(self, response):
    PRODUCTS_SELECTOR = '#content-middle > div:nth-child(6) > div > div > div > div.row.product-grid.no-gutters.main-grid > div'
    products = response.css(PRODUCTS_SELECTOR)

    for product in products:
      link = product.css("div > div:nth-child(2) > a").attrib['href']
      sep = '?pfm'
      link = 'https://www.americanas.com.br' + link.split(sep, 1)[0]
      
      new_request = scrapy.Request(url=link, callback=self.parse_product)
      yield new_request

  def parse_product(self, response):
    if 'produto' in response.url:
      #Seletor para verificar se a categoria é "bebidas alcoólicas"
      category_selector = '#content > div > div > div.GridUI-wcbvwm-0.idBPEj.ViewUI-sc-1ijittn-6.iXIDWU > div > section > div > div.SpacingUI-pvph4q-0.ckpIiF.ViewUI-sc-1ijittn-6.iXIDWU > div > div:nth-child(4) > a > div > span::text'
      category = response.css(category_selector).get()
      if category != "bebidas alcoólicas":
        return

      name = response.css('#product-name-default::text').get().lower()
      for forbidden_word in self.forbidden_words:
        if forbidden_word in name or 'ml' not in name:
          return
      img_src = response.css('.image-gallery-image > img')[0].attrib['src']
      
      #Seletor padrão americanas
      price_sel1 = '#content > div > div > div.GridUI-wcbvwm-0.idBPEj.ViewUI-sc-1ijittn-6.iXIDWU > div > section > div > div.GridUI-wcbvwm-0.gpGkIJ.ViewUI-sc-1ijittn-6.iXIDWU > div.ColUI-gjy0oc-0.eukbCO.ViewUI-sc-1ijittn-6.iXIDWU > div:nth-child(3) > div > section > div > div > div.buybox-b__ColMargin-wregum-1.kLeyWM.ColUI-gjy0oc-0.dUUZYI.ViewUI-sc-1ijittn-6.iXIDWU > div > div > p.main-offer__ParagraphUI-sc-1oo1w8r-0.bBzQni.ParagraphUI-b71w0e-0.YXzMm > span'
      #Seletor preço à direita
      price_sel2 = '#content > div > div > div.GridUI-wcbvwm-0.idBPEj.ViewUI-sc-1ijittn-6.iXIDWU > div > section > div > div.product-main-area-b__ProductMainAreaUI-sc-18529u5-0.eFYfmy.ViewUI-sc-1ijittn-6.iXIDWU > div.offer-box__Wrapper-sc-1hat60-0.ZybqH.ViewUI-sc-1ijittn-6.iXIDWU > div > div.buybox__BigSection-sc-4z0zqv-0.hmvxqX.ViewUI-sc-1ijittn-6.iXIDWU > div:nth-child(1) > div > div.main-offer__ContainerUI-sc-1c7pzd1-0.fjQzCD.ViewUI-sc-1ijittn-6.iXIDWU > div > div > span'
      #Seletor várias lojas
      price_sel3 = '#content > div > div > div.GridUI-wcbvwm-0.idBPEj.ViewUI-sc-1ijittn-6.iXIDWU > div > section > div > div.product-main-area-b__ProductMainAreaUI-sc-18529u5-0.eFYfmy.ViewUI-sc-1ijittn-6.iXIDWU > div.offer-box__Wrapper-sc-1hat60-0.ZybqH.ViewUI-sc-1ijittn-6.iXIDWU > div > div.buybox__BigSection-sc-4z0zqv-0.hmvxqX.ViewUI-sc-1ijittn-6.iXIDWU > div:nth-child(1) > div > div.main-offer__ContainerUI-sc-1c7pzd1-0.fjQzCD.ViewUI-sc-1ijittn-6.iXIDWU > div > div > span'
      #Seletor varias lojas 2
      price_sel4 = '#content > div > div > div.GridUI-wcbvwm-0.idBPEj.ViewUI-sc-1ijittn-6.iXIDWU > div > section > div > div.GridUI-wcbvwm-0.gpGkIJ.ViewUI-sc-1ijittn-6.iXIDWU > div.ColUI-gjy0oc-0.eukbCO.ViewUI-sc-1ijittn-6.iXIDWU > div:nth-child(3) > div > div > div.tab-panel > div > div > div.buybox-b__ColAlign-wregum-0.eTBVhk.ColUI-gjy0oc-0.fCpCWN.ViewUI-sc-1ijittn-6.iXIDWU > div.main-price > p.main-offer__ParagraphUI-sc-1oo1w8r-0.bBzQni.ParagraphUI-b71w0e-0.YXzMm > span'      
      #Seletor escolha uma cor
      price_sel5 = '#content > div > div > div.GridUI-wcbvwm-0.idBPEj.ViewUI-sc-1ijittn-6.iXIDWU > div > section > div > div.GridUI-wcbvwm-0.gpGkIJ.ViewUI-sc-1ijittn-6.iXIDWU > div.ColUI-gjy0oc-0.eukbCO.ViewUI-sc-1ijittn-6.iXIDWU > div:nth-child(4) > div > section > div > div > div.buybox-b__ColMargin-wregum-1.kLeyWM.ColUI-gjy0oc-0.dUUZYI.ViewUI-sc-1ijittn-6.iXIDWU > div > div > p.main-offer__ParagraphUI-sc-1oo1w8r-0.bBzQni.ParagraphUI-b71w0e-0.YXzMm > span'
      price = response.css(price_sel1) or response.css(price_sel2) or response.css(price_sel3) or response.css(price_sel4) or response.css(price_sel5)
      price = float(price.css('::text').get().replace('R$ ', '').replace('.', '').replace(',', '.'))
      
      if not price:
        return
      
      volume = int(re.search("\d+?[ ]ml|\d+?ml", name).group().replace("ml", ""))
      apu = volume * self.abv

      product = ProductItem()
      product['name'] = name
      product['img_src'] = img_src
      product['price'] = price
      product['url'] = response.url
      product['apu'] = apu
      yield product


class ProductItem(scrapy.Item):
  name = scrapy.Field()
  img_src = scrapy.Field()
  price = scrapy.Field()
  apu = scrapy.Field()
  url = scrapy.Field()