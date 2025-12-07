"""CrewAI Flows for Otterfall game development.

Flows orchestrate multiple crews in sequences with evaluation
and retry loops for quality control.
"""

from __future__ import annotations

from agentic_crew.flows.asset_generation_flow import AssetGenerationFlow
from agentic_crew.flows.game_design_flow import GameDesignFlow
from agentic_crew.flows.implementation_flow import ImplementationFlow

__all__ = [
    "AssetGenerationFlow",
    "GameDesignFlow",
    "ImplementationFlow",
]
