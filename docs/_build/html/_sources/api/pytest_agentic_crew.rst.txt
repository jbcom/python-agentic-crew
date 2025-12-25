pytest-agentic-crew API Reference
=================================

Overview
--------

pytest-agentic-crew provides pytest fixtures and VCR integration for testing
agentic-crew applications with real or recorded LLM API calls.

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install pytest-agentic-crew[all]

Core Module
-----------

.. automodule:: pytest_agentic_crew
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

.. automodule:: pytest_agentic_crew.models
   :members:
   :undoc-members:
   :show-inheritance:

VCR Integration
---------------

.. automodule:: pytest_agentic_crew.vcr
   :members:
   :undoc-members:
   :show-inheritance:

Plugin Fixtures
---------------

.. automodule:: pytest_agentic_crew.plugin
   :members:
   :undoc-members:
   :show-inheritance:

Available Fixtures
~~~~~~~~~~~~~~~~~~

The following fixtures are automatically available when pytest-agentic-crew is installed:

**API Key Checks**

- ``check_api_key`` - Skips test if ``ANTHROPIC_API_KEY`` not set
- ``check_aws_credentials`` - Skips test if AWS credentials not configured

**Crew Configurations**

- ``simple_agent_config`` - Basic agent configuration dict
- ``simple_task_config`` - Basic task configuration dict
- ``simple_crew_config`` - Single agent/task crew configuration
- ``multi_agent_crew_config`` - Multi-agent crew with researcher/writer
- ``crew_with_knowledge`` - Crew with knowledge sources

**VCR Cassettes**

- ``vcr`` - VCR instance for recording HTTP interactions
- ``vcr_cassette`` - Context manager for cassette recording/playback
- ``vcr_config`` - Override to customize VCR settings
- ``vcr_cassette_dir`` - Directory for cassette files
- ``vcr_cassette_name`` - Name of the cassette file

**Utilities**

- ``temp_crew_dir`` - Temporary ``.crewai`` directory

Command Line Options
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   --e2e                 Enable E2E tests (disabled by default)
   --framework=NAME      Filter tests by framework (crewai, langgraph, strands)
   --vcr-record=MODE     VCR recording mode (once, new_episodes, none, all)
   --disable-vcr         Disable VCR cassette recording/playback
