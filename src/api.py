from flask import Flask, jsonify, request
import os
import json

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

	with open("data.json") as file:
		data = json.loads(file.read())

		response = paginate(data, per_page, page)
		return jsonify(response)


@app.route("/article/<article_id>")
def league(article_id: str):
	pass
	# result = []
	# if league in leagues and season in seasons:
	# 	with open(f"./data/league_{leagues[league]}_{season}.json", "r") as outfile:
	# 		# json.dump(data, outfile)
	# 		data = json.loads(outfile.read())

			# result = data
		# for d in data:
		# 	result.append({
		# 		"id": r[0],
		# 		"title": r[1],
		# 		"url": r[2],
		# 		"unique_id": r[3],
		# 		"salary_low": r[4],
		# 		"salary_high": r[5],
		# 		"created": r[6]
		# 	})

	return jsonify(result)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("HTTP_PORT", 5000)))