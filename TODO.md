# TODO — Environmental Change Based Scenario Simulation

## Steps

- [x] 1. Create `scenario_simulation.py` core engine module
  - [x] Define 10 environmental change scenarios with traffic/parking demand impacts
  - [x] Define 7 intervention strategies with mitigation effects
  - [x] Implement `simulate_scenario()` to compute future conditions
  - [x] Recompute TrafficScore, OccupancyScore, SystemicStress, Priority
  - [x] Compare current vs future state
  - [x] Evaluate & rank intervention strategies
  - [x] Save results to `output/scenario_scenario_summary.csv`
- [x] 2. Add `🌍 Scenario Simulation` page to `dashboard.py`
  - [x] Import scenario module
  - [x] Add nav option
  - [x] Scenario selector + intensity selector + intervention selector
  - [x] Current vs future comparison charts
  - [x] Priority shift table
  - [x] Intervention effectiveness ranking chart
- [x] 3. Verify
  - [x] Run `python scenario_simulation.py`
  - [x] Compile dashboard & scenario modules (py_compile)
