"""
agents.py — Defines the Person agent for the SIR Epidemic Model.

States:
    "S" — Susceptible: healthy but can be infected
    "I" — Infected: currently sick and contagious
    "R" — Recovered: immune, cannot be re-infected
"""

import mesa


class PersonAgent(mesa.Agent):
    """
    A single person in the epidemic simulation.

    Attributes:
        state (str): One of "S", "I", or "R".
        infection_timer (int): Days the agent has been infected.
        days_infected (int): How many days until the agent recovers.
    """

    def __init__(self, model, state: str = "S"):
        super().__init__(model)
        self.state = state
        self.infection_timer = 0
        # Draw recovery duration from a normal distribution around the model's mean
        self.days_infected = max(
            1,
            int(
                self.random.normalvariate(
                    self.model.recovery_days, self.model.recovery_days * 0.2
                )
            ),
        )

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------

    def move(self):
        """Move to a random empty neighboring cell."""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    # ------------------------------------------------------------------
    # Infection logic
    # ------------------------------------------------------------------

    def infect_neighbors(self):
        """Try to infect susceptible neighbors."""
        if self.state != "I":
            return
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            if other is self:
                continue
            if other.state == "S" and self.random.random() < self.model.infection_prob:
                other.state = "I"

    # ------------------------------------------------------------------
    # Recovery logic
    # ------------------------------------------------------------------

    def recover(self):
        """Advance infection timer; recover when timer expires."""
        if self.state != "I":
            return
        self.infection_timer += 1
        if self.infection_timer >= self.days_infected:
            self.state = "R"

    # ------------------------------------------------------------------
    # Mesa step
    # ------------------------------------------------------------------

    def step(self):
        """One time-step: move, try to spread, try to recover."""
        self.move()
        self.infect_neighbors()
        self.recover()
