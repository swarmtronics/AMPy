# Configuration file for the Sphinx documentation builder.

import os.path as osp
import datetime
import sys

sys.path.insert(0, osp.abspath(osp.join('..', '..')))

import ampy

# -- Project information

project = 'AMPy'
copyright = f'{datetime.date.today().year}, Swarmtronics'
author = 'Vadim Porvatov, Mikhail Buzakov'

release = '0.1'
version = '0.1.3.2'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

html_logo = ('https://raw.githubusercontent.com/swarmtronics/ampy/master/materials/ampy_logo_image_only.png')
html_favicon = ('https://raw.githubusercontent.com/swarmtronics/ampy/master/materials/ampy_favicon.png')
html_static_path = ['_materials']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
