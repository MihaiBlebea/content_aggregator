import feedparser
import json
import uuid

urls = [
	"https://www.freecodecamp.org/news/rss/",
	"https://cdn.hackernoon.com/tagged/golang/feed",
	"https://waylonwalker.com/rss.xml"
]

def main():
	results = []
	for u in urls:
		results += parse_rss(u)

	with open("data.json", "w") as outfile:
		json.dump(results, outfile)

def parse_rss(url: str) -> list:
	feed = feedparser.parse(url)
	results = []
	for entry in feed["entries"]:
		results.append({
			"id": str(uuid.uuid4()),
			"title": entry["title"],
			"url": entry["link"],
			"summary": entry["summary"],
			"published": entry["published"]
		})

	return results

if __name__ == "__main__":
	main()