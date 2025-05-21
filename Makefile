# IDA project Makefile
.DEFAULT_GOAL := help

export ROOT := $(CURDIR)
export CONFIG := $(ROOT)/config
export DOCS := $(ROOT)/docs
export TF := $(ROOT)/tf
export UI := $(ROOT)/ui

export NAMESPACE := ida
export ENVIRONMENT := staging

export PY := $(shell cat "$(ROOT)/.python-version")
export VENV := $(ROOT)/.venv
export VENV_BIN := $(abspath ${VENV})/bin

-include Makefiles/Makefile.app
-include Makefiles/Makefile.db
-include Makefiles/Makefile.deploy
-include Makefiles/Makefile.docs
-include Makefiles/Makefile.infra
-include Makefiles/Makefile.ui

help:
	@echo "usage: make [option]"
	@echo "Makefile for running development tasks. Requires gmake."
	@echo ""
	@echo "  dev                      run the developer environment"
	@echo "  help                     show this message"
	@echo "  init                     bootstrap the developer environment"
	@echo "  sync                     update and rebuild the developer environment"
	@echo "  test                     run the entire automated test suite"
	@echo ""
	@$(MAKE) app.help
	@$(MAKE) db.help
	@$(MAKE) deploy.help
	@$(MAKE) docs.help
	@$(MAKE) infra.help
	@$(MAKE) ui.help
.PHONY: help

dev: infra.start infra.log
.PHONY: dev

init: _infra.oidc.key _infra.env _app.init _ui.init _infra.hooks.install _infra.build
.PHONY: init

sync: app.sync ui.sync docs.sync infra.hooks.update
.PHONY: sync

test: app.test ui.test
.PHONY: test

### Private (non-interface) targets.
_confirm:
	@echo "DESTRUCTIVE OPERATION - Are you sure? [y/N] " && \
		read ans && [ $${ans:-N} = y ]
.PHONY: _confirm
