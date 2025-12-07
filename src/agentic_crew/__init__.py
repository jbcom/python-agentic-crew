"""CrewAI Agents for game development.

This package provides autonomous AI crews that design and implement
game systems, using Anthropic Claude for best code generation.

Usage:
    from agentic_crew import GameDesignFlow, ImplementationFlow, AssetGenerationFlow

    # Run the complete design phase
    design = await GameDesignFlow().kickoff_async()

    # Then run implementation
    impl = await ImplementationFlow().kickoff_async(inputs=design)

    # Or generate assets
    assets = await AssetGenerationFlow().kickoff_async(inputs=design)
"""

from __future__ import annotations

from agentic_crew.crews import (
    AssetPipelineCrew,
    CreatureDesignCrew,
    ECSImplementationCrew,
    GameplayDesignCrew,
    QAValidationCrew,
    RenderingCrew,
    WorldDesignCrew,
)
from agentic_crew.flows import (
    AssetGenerationFlow,
    GameDesignFlow,
    ImplementationFlow,
)

__version__ = "0.2.0"

__all__ = [
    # Flows (primary interface)
    "GameDesignFlow",
    "ImplementationFlow",
    "AssetGenerationFlow",
    # Crews (for direct use if needed)
    "WorldDesignCrew",
    "CreatureDesignCrew",
    "GameplayDesignCrew",
    "ECSImplementationCrew",
    "RenderingCrew",
    "AssetPipelineCrew",
    "QAValidationCrew",
]
