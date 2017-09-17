.DEFAULT_GOAL := template

check:
	flake8
	isort --check-only --diff

template:
	mkdir -p content/
	python dokku_stack.py > content/dokku_stack.json

upload:
	aws s3 sync content/ s3://dokku-aws/ --acl public-read
