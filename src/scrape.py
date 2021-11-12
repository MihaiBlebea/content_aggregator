from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals

from content_spider import ContentSpider
from store import store_article_records

results = []

def crawler_results(signal, sender, item, response, spider):
	results.append(item)

def main():
	dispatcher.connect(crawler_results, signal=signals.item_scraped)

	process = CrawlerProcess(settings={
		"SPLASH_URL": "http://127.0.0.1:8050",
		"DOWNLOADER_MIDDLEWARES": {
			"scrapy_splash.SplashCookiesMiddleware": 723,
			"scrapy_splash.SplashMiddleware": 725,
			"scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
		},
		"SPIDER_MIDDLEWARES": {
			"scrapy_splash.SplashDeduplicateArgsMiddleware": 100,
		},
		"DUPEFILTER_CLASS": "scrapy_splash.SplashAwareDupeFilter",
		"HTTPCACHE_STORAGE": "scrapy_splash.SplashAwareFSCacheStorage"
	})

	process.crawl(ContentSpider)
	process.start()

	store_article_records(results)
	# with open("output.json", "w") as outfile:
	# 	json.dump(results, outfile)

if __name__ == "__main__":
	main()