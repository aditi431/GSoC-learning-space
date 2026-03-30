"""
model.py — SIR Epidemic Model built with Mesa.

The model places PersonAgents on a toroidal grid.
Each step, agents move, spread infection, and recover.

Parameters:
    n_agents       (int):   Total number of agents.
    width          (int):   Grid width.
    height         (int):   Grid height.
    initial_infected (int): Number of agents infected at start.
    infection_prob (float): Probability of infecting a co-located susceptible (0–1).
    recovery_days  (int):   Mean days until recovery (individual variance ±20%).
"""

import mesa
from mesa.datacollection import DataCollector

from agents import PersonAgent


# ---------------------------------------------------------------------------
# Helper functions for data collection
# ---------------------------------------------------------------------------

def count_state(model, state: str) -> int:
    """Return number of agents currently in *state*."""
    return sum(1 for a in model.agents if a.state == state)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class EpidemicModel(mesa.Model):
    """SIR epidemic model on a multi-grid."""

    def __init__(
        self,
        n_agents: int = 150,
        width: int = 20,
        height: int = 20,
        initial_infected: int = 3,
        infection_prob: float = 0.3,
        recovery_days: int = 14,
        seed=None,
    ):
        super().__init__(seed=seed)

        # Store parameters (also consumed by agents via self.model)
        self.n_agents = n_agents
        self.width = width
        self.height = height
        self.initial_infected = initial_infected
        self.infection_prob = infection_prob
        self.recovery_days = recovery_days

        # Multi-cell grid: multiple agents may share a cell
        self.grid = mesa.spaces.MultiGrid(width, height, torus=True)

        # ---------------------------------------------------------------
        # Create agents
        # ---------------------------------------------------------------
        for i in range(n_agents):
            state = "I" if i < initial_infected else "S"
            agent = PersonAgent(self, state=state)
            # Place on a random cell
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(agent, (x, y))

        # ---------------------------------------------------------------
        # Data collection
        # ---------------------------------------------------------------
        self.datacollector = DataCollector(
            model_reporters={
                "Susceptible": lambda m: count_state(m, "S"),
                "Infected":    lambda m: count_state(m, "I"),
                "Recovered":   lambda m: count_state(m, "R"),
            },
            agent_reporters={
                "State":            "state",
                "Infection_Timer":  "infection_timer",
            },
        )

        # Collect initial state (step 0)
        self.datacollector.collect(self)

    # ------------------------------------------------------------------
    # Running
    # ------------------------------------------------------------------

    def step(self):
        """Advance the model by one step."""
        self.agents.shuffle_do("step")   # random activation order
        self.datacollector.collect(self)

    def run(self, n_steps: int = 100):
        """Convenience method: run *n_steps* steps."""
        for _ in range(n_steps):
            if count_state(self, "I") == 0:
                break           # stop early if no infected agents remain
            self.step()
