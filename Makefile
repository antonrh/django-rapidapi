.PHONY: help docs
.DEFAULT_GOAL := help

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

lint: ## Run code linters
	isort --check rapidapi tests
	black --check rapidapi tests
	flake8 rapidapi tests
	mypy rapidapi tests
	safety check --full-report

fmt format: ## Run code formatters
	isort rapidapi tests
	black rapidapi tests

install: ## Install dependencies
	pip install -e .[dev]