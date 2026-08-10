
from . import strategies as strats
from . import auto_mode
from pathlib import Path
import pandas as pd
import numpy as np
import os
from scipy.stats import norm, t, ttest_ind_from_stats
from .game_simulation import run_simulation, config_comparison_game


def run_pilot():
    """Runs 30k rounds for each strategy to calculate std and mean of return"""

    results = {}
    for strategy in strats.STRATEGY_NAMES_LIST:

        game = config_comparison_game(30000, strategy)
        game.players[0].id = game.players[0].strategy["name"]
        game.play(export_hand_data=True, export_meta_data=False)

        path = Path(f"data/hand_log_{game.id}.csv")
        if not path.exists():
            raise FileNotFoundError("Error opening hand log file")
        else:
            df = pd.read_csv(path, usecols=["round_id", "player_id", "profit/loss"])
            results[strategy] = {
                    "mean": float(df["profit/loss"].mean()),
                    "var": float(df["profit/loss"].var()),
                    }
            try:
                os.remove(path)
            except:
                print("Failed to delete file...")

    for strategy in strats.STRATEGY_NAMES_LIST:
    
            game = config_comparison_game(30000, strategy, insurance=True)
            game.players[0].id = game.players[0].strategy["name"] + " Insurance"
            game.play(export_hand_data=True, export_meta_data=False)
    
            path = Path(f"data/hand_log_{game.id}.csv")
            if not path.exists():
                raise FileNotFoundError("Error opening hand log file")
            else:
                df = pd.read_csv(path, usecols=["round_id", "player_id", "profit/loss"])
                results[game.players[0].id] = {
                        "mean": float(df["profit/loss"].mean()),
                        "var": float(df["profit/loss"].var()),
                        }
    
                try:
                    os.remove(path)
                except:
                    print("Failed to delete file...")

    return results


def calc_cohens_d(mean_1, mean_2, var_1, var_2):
    """Takes the mean and std of both given strategies to calculate Cohen's d"""
    
    if var_1 < 0 or var_2 < 0:
        raise ValueError("Variances can't be negative.")

    var_pooled = np.sqrt((var_1 + var_2)/2)
    return (mean_1 - mean_2) / var_pooled


def calc_required_n(cohens_d, power=0.8, alpha=0.05):
    """Performs a two-sided Power Analysis using a given Cohen's d, confidence level alpha and power"""

    if cohens_d == 0:
        return 101010
    z_alpha_2 = norm.ppf(1-(alpha/2))
    z_1_beta = norm.ppf(power if power > 0 else 0.8)
    n = (2 *(z_alpha_2 + z_1_beta)**2)/ cohens_d**2

    return min(int(np.ceil(n)), 101010)


def fetch_player_results(game_id):

    results = {}
    path = Path(f"data/hand_log_{game_id}.csv")
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")
    else:
        df = pd.read_csv(path, usecols=["round_id", "player_id", "profit/loss"])
        results["mean"] = df["profit/loss"].mean()
        results["var"] = df["profit/loss"].var()

        try:
            os.remove(path)
        except:
            print("Failed to delete file...")

    return results


def welch_t_test(n, mean_1, mean_2, var_1, var_2):
    """Run a Welch's t test on the simulation results"""

    se_1 = np.sqrt(var_1)/np.sqrt(n)
    se_2 = np.sqrt(var_2)/np.sqrt(n)
    se_pooled = np.sqrt(var_1/n + var_2/n)
    t_stat = (mean_1 - mean_2) / se_pooled
    df = (se_1**2 + se_2**2)**2 / ( se_1**4/(n-1) + se_2**4/(n-1))
    t_crit = t.ppf(0.975, df)
    p_value = 2 * (1 - t.cdf(np.abs(t_stat), df))
    conf_interval = [(mean_1 - mean_2) - se_pooled * t_crit, (mean_1 - mean_2) + se_pooled * t_crit]

    return {
        "p_value": p_value,
        "conf_interval": conf_interval,
        "t_stat": t_stat,
        "n": n,
        "mean_1": mean_1,
        "mean_2": mean_2,
        "var_1": var_1,
        "var_2": var_2,
    }


def run_comparison(strategy_1, strategy_2, pay_insurance_1, pay_insurance_2):

    results = {}

    strategy_1 = strategy_1 if not pay_insurance_1 else strategy_1 + " Insurance"
    strategy_2 = strategy_2 if not pay_insurance_2 else strategy_2 + " Insurance"

    d = calc_cohens_d(mean_1 = strats.PILOT_RUN_METRICS[strategy_1]["mean"],
                        mean_2 = strats.PILOT_RUN_METRICS[strategy_2]["mean"],
                        var_1 = strats.PILOT_RUN_METRICS[strategy_1]["var"],
                        var_2 = strats.PILOT_RUN_METRICS[strategy_2]["var"])

    n = calc_required_n(d)

    game_1 = config_comparison_game(n, strategy_1, pay_insurance_1)
    game_2 = config_comparison_game(n, strategy_2, pay_insurance_2)
    results_1 = fetch_player_results(run_simulation(game_1))
    results_2 = fetch_player_results(run_simulation(game_2))

    results = welch_t_test(n, 
                        mean_1 = results_1["mean"],
                        var_1 = results_1["var"],
                        mean_2 = results_2["mean"],
                        var_2 = results_2["var"])
    

    results["estimated_d"] = d

    scipy_results = ttest_ind_from_stats(results_1["mean"], np.sqrt(results_1["var"]), n, results_2["mean"], 
                                         np.sqrt(results_2["var"]), n, equal_var=False)

    results["scipy_pvalue"] = scipy_results.pvalue
    results["scipy_tstat"] = scipy_results.statistic
    results["d"] = calc_cohens_d(mean_1 = results_1["mean"],
                                var_1 = results_1["var"],
                                mean_2 = results_2["mean"],
                                var_2 = results_2["var"])

    return results
    

if __name__=="__main__":
    print(run_pilot())