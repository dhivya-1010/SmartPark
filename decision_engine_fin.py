import pandas as pd

# ======================================
# Load Systemic Stress Dataset
# ======================================
parking = pd.read_csv("output/systemic_stress.csv")

print("Parking Locations :", len(parking))

# ======================================
# Rule-Based Decision Engine
# ======================================
def generate_recommendation(row):

    priority = row["Priority"]
    utilization = row["UtilizationLevel"]
    traffic = row["TrafficLevel"]

    # Critical situations
    if priority == "Critical":
        return (
            "Immediate intervention required. "
            "Activate dynamic pricing, redirect vehicles to nearby parking, "
            "and deploy traffic management measures."
        )

    # High stress
    elif priority == "High":

        if traffic == "Very High":
            return (
                "Redirect incoming vehicles to nearby parking areas and "
                "optimize traffic signal timings."
            )

        elif utilization == "High":
            return (
                "Increase parking turnover through pricing or time limits."
            )

        else:
            return (
                "Closely monitor occupancy and prepare overflow parking."
            )

    # Moderate stress
    elif priority == "Moderate":

        if traffic in ["High", "Very High"]:
            return (
                "Increase monitoring during peak traffic periods."
            )

        else:
            return (
                "Monitor occupancy trends and optimize parking guidance."
            )

    # Low stress
    else:
        return (
            "No immediate action required. Continue routine monitoring."
        )

# ======================================
# Apply Decision Engine
# ======================================
parking["Recommendation"] = parking.apply(
    generate_recommendation,
    axis=1
)

# ======================================
# Save
# ======================================
parking.to_csv(
    "output/final_decision_intelligence.csv",
    index=False
)

print("\nDecision Engine Completed!\n")

print(
    parking[
        [
            "ParkingName",
            "Priority",
            "Recommendation"
        ]
    ].head()
)

print("\nSaved Successfully!")