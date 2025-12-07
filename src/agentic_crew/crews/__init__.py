"""CrewAI Crews for game development.

Each crew is a specialized team of agents that work together
on a specific domain of game development.
"""

from __future__ import annotations

from agentic_crew.crews.asset_pipeline.asset_crew import AssetPipelineCrew
from agentic_crew.crews.creature_design.creature_design_crew import CreatureDesignCrew
from agentic_crew.crews.ecs_implementation.ecs_crew import ECSImplementationCrew
from agentic_crew.crews.game_builder.game_builder_crew import GameBuilderCrew
from agentic_crew.crews.gameplay_design.gameplay_design_crew import GameplayDesignCrew
from agentic_crew.crews.qa_validation.qa_crew import QAValidationCrew
from agentic_crew.crews.rendering.rendering_crew import RenderingCrew
from agentic_crew.crews.world_design.world_design_crew import WorldDesignCrew

__all__ = [
    "AssetPipelineCrew",
    "CreatureDesignCrew",
    "ECSImplementationCrew",
    "GameBuilderCrew",
    "GameplayDesignCrew",
    "QAValidationCrew",
    "RenderingCrew",
    "WorldDesignCrew",
]
