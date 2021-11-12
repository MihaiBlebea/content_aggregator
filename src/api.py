from flask import Flask, jsonify, request, abort
import os

from store import get_all_rss, get_article_by_id

app = Flask(__name__)

def chunks(source: list, n: int) -> list:
	"""Yield successive n-sized chunks from lst."""
	result = []
	for i in range(0, len(source), n):
		result.append(source[i:i + n])

	return result

def paginate(data, per_page, page) -> dict:
	paginated = chunks(data, per_page)
	if page > len(paginated) - 1:
		page = len(paginated) - 1

	response = {
		"data": paginated[page],
		"meta": {
			"page": page + 1,
			"per_page": per_page,
			"total": len(data),
		}
	}

	if page > 0:
		response["meta"]["prev"] = f"{request.host_url}articles?per_page={per_page}&page={page}"

	if page + 1 < len(paginated):
		response["meta"]["next"] = f"{request.host_url}articles?per_page={per_page}&page={page + 2}"

	return response


@app.route("/articles")
def index():
	per_page = 20
	page = 0
	if request.args.get("per_page") is not None:
		per_page = int(request.args.get("per_page"))

	if request.args.get("page") is not None:
		page = int(request.args.get("page")) - 1
		if page < 0:
			page = 0

	data = get_all_rss()

	for article in data:
		article["details"] = f"{request.host_url}article/{article['id']}"

	response = paginate(data, per_page, page)
	return jsonify(response)


@app.route("/article/<article_id>")
def league(article_id: str):
	data = get_article_by_id(article_id)
	if data is not None:
		return jsonify(data)

	return abort(404)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("HTTP_PORT", 5000)))