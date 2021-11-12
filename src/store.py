from tinydb import TinyDB, Query

db = TinyDB("store.json")

def store_rss_records(records):
	rss = db.table("rss")
	rss.insert_multiple(records)

def get_all_rss() -> list:
	rss = db.table("rss")
	return rss.all()

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
