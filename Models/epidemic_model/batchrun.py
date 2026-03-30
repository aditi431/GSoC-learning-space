"""
batch_run.py — Run multiple simulations with different parameters.
"""

from mesa.batchrunner import batch_run
import pandas as pd

from model import EpidemicModel


parameters = {
    "n_agents": [150],
    "infection_prob": [0.1, 0.2, 0.3, 0.4],
    "recovery_days": [7, 14, 21],
}


results = batch_run(
    EpidemicModel,
    parameters,
    iterations=3,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

df = pd.DataFrame(results)

df.to_csv("batch_results.csv")

print("Batch run finished.")
print("Results saved to batch_results.csv")