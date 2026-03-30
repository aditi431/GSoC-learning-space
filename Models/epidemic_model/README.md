# SIR Epidemic Model — Mesa

An agent-based SIR (Susceptible–Infected–Recovered) epidemic model built with [Mesa](https://mesa.readthedocs.io/).

Agents (people) move around a grid, infect neighbors, and eventually recover.  
Classic emergent behavior: epidemic curves, herd immunity, and extinction arise from simple local rules.

---

## Project Structure

```
epidemic_model/
├── agents.py        # PersonAgent — state machine (S → I → R)
├── model.py         # EpidemicModel — grid, scheduler, data collection
├── visualization.py # Interactive browser dashboard (SolaraViz)
├── analysis.py      # Single-run plots + parameter sweep heatmap
├── run_batch.py     # Headless batch runner → batch_results.csv
└── README.md
```

---

## Model Description

### States

| State | Meaning |
|-------|---------|
| **S** Susceptible | Healthy; can be infected by co-located infected agents |
| **I** Infected    | Sick and contagious; recovers after `recovery_days` (±20%) |
| **R** Recovered   | Immune; cannot be re-infected |

### Dynamics (each step = one day)

1. Every agent moves to a random neighboring cell (Moore neighborhood, toroidal grid).
2. Each infected agent attempts to infect every susceptible agent sharing its cell (prob = `infection_prob`).
3. Each infected agent increments its timer; recovers when timer ≥ its personal `days_infected`.

---

## Installation

```bash
pip install mesa matplotlib pandas numpy
```

---

## Usage

### Interactive visualization

```bash
solara run visualization.py
# → open http://127.0.0.1:8765
```

Sliders let you tune all parameters in real time.

### Run analysis & generate plots

```bash
python analysis.py
# → sir_curves.png
# → sir_heatmap.png
```

### Headless batch experiments

```bash
python run_batch.py
# → batch_results.csv
```

### Python API

```python
from model import EpidemicModel

model = EpidemicModel(
    n_agents=200,
    infection_prob=0.4,
    recovery_days=10,
    seed=42,
)
model.run(150)

df = model.datacollector.get_model_vars_dataframe()
print(df.tail())
```

---

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_agents` | 150 | Total number of people |
| `width` | 20 | Grid columns |
| `height` | 20 | Grid rows |
| `initial_infected` | 3 | Seed infections at step 0 |
| `infection_prob` | 0.3 | Probability of infecting a co-located susceptible per step |
| `recovery_days` | 14 | Mean days to recover (±20% individual variance) |

---

## Key Mesa Features Used

- `mesa.Model` + `mesa.Agent` — core building blocks
- `mesa.spaces.MultiGrid` — multiple agents per cell, toroidal wrapping
- `AgentSet.shuffle_do()` — random activation order each step
- `DataCollector` — model-level (S/I/R counts) and agent-level (state, timer) data
- `SolaraViz` + `make_space_component` + `make_plot_component` — browser dashboard

---

## What You Can Observe

- **Basic epidemic wave**: fast rise and fall of infections with moderate parameters.
- **Herd immunity**: when enough agents recover, spread slows even if susceptibles remain.
- **Extinction without full spread**: with low `infection_prob` or small grids, epidemic may die out early.
- **Parameter sensitivity**: the heatmap from `analysis.py` shows how `infection_prob` and `recovery_days` jointly determine peak burden.

---

## License

MIT — free to use, modify, and contribute.
