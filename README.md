# [DALME Online Database](https://dalme.org)

[![License](https://img.shields.io/badge/License-BSD-green.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org)
[![Javascript](https://img.shields.io/badge/Language-Javascript-orange.svg)](http://www.ecma-international.org)
[![Framework](https://img.shields.io/badge/Framework-Django-blue.svg)](https://www.djangoproject.com)

A digital environment designed to facilitate the extraction, analysis, and publication of material culture information from textual primary sources.

---

![screenshot](https://dalme-app-media.s3.amazonaws.com/media/original_images/dalme_demo.gif)

## Overview

This application is the backbone of the [DALME project’s online environment](https://db.dalme.org), providing the tools to store, transcribe, and extract textual things, that is to say objects as described in textual sources, from household or estate inventories from a number of different cities and regions in Europe in a manner that makes it possible to draw legitimate comparisons between textual things on the one hand and museum objects or excavated artefacts on the other.

[DALME](https://dalme.org) is a research project directed by [Daniel Smail](https://scholar.harvard.edu/smail) and [Gabriel Pizzorno](https://scholar.harvard.edu/pizzorno), from the [Department of History](https://history.fas.harvard.edu) at [Harvard University](https://www.harvard.edu). The goal of the project is to increase our understanding of Europe’s material horizons during the later Middle Ages, an era when changing patterns of production and consumption altered the material world and transformed the relationship between people and things. We aim to accomplish this by developing a publicly accessible and fully searchable online database of material culture based on household inventories and other textual sources from the period.

## Requirements

The core functionality of the DALME Online Database requires [Python](https://www.python.org), [Django](https://www.djangoproject.com), [Django REST Framework](https://www.django-rest-framework.org) (for the API), and [Wagtail](https://wagtail.io) (for the public website). [MySQL](https://www.mysql.com) is the current database backend, deployed through [RDS](https://aws.amazon.com/rds/), although [PostgreSQL](https://www.postgresql.org) is also supported. Full-text search capabilities are implemented using [Haystack](https://haystacksearch.org) and [Elasticsearch](https://aws.amazon.com/elasticsearch-service/). Periodic and background tasks are handled using [Celery](https://docs.celeryproject.org/en/stable/index.html) and [SQS](https://aws.amazon.com/sqs/). Bibliographic resources are kept in [Zotero](https://www.zotero.org) and managed via the [Zotero API](https://www.zotero.org/support/dev/web_api/v3/start). The app is deployed with [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/), with [S3](https://aws.amazon.com/s3/) providing media storage.

## Documentation

The project's documentation is available in our [Knowledge Base](https://kb.dalme.org).
Instructions on how to set up a development environment to run the DALME Online Database can be found [here](getting_started.md).

## License

This software is licensed under a modified [BSD license](https://opensource.org/licenses/BSD-3-Clause). See the LICENSE file in the top distribution directory for the full license text.
