"""Configuration file for the Sphinx documentation builder."""  # noqa: INP001

from __future__ import annotations

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'IDA'
copyright = '2023, The Initiative for Documentary Archaeology'  # noqa: A001
author = 'Initiative for Documentary Archaeology'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    # "sphinx_js",
    'sphinxcontrib.mermaid',
]

myst_enable_extensions = [
    'attrs_block',
    'colon_fence',
    'deflist',
    'smartquotes',
]

templates_path = ['_templates']
exclude_patterns = ['.DS_Store', '*.txt', '_build', 'README.md', 'Thumbs.db']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

# -- Options for sphinx-js  https://github.com/mozilla/sphinx-js -------------

# js_language = "typescript"
# js_source_path = "ui/src"
