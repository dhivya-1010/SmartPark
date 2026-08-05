"""
=========================================================================
ENVIRONMENTAL CHANGE BASED SCENARIO SIMULATION MODULE
=========================================================================
Decision Intelligence layer that evaluates FUTURE urban scenarios.

For each user-selected environmental change this module:
    1. Estimates the increase/decrease in traffic demand.
    2. Estimates the increase in parking demand.
    3. Recalculates Systemic Stress for the future state.
    4. Compares current vs future state.
    5. Evaluates multiple intervention strategies and ranks their
       effectiveness in reducing systemic stress.
=========================================================================
"""

import pandas as pd

# =========================================================================
# 1. ENVIRONMENTAL CHANGE SCENARIOS
#    Each scenario has a baseline % impact on traffic demand and
#    parking demand. The intensity multiplier (low / medium / high)
#    scales these baseline impacts.
# =========================================================================
SCENARIOS = {
    "New Tech Park": {
        "traffic_impact": 0.18,   # +18% traffic
        "parking_impact": 0.22,   # +22% parking demand
        "description": (
            "A new technology park attracts thousands of daily commuters, "
            "significantly boosting both road traffic and parking demand "
            "in surrounding areas."
        ),
    },
    "Population Growth": {
        "traffic_impact": 0.20,
        "parking_impact": 0.18,
        "description": (
            "Urban population growth increases the number of vehicles on "
            "the road and raises baseline parking demand across the city."
        ),
    },
    "Shopping Mall": {
        "traffic_impact": 0.15,
        "parking_impact": 0.25,
        "description": (
            "A new shopping mall generates concentrated traffic and very "
            "high parking demand, especially during evenings and weekends."
        ),
    },
    "Stadium": {
        "traffic_impact": 0.12,
        "parking_impact": 0.28,
        "description": (
            "A stadium causes periodic but intense surges in traffic and "
            "parking demand during events and match days."
        ),
    },
    "Hospital": {
        "traffic_impact": 0.10,
        "parking_impact": 0.20,
        "description": (
            "A new hospital increases steady all-day traffic and expands "
            "long-stay parking demand for patients and visitors."
        ),
    },
    "School / College": {
        "traffic_impact": 0.12,
        "parking_impact": 0.15,
        "description": (
            "An educational institution adds peak-hour traffic during "
            "drop-off and pick-up times and raises parking demand during "
            "term time."
        ),
    },
    "Residential Expansion": {
        "traffic_impact": 0.16,
        "parking_impact": 0.20,
        "description": (
            "New residential developments bring more resident vehicles, "
            "increasing overnight parking demand and commuter traffic."
        ),
    },
    "Road Closure": {
        "traffic_impact": 0.25,
        "parking_impact": 0.10,
        "description": (
            "A road closure diverts traffic onto alternative routes, "
            "concentrating congestion and raising parking pressure in "
            "adjacent streets."
        ),
    },
    "Metro Station": {
        "traffic_impact": 0.08,
        "parking_impact": 0.06,
        "description": (
            "A metro station encourages park-and-ride but also attracts "
            "feeder traffic and parking demand near the station."
        ),
    },
    "Bus Terminal": {
        "traffic_impact": 0.06,
        "parking_impact": 0.05,
        "description": (
            "A bus terminal increases bus-related traffic flow and "
            "moderate parking demand for commuters connecting onward."
        ),
    },
}

# Intensity multipliers applied to a scenario's baseline impacts.
INTENSITY = {
    "Low": 0.5,
    "Medium": 1.0,
    "High": 1.5,
}

# =========================================================================
# 2. INTERVENTION STRATEGIES
#    Each strategy reduces either traffic demand, parking demand, or both.
#    The mitigation is expressed as a % reduction applied when the
#    intervention is activated for a scenario.
# =========================================================================
INTERVENTIONS = {
    "No Intervention": {
        "traffic_reduction": 0.0,
        "parking_reduction": 0.0,
        "description": "Baseline future state with no mitigating action.",
    },
    "Increase Parking Capacity": {
        "traffic_reduction": 0.0,
        "parking_reduction": 0.25,
        "description": (
            "Adds parking spaces to absorb excess demand, reducing parking "
            "stress without directly altering traffic volumes."
        ),
    },
    "Dynamic Pricing": {
        "traffic_reduction": 0.05,
        "parking_reduction": 0.15,
        "description": (
            "Variable pricing discourages unnecessary journeys and "
            "spreads parking demand across the day."
        ),
    },
    "Shuttle Services": {
        "traffic_reduction": 0.12,
        "parking_reduction": 0.10,
        "description": (
            "Frequent shuttles move people from peripheral parking to "
            "destinations, cutting through-traffic and central parking demand."
        ),
    },
    "Public Transport Incentives": {
        "traffic_reduction": 0.15,
        "parking_reduction": 0.12,
        "description": (
            "Subsidised public transport shifts car trips to transit, "
            "reducing both traffic and parking pressure."
        ),
    },
    "Traffic Diversion": {
        "traffic_reduction": 0.18,
        "parking_reduction": 0.02,
        "description": (
            "Redirects through-traffic to alternative corridors, easing "
            "congestion around high-stress facilities."
        ),
    },
    "Signal Optimization": {
        "traffic_reduction": 0.10,
        "parking_reduction": 0.03,
        "description": (
            "Smart signal timing smooths traffic flow, reducing idling and "
            "congestion near parking entrances."
        ),
    },
    "New Parking Facility": {
        "traffic_reduction": 0.02,
        "parking_reduction": 0.30,
        "description": (
            "A new purpose-built parking facility significantly relieves "
            "parking demand in the most stressed zones."
        ),
    },
}

# =========================================================================
# 3. STRESS RECOMPUTATION (mirrors sysetmic_stress.py)
# =========================================================================
def classify_priority(stress):
    """Map a SystemicStress value to a Priority band."""
    if stress < 30:
        return "Low"
    elif stress < 60:
        return "Moderate"
    elif stress < 80:
        return "High"
    else:
        return "Critical"


def recompute_scores(df):
    """
    Given a DataFrame with 'VehicleCount' (traffic) and 'OccupancyRatio'
    (parking), recompute TrafficScore, OccupancyScore, SystemicStress and
    Priority exactly as the existing systemic stress engine does.
    """
    out = df.copy()

    # --- Traffic Score (min-max normalized to 0-100) ---
    min_vehicle = out["VehicleCount"].min()
    max_vehicle = out["VehicleCount"].max()
    if max_vehicle > min_vehicle:
        out["TrafficScore"] = (
            (out["VehicleCount"] - min_vehicle)
            / (max_vehicle - min_vehicle)
        ) * 100
    else:
        out["TrafficScore"] = 0.0
    out["TrafficScore"] = out["TrafficScore"].round(2)

    # --- Occupancy Score (= OccupancyRatio, 0-100) ---
    out["OccupancyScore"] = out["OccupancyRatio"].round(2)

    # --- Systemic Stress Index ---
    out["SystemicStress"] = (
        0.6 * out["OccupancyScore"] + 0.4 * out["TrafficScore"]
    ).round(2)

    # --- Priority Classification ---
    out["Priority"] = out["SystemicStress"].apply(classify_priority)

    return out


# =========================================================================
# 4. CORE SIMULATION
# =========================================================================
def simulate_scenario(
    df,
    scenario_name,
    intensity="Medium",
    intervention="No Intervention",
):
    """
    Simulate a future state for a chosen environmental change.

    Parameters
    ----------
    df : pd.DataFrame
        Current-state parking facilities (from final_decision_intelligence.csv).
    scenario_name : str
        One of the keys in SCENARIOS.
    intensity : str
        'Low', 'Medium' or 'High'.
    intervention : str
        One of the keys in INTERVENTIONS.

    Returns
    -------
    dict with keys:
        scenario     : scenario metadata
        intensity    : chosen intensity
        intervention : intervention metadata
        traffic_impact  : net traffic demand change
        parking_impact  : net parking demand change
        future_df    : DataFrame of future-state facilities
        current_df   : input df (with recomputed baseline columns)
        comparison   : summary DataFrame comparing current vs future
    """
    scenario = SCENARIOS[scenario_name]
    inten = INTENSITY[intensity]
    inter = INTERVENTIONS[intervention]

    # Scale baseline scenario impacts by intensity
    traffic_impact = scenario["traffic_impact"] * inten
    parking_impact = scenario["parking_impact"] * inten

    # Apply intervention mitigation (reductions)
    traffic_net = traffic_impact * (1.0 - inter["traffic_reduction"])
    parking_net = parking_impact * (1.0 - inter["parking_reduction"])

    # Build the future scenario as new columns on the current dataframe
    future = df.copy()
    future["Scenario"] = scenario_name
    future["ScenarioIntensity"] = intensity
    future["Intervention"] = intervention
    future["TrafficDemandChange"] = traffic_net
    future["ParkingDemandChange"] = parking_net

    # --- Simulate future conditions ---
    # Traffic demand increases by traffic_net fraction
    future["FutureVehicleCount"] = (
        future["VehicleCount"] * (1.0 + traffic_net)
    ).round(0)

    # Parking demand increases by parking_net fraction
    future["FutureAvgOccupancy"] = (
        future["AvgOccupancy"] * (1.0 + parking_net)
    ).round(2)

    # Recompute occupancy ratio (capped at 100 to be physically sensible)
    future["FutureOccupancyRatio"] = (
        (future["FutureAvgOccupancy"] / future["Capacity"]) * 100
    ).clip(upper=100).round(2)

    # --- Recalculate Systemic Stress for the future state ---
    future["VehicleCount"] = future["FutureVehicleCount"]
    future["OccupancyRatio"] = future["FutureOccupancyRatio"]
    future = recompute_scores(future)

    # Restore future columns for clarity
    future["FutureTrafficScore"] = future["TrafficScore"]
    future["FutureOccupancyScore"] = future["OccupancyScore"]
    future["FutureSystemicStress"] = future["SystemicStress"]
    future["FuturePriority"] = future["Priority"]

    # Keep the current-state scores for comparison
    current = df.copy()
    current = recompute_scores(current)
    current["CurrentSystemicStress"] = current["SystemicStress"]
    current["CurrentPriority"] = current["Priority"]

    # Build comparison summary
    comparison = pd.DataFrame(
        {
            "SystemCodeNumber": current["SystemCodeNumber"],
            "ParkingName": current["ParkingName"],
            "CurrentSystemicStress": current["CurrentSystemicStress"],
            "CurrentPriority": current["CurrentPriority"],
            "FutureSystemicStress": future["FutureSystemicStress"].values,
            "FuturePriority": future["FuturePriority"].values,
            "CurrentTrafficScore": current["TrafficScore"].values,
            "FutureTrafficScore": future["FutureTrafficScore"].values,
            "CurrentOccupancyScore": current["OccupancyScore"].values,
            "FutureOccupancyScore": future["FutureOccupancyScore"].values,
            "StressDelta": (
                future["FutureSystemicStress"].values
                - current["CurrentSystemicStress"].values
            ).round(2),
        }
    )

    return {
        "scenario": scenario,
        "intensity": intensity,
        "intervention": inter,
        "traffic_impact": traffic_net,
        "parking_impact": parking_net,
        "future_df": future,
        "current_df": current,
        "comparison": comparison,
    }


# =========================================================================
# 5. INTERVENTION EVALUATION
#    For a given scenario + intensity, run every intervention and rank
#    them by how much they reduce future systemic stress.
# =========================================================================
def evaluate_interventions(df, scenario_name, intensity="Medium"):
    results = []

    for name in INTERVENTIONS.keys():
        res = simulate_scenario(df, scenario_name, intensity, name)

        comp = res["comparison"]

        avg_stress = comp["FutureSystemicStress"].mean()
        max_stress = comp["FutureSystemicStress"].max()
        critical_count = (comp["FuturePriority"] == "Critical").sum()
        high_count = (comp["FuturePriority"] == "High").sum()
        stress_above_60 = (comp["FutureSystemicStress"] >= 60).sum()

        results.append(
            {
                "Intervention": name,
                "AvgSystemicStress": round(avg_stress, 2),
                "MaxSystemicStress": round(max_stress, 2),
                "CriticalCount": critical_count,
                "HighCount": high_count,
                "StressAbove60": stress_above_60,
                "TrafficReduction": INTERVENTIONS[name]["traffic_reduction"],
                "ParkingReduction": INTERVENTIONS[name]["parking_reduction"],
            }
        )

    ranking_df = pd.DataFrame(results)
    ranking_df = ranking_df.sort_values(
        "AvgSystemicStress", ascending=True
    ).reset_index(drop=True)
    return ranking_df


# =========================================================================
# 6. MAIN ENTRY POINT (CLI usage)
# =========================================================================
def main():
    print("=" * 70)
    print("ENVIRONMENTAL CHANGE BASED SCENARIO SIMULATION")
    print("=" * 70)

    df = pd.read_csv("output/final_decision_intelligence.csv")
    print(f"Parking Facilities : {len(df)}")

    # Run a default demonstration across all scenarios (Medium intensity)
    all_rows = []

    for scenario_name in SCENARIOS.keys():
        res = simulate_scenario(df, scenario_name, "Medium", "No Intervention")
        comp = res["comparison"]
        all_rows.append(
            {
                "Scenario": scenario_name,
                "AvgCurrentStress": round(comp["CurrentSystemicStress"].mean(), 2),
                "AvgFutureStress": round(comp["FutureSystemicStress"].mean(), 2),
                "StressDelta": round(
                    comp["FutureSystemicStress"].mean()
                    - comp["CurrentSystemicStress"].mean(),
                    2,
                ),
                "CriticalBefore": int(
                    (comp["CurrentPriority"] == "Critical").sum()
                ),
                "CriticalAfter": int(
                    (comp["FuturePriority"] == "Critical").sum()
                ),
                "HighBefore": int((comp["CurrentPriority"] == "High").sum()),
                "HighAfter": int((comp["FuturePriority"] == "High").sum()),
            }
        )

    summary = pd.DataFrame(all_rows)

    # Save
    summary.to_csv(
        "output/scenario_scenario_summary.csv",
        index=False,
    )
    print("\nScenario Summary saved to: output/scenario_scenario_summary.csv\n")
    print(summary.to_string(index=False))

    # Demonstrate intervention evaluation for the most impactful scenario
    print("\n" + "=" * 70)
    print("INTERVENTION EVALUATION — Shopping Mall (Medium)")
    print("=" * 70)
    ranking = evaluate_interventions(df, "Shopping Mall", "Medium")
    print(ranking.to_string(index=False))
    ranking.to_csv(
        "output/scenario_intervention_ranking.csv",
        index=False,
    )
    print(
        "\nIntervention ranking saved to: "
        "output/scenario_intervention_ranking.csv"
    )


if __name__ == "__main__":
    main()
