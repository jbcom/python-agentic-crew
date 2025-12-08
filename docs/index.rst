agentic-crew Documentation
==========================

**Framework-agnostic AI crew orchestration** - declare once, run on CrewAI, LangGraph, or Strands.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   QUICKSTART

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   ARCHITECTURE
   INTEGRATION

.. toctree::
   :maxdepth: 2
   :caption: Packages

   agentic-crew <api/agentic_crew>
   pytest-agentic-crew <api/pytest_agentic_crew>

.. toctree::
   :maxdepth: 1
   :caption: Development

   AGENTS
   CLAUDE

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Quick Example
-------------

.. code-block:: python

   from agentic_crew import run_crew

   # Auto-detect framework and run
   result = run_crew(
       package="my-package",
       crew="my_crew",
       inputs={"topic": "Python testing"}
   )

Installation
------------

.. code-block:: bash

   # Core package
   pip install agentic-crew

   # With framework support
   pip install agentic-crew[crewai]
   pip install agentic-crew[langgraph]
   pip install agentic-crew[strands]

   # Testing plugin
   pip install pytest-agentic-crew
