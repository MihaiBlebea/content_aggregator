venv-create:
	python3 -m venv virtualenv

venv-activate:
	source ./virtualenv/bin/activate

venv-lock:
	./virtualenv/bin/pip3 freeze > requirements.txt

venv-install-all:
	./virtualenv/bin/pip3 install -r requirements.txt

venv-install:
	./virtualenv/bin/pip3 install $(package)

ansible-deploy:
	ansible-playbook -i $$HOME/.ansible/inventory ./ansible/deploy.yaml

ansible-remove:
	ansible-playbook -i $$HOME/.ansible/inventory ./ansible/remove.yaml

git:
	git add . && git commit -m "$(msg)" && git push origin master

git-deploy: git ansible-deploy

splash:
	docker run -d -p 8050:8050 --name spash --rm scrapinghub/splash

splash-stop:
	docker stop splash && docker rm splash

docker-api-build:
	docker build -t api:v1.0 .

docker-api-run:
	docker run -v ${PWD}/store:/app/store -d -p 5000:5000 --name api api:v1.0

docker-api: docker-api-build docker-api-run

docker-api-stop:
	docker stop api && docker rm api

scrape:
	./virtualenv/bin/scrapy crawl content -O output.json

shell:
	./virtualenv/bin/scrapy shell

api:
	./virtualenv/bin/python3 ./src/api.py
