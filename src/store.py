from tinydb import TinyDB, Query, where

db = TinyDB("./store/store.json")

def store_rss_link(link: str):
	links = db.table("links")
	if len(links.search(where("link") == link)) > 0:
		return
	links.insert({"link": link})

def get_rss_links() -> list:
	links = db.table("links")
	return links.all()

def remove_rss_link(link: str):
	links = db.table("links")
	links.remove(where("link") == link)

def store_rss_records(records):
	rss = db.table("rss")
	unique = []
	for record in records:
		if len(rss.search(where("url") == record["url"])) == 0:
			unique.append(record)

	rss.insert_multiple(unique)

def get_all_rss() -> list:
	rss = db.table("rss")
	return rss.all()

def exist_record_by_url(url: str):
	rss = db.table("rss")
	return len(rss.search(where("url") == url)) > 0

def store_article_records(records):
	articles = db.table("articles")
	articles.insert_multiple(records)

def get_article_by_id(id: str):
	articles = db.table("articles")
	Article = Query()

	records = articles.search(Article.id == id)
	if len(records) == 0:
		return None

	return records[0]

# def main():
# 	rss = db.table("rss")
# 	all = rss.all()

# 	print(all[0])

# if __name__ == "__main__":
# 	main()
