# IDA project Makefile
.DEFAULT_GOAL := help

export PROJECT := ida
export ROOT := $(CURDIR)
export CONFIG := $(ROOT)/config
export DOCS := $(ROOT)/docs
export TF := $(ROOT)/tf
export UI := $(ROOT)/ui

export ENVIRONMENT := staging

export PY := $(shell cat "$(ROOT)/.python-version")
export VENV := $(ROOT)/.venv
export VENV_BIN := $(abspath ${VENV})/bin

-include Makefiles/Makefile.db
-include Makefiles/Makefile.deploy
-include Makefiles/Makefile.docs
-include Makefiles/Makefile.infra
-include Makefiles/Makefile.ui
-include Makefiles/Makefile.web

confirm:
	@echo "DESTRUCTIVE OPERATION - Are you sure? [y/N] " && \
		read ans && [ $${ans:-N} = y ]
.PHONY: confirm

dev: infra.start infra.log
.PHONY: dev

init: infra.oidc.key infra.env web.init ui.init infra.hooks.install infra.build
.PHONY: init

sync: web.sync ui.sync docs.sync infra.hooks.update
.PHONY: sync

test: web.test # ui.test
.PHONY: test

bootstrap:
ifndef dump
	$(error No local dump specified to restore. \
		Usage: make bootstrap dump='dalme-20231025-T1698276955.dump')
else
	make db.migrate
	make web.manage args='ensure_tenants'
	make db.load dump='$(dump)'
	make web.migrate_data
	make web.manage args='ensure_oauth'
	make web.manage args='tenant_command update_index --schema=dalme'
	make web.collectstatic
endif
.PHONY: bootstrap

help:
	@echo "usage: make [option]"
	@echo "Makefile for running development tasks. Requires gmake."
	@echo ""
	@echo "  dev                    run the developer environment"
	@echo "  help                   show this message"
	@echo "  init                   bootstrap the developer environment"
	@echo "  sync                   update and rebuild the developer environment"
	@echo "  test                   run the entire automated test suite"
	@echo ""
	@$(MAKE) db.help
	@$(MAKE) deploy.help
	@$(MAKE) docs.help
	@$(MAKE) infra.help
	@$(MAKE) ui.help
	@$(MAKE) web.help
.PHONY: help
