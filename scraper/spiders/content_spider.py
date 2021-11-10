from scrapy import Request, Spider
from scrapy_splash import SplashRequest
import re
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup


class ContentSpider(Spider):

	name = "content"

	start_urls = []

	json_file = "data.json"

	def __init__(self):
		with open(self.json_file) as file:
			data = json.loads(file.read())
			for d in data[:1]:
				self.start_urls.append(d["url"])

	def start_requests(self):
		for url in self.start_urls:
			yield self.__req(url)

	def parse_content(self, response):
		yield {
			"url": response.url,
			"title": response.css("title::text").get(),
			"description": self.__parse_meta_description(response),
			"content_text": self.__parse_content(response),
			"images": self.__parse_images(response),
			"links": self.__get_page_links(response),
			"tags": self.__parse_meta_tags(response)
		}

	def __req(self, url: str):
		return SplashRequest(
			url=url, 
			callback=self.parse_content,
			args={
				"wait": 2
			}
		)

	def __get_page_links(self, response):
		base_url = self.__extract_host_from_url(response.url)
		links = []
		for link in response.css("a::attr(href)").getall():
			if link == "/" or link == "":
				continue
			links.append(self.__parse_link(base_url, link))
		return links

	def __extract_host_from_url(self, url: str) -> str:
		parsed_uri = urlparse(url)
		return "{uri.scheme}://{uri.netloc}".format(uri=parsed_uri)

	def __parse_content(self, response) -> list:
		soup = BeautifulSoup(response.body, "lxml")
		tags = soup.findAll(["h1", "h2", "h3", "h4", "p"])

		results = []
		for tag in tags:
			result = {}
			result[tag.name] = tag.text.strip()
			results.append(result)
			
		return results

	def __parse_link(self, base_link, link: str) -> str:
		base_url = self.__extract_host_from_url(base_link)
		if "http" not in link:
			if link[0] == "/":
				link = base_url + link
			else:
				link = f"{base_url}/{link}"

		return link

	def __parse_images(self, response) -> list:
		base_url = self.__extract_host_from_url(response.url)
		soup = BeautifulSoup(response.body, "lxml")

		results = []
		for pic in soup.findAll("img"):
			link = pic.attrs.get("src", None)
			if link is None:
				continue
			results.append(self.__parse_link(base_url, link))

		return results

	def __parse_meta_description(self, response) -> str:
		desc = response.xpath("//meta[@name='description']/@content").get()
		if desc == "":
			desc = response.xpath("//meta[@name='og:description']/@content").get()
		
		return desc

	def __parse_meta_tags(self, response) -> list:
		tags = response.xpath("//meta[@property='article:tag']/@content").getall()
		if len(tags) == 0:
			tags = response.xpath("//meta[@name='keywords']/@content").get()
			if tags is not None:
				tags = tags.split(",").strip()
			else:
				tags = []

		return tags
