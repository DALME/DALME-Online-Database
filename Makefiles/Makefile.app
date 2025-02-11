# ; -*- mode: makefile ;-*-
# vi: set ft=make :
RESOLVER := /etc/resolver/localhost

app.help:
	@echo "  app.collectstatic        bundle static files for all apps and tenants"
	@echo "  app.manage               call django management commands"
	@echo "  app.notebook             start Jupyter notebook instance"
	@echo "  app.open                 view the site in your browser"
	@echo "  app.python               shell into python on the web container"
	@echo "  app.renditions.update    regenerate Wagtail image renditions"
	@echo "  app.shell                shell into the web container"
	@echo "  app.sync                 install the web requirements and rebuild the service"
	@echo "  app.test                 run the web test suite in full"
	@echo "  app.test.i               run only the web integration tests"
	@echo "  app.test.p               run only the web property tests"
	@echo "  app.test.u               run only the web unit tests"
	@echo "  app.test.watch           re-run the test suite on code changes"
	@echo ""
.PHONY: app.help

app.collectstatic:
	docker compose exec \
		$(NAMESPACE).app \
		python manage.py collectstatic_tenants
.PHONY: app.collectstatic

app.manage:
ifndef args
	$(error Call management commands with args. \
		Usage: make app.manage command='collectstatic --no-input')
else
	docker compose exec \
		$(NAMESPACE).app \
		python manage.py $(command)
endif
.PHONY: app.manage

app.migrate_data:
	docker compose exec \
		-e DATA_MIGRATION=1 \
		$(NAMESPACE).app \
		python manage.py migrate_data
.PHONY: app.manage

app.notebook:
	docker compose exec \
		$(NAMESPACE).app \
		python manage.py shell_plus --notebook
.PHONY: app.notebook

app.open:
	open http://dalme.localhost:8000/
.PHONY: app.open

app.python:
	docker compose exec \
		$(NAMESPACE).app \
		python manage.py shell_plus --print-sql
.PHONY: app.python

app.shell:
	docker compose exec \
		$(NAMESPACE).app \
		bash
.PHONY: app.shell

app.renditions.update:
ifndef schema
	$(error No target schema specified. \
		Usage: make app.renditions.update schema='dalme')
else
	docker compose exec \
		$(NAMESPACE).app \
		python manage.py tenant_command wagtail_update_image_renditions --schema=$(schema)
endif
.PHONY: app.renditions.update

app.sync: _app.install _app.build
.PHONY: app.sync

app.test:
	docker compose run --rm \
		-e DEBUG='' \
		$(NAMESPACE).app \
		pytest -s \
		--cov=. \
		--cov-report=term-missing \
		--hypothesis-show-statistics \
		$(args)
.PHONY: app.test

app.test.i:
	docker compose run --rm \
		$(NAMESPACE).app \
		pytest -svv \
		-m 'integration' \
		--cov=. \
		--cov-report=term-missing \
		$(args)
.PHONY: app.test.i

app.test.p:
	docker compose run --rm \
		$(NAMESPACE).app \
		pytest -svv \
		-m 'property' \
		--cov=. \
		--cov-report=term-missing \
		--hypothesis-show-statistics \
		$(args)
.PHONY: app.test.p

app.test.u:
	docker compose run --rm \
		$(NAMESPACE).app \
		pytest -svv \
		-m 'unit' \
		--cov=. \
		--cov-report=term-missing \
		$(args)
.PHONY: app.test.u

app.test.watch:
	docker compose run --rm \
		$(NAMESPACE).app \
		ptw . $(args)
.PHONY: app.test.watch

### Private (non-interface) targets.
_app.build:
	 docker compose up -d --no-deps --build $(NAMESPACE).app
.PHONY: _app.build

_app.dns:
	sudo mkdir -p /etc/resolver
	[ -L $(RESOLVER) ] || sudo ln -s $(CONFIG)/localhost $(RESOLVER)
.PHONY: _app.dns

_app.init: _app.install _app.dns
.PHONY: _app.init

_app.install:
	$(VENV_BIN)/python3 -m \
		pip install -r $(ROOT)/app/requirements-dev.txt
.PHONY: _app.install
