"""
visualization.py — Interactive browser dashboard for the SIR Epidemic Model.

Run with:
    python visualization.py

Then open http://127.0.0.1:8521/ in your browser.

Color scheme:
    Blue  → Susceptible
    Red   → Infected
    Green → Recovered
"""

import mesa
from mesa.visualization import SolaraViz, make_space_component, make_plot_component

from model import EpidemicModel


# ---------------------------------------------------------------------------
# Agent portrayal
# ---------------------------------------------------------------------------

STATE_COLORS = {
    "S": "#1f77b4",   # blue
    "I": "#d62728",   # red
    "R": "#2ca02c",   # green
}


def agent_portrayal(agent):
    """Map agent state to visual properties."""
    return {
        "color": STATE_COLORS.get(agent.state, "grey"),
        "size":  10,
    }


# ---------------------------------------------------------------------------
# UI components
# ---------------------------------------------------------------------------

SpaceView = make_space_component(agent_portrayal)

SIRChart = make_plot_component(
    {
        "Susceptible": "#1f77b4",
        "Infected":    "#d62728",
        "Recovered":   "#2ca02c",
    }
)

# ---------------------------------------------------------------------------
# Model parameters sliders (shown in the UI)
# ---------------------------------------------------------------------------

model_params = {
    "n_agents": {
        "type": "SliderInt",
        "label": "Number of Agents",
        "value": 150,
        "min": 20,
        "max": 500,
        "step": 10,
    },
    "width": {
        "type": "SliderInt",
        "label": "Grid Width",
        "value": 20,
        "min": 10,
        "max": 50,
        "step": 5,
    },
    "height": {
        "type": "SliderInt",
        "label": "Grid Height",
        "value": 20,
        "min": 10,
        "max": 50,
        "step": 5,
    },
    "initial_infected": {
        "type": "SliderInt",
        "label": "Initially Infected",
        "value": 3,
        "min": 1,
        "max": 20,
        "step": 1,
    },
    "infection_prob": {
        "type": "SliderFloat",
        "label": "Infection Probability",
        "value": 0.3,
        "min": 0.0,
        "max": 1.0,
        "step": 0.05,
    },
    "recovery_days": {
        "type": "SliderInt",
        "label": "Mean Recovery Days",
        "value": 14,
        "min": 1,
        "max": 60,
        "step": 1,
    },
}

# ---------------------------------------------------------------------------
# Launch
# ---------------------------------------------------------------------------

page = SolaraViz(
    EpidemicModel,
    components=[SpaceView, SIRChart],
    model_params=model_params,
    name="SIR Epidemic Model",
)

# `page` is the Solara app — Mesa's server picks it up automatically.
# Run: `solara run visualization.py`  OR  `python visualization.py`

if __name__ == "__main__":
    import solara
    solara.run(page)
