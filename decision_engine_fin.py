import pandas as pd

# ======================================
# Load Systemic Stress Dataset
# ======================================
parking = pd.read_csv("output/systemic_stress.csv")

print("Parking Locations :", len(parking))


# ======================================
# Government Decision Engine
# ======================================
def generate_decision(row):

    priority = row["Priority"]
    traffic = row["TrafficLevel"]
    utilization = row["UtilizationLevel"]
    peak_hour = row["PeakHour"]
    peak_day = row["PeakDay"]

    # ======================================
    # CRITICAL
    # ======================================
    if priority == "Critical":

        reason = (
            f"Critical parking demand caused by {utilization.lower()} parking utilization "
            f"and {traffic.lower()} surrounding traffic."
        )

        immediate = (
            "• Activate dynamic parking pricing\n"
            "• Redirect vehicles to nearby available parking facilities\n"
            "• Deploy traffic management personnel immediately\n"
            "• Update digital parking guidance signboards\n"
            f"• Increase monitoring around {peak_hour}:00 on {peak_day}"
        )

        long_term = (
            "Evaluate parking capacity expansion; "
            "Review parking pricing policy; "
            "Assess surrounding road network improvements."
        )

    # ======================================
    # HIGH
    # ======================================
    elif priority == "High":

        reason = (
            f"High parking utilization with {traffic.lower()} surrounding traffic "
            f"during peak demand periods."
        )

        immediate = (
            "• Redirect vehicles to nearby parking facilities\n"
            "• Optimize traffic signal timings\n"
            "• Increase parking enforcement during peak periods\n"
            f"• Monitor operations around {peak_hour}:00 on {peak_day}"
        )

        long_term = (
            "Review parking allocation strategy; "
            "Improve traffic signal coordination; "
            "Evaluate demand management policies."
        )

    # ======================================
    # MODERATE
    # ======================================
    elif priority == "Moderate":

        reason = (
            f"Moderate parking demand requiring operational monitoring "
            f"during peak periods."
        )

        immediate = (
            "• Increase monitoring during peak hours\n"
            "• Update parking guidance information\n"
            "• Monitor surrounding traffic conditions\n"
            f"• Focus monitoring around {peak_hour}:00 on {peak_day}"
        )

        long_term = (
            "Monitor utilization trends periodically; "
            "Review parking operations if demand increases."
        )

    # ======================================
    # LOW
    # ======================================
    else:

        reason = (
            "Low parking utilization with manageable surrounding traffic conditions."
        )

        immediate = (
            "• Continue routine monitoring\n"
            "• Maintain current parking operations\n"
            "• Perform scheduled inspections"
        )

        long_term = (
            "Continue periodic performance assessment and monitor future demand trends."
        )

    return pd.Series(
        [reason, immediate, long_term]
    )


# ======================================
# Apply Government Decision Engine
# ======================================
parking[
    [
        "Reason",
        "ImmediateActions",
        "LongTermConsiderations"
    ]
] = parking.apply(generate_decision, axis=1)


# ======================================
# Save Final Output
# ======================================
parking.to_csv(
    "output/final_decision_intelligence.csv",
    index=False
)


print("\nGovernment Decision Engine Completed!\n")

print(
    parking[
        [
            "ParkingName",
            "Priority",
            "Reason",
            "ImmediateActions",
            "LongTermConsiderations"
        ]
    ].head()
)

print("\nSaved Successfully!")