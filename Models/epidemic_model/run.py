"""
run.py — Simple script to run the epidemic model from terminal.
"""

from model import EpidemicModel


def main():

    model = EpidemicModel(
        n_agents=150,
        width=20,
        height=20,
        initial_infected=3,
        infection_prob=0.3,
        recovery_days=14,
    )

    steps = 100

    print("Running simulation...")

    for i in range(steps):
        model.step()

    df = model.datacollector.get_model_vars_dataframe()

    print("\nSimulation results:")
    print(df.tail())


if __name__ == "__main__":
    main()