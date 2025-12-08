"""Sphinx configuration for agentic-crew documentation."""

import os
import sys

# Add package sources to path for autodoc
sys.path.insert(0, os.path.abspath("../packages/agentic-crew/src"))
sys.path.insert(0, os.path.abspath("../packages/pytest-agentic-crew/src"))

# Project information
project = "agentic-crew"
copyright = "2025, Jon Bogaty"
author = "Jon Bogaty"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

# MyST parser settings (for Markdown support)
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
    "show-inheritance": True,
}
autosummary_generate = True

# Napoleon settings (Google style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pytest": ("https://docs.pytest.org/en/stable/", None),
}

# HTML output settings
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_title = "agentic-crew"

# Source settings
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
master_doc = "index"

# Exclude patterns
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
