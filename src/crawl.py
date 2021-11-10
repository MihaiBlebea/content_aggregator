from scraper.spiders.content_spider import ContentSpider

# scrapy api
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings

def spider_closing(spider):
    """Activates on spider closed signal"""
    reactor.stop()


def main():
	# crawl responsibly
	crawler = Crawler(ContentSpider)

	# stop reactor when spider closes
	crawler.signals.connect(spider_closing, signal=signals.spider_closed)
	crawler.crawl(ContentSpider("https://waylonwalker.com/nvim-ides-are-slow"))
	crawler.stop()

if __name__ == "__main__":
	main()