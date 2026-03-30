"""
analysis.py — Batch experiments and result plotting for the SIR Epidemic Model.

Usage:
    python analysis.py

Produces:
    - Console summary statistics
    - sir_curves.png   : SIR curves for a single run
    - sir_heatmap.png  : Peak infection % vs infection_prob × recovery_days
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

from model import EpidemicModel


# ---------------------------------------------------------------------------
# Single run
# ---------------------------------------------------------------------------

def single_run(
    n_agents=150,
    infection_prob=0.3,
    recovery_days=14,
    n_steps=200,
    seed=42,
):
    """Run one simulation and return the collected DataFrame."""
    model = EpidemicModel(
        n_agents=n_agents,
        infection_prob=infection_prob,
        recovery_days=recovery_days,
        seed=seed,
    )
    model.run(n_steps)
    df = model.datacollector.get_model_vars_dataframe()
    return df


def plot_sir_curves(df, n_agents, save_path="sir_curves.png"):
    """Plot S/I/R counts over time."""
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df.index, df["Susceptible"], color="#1f77b4", lw=2, label="Susceptible")
    ax.plot(df.index, df["Infected"],    color="#d62728", lw=2, label="Infected")
    ax.plot(df.index, df["Recovered"],   color="#2ca02c", lw=2, label="Recovered")

    ax.set_xlabel("Day", fontsize=12)
    ax.set_ylabel("Number of Agents", fontsize=12)
    ax.set_title("SIR Epidemic Dynamics", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.set_xlim(left=0)
    ax.set_ylim(0, n_agents * 1.05)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    print(f"Saved → {save_path}")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Batch / parameter sweep
# ---------------------------------------------------------------------------

def parameter_sweep(
    infection_probs=(0.1, 0.2, 0.3, 0.4, 0.5),
    recovery_days_list=(7, 14, 21),
    n_agents=150,
    n_steps=200,
    n_replicates=3,
):
    """
    Sweep infection_prob × recovery_days, averaging over replicates.
    Returns a DataFrame with columns:
        infection_prob, recovery_days, peak_infected, final_recovered, epidemic_length
    """
    records = []
    total = len(infection_probs) * len(recovery_days_list) * n_replicates
    done = 0

    for ip in infection_probs:
        for rd in recovery_days_list:
            peak_list, final_r_list, length_list = [], [], []

            for rep in range(n_replicates):
                model = EpidemicModel(
                    n_agents=n_agents,
                    infection_prob=ip,
                    recovery_days=rd,
                    seed=rep * 100,
                )
                model.run(n_steps)
                df = model.datacollector.get_model_vars_dataframe()

                peak_list.append(df["Infected"].max())
                final_r_list.append(df["Recovered"].iloc[-1])
                # epidemic length = last step where I > 0
                infected_steps = df[df["Infected"] > 0].index
                length_list.append(int(infected_steps[-1]) if len(infected_steps) else 0)

                done += 1
                print(f"  [{done}/{total}] ip={ip:.2f}  rd={rd}  rep={rep}")

            records.append(
                {
                    "infection_prob": ip,
                    "recovery_days": rd,
                    "peak_infected": np.mean(peak_list),
                    "peak_infected_pct": np.mean(peak_list) / n_agents * 100,
                    "final_recovered_pct": np.mean(final_r_list) / n_agents * 100,
                    "epidemic_length": np.mean(length_list),
                }
            )

    return pd.DataFrame(records)


def plot_heatmap(sweep_df, metric="peak_infected_pct", save_path="sir_heatmap.png"):
    """Plot a heatmap of *metric* over infection_prob × recovery_days."""
    pivot = sweep_df.pivot(
        index="recovery_days", columns="infection_prob", values=metric
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd", origin="lower")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(f"{metric.replace('_', ' ').title()} (%)", fontsize=11)

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels([f"{v:.2f}" for v in pivot.columns])
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)

    ax.set_xlabel("Infection Probability", fontsize=12)
    ax.set_ylabel("Recovery Days", fontsize=12)
    ax.set_title("Peak Infection % — Parameter Sweep", fontsize=14, fontweight="bold")

    # Annotate cells
    for (i, j), val in np.ndenumerate(pivot.values):
        ax.text(j, i, f"{val:.0f}%", ha="center", va="center", fontsize=9,
                color="black" if val < 60 else "white")

    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    print(f"Saved → {save_path}")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    N_AGENTS = 150

    # --- Single run ---
    print("=== Single run ===")
    df_single = single_run(n_agents=N_AGENTS)
    print(df_single.describe().round(1))
    plot_sir_curves(df_single, n_agents=N_AGENTS)

    # --- Parameter sweep ---
    print("\n=== Parameter sweep ===")
    sweep_df = parameter_sweep(n_agents=N_AGENTS, n_replicates=3)
    print(sweep_df.to_string(index=False))
    plot_heatmap(sweep_df)

    print("\nDone!")
