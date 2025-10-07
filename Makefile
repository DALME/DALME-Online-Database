# DALME project Makefile
.DEFAULT_GOAL := help

export ROOT := $(CURDIR)
export CONFIG := $(ROOT)/config

export NAMESPACE := dalme

help:
	@echo "usage: make [option]"
	@echo "Makefile for running development tasks. Requires gmake."
	@echo ""
	@echo "  notebook             start Jupyter notebook instance"
	@echo ""
.PHONY: help

notebook:
	docker compose exec \
		$(NAMESPACE).eb \
		python manage.py shell_plus --notebook
.PHONY: notebook

