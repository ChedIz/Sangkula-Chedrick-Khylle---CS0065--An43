# TA3 – Case-Based Reasoning (CBR) System Development

**Case Study 1: Disaster Response Decision Support System (DSS)**

A simple CBR program that helps a local government unit plan its response to a new disaster by reusing the response plans of similar past disasters (Typhoon Ursula, Odette, Ulysses, Tropical Storm Ondoy, Bohol Earthquake — simplified sample data).

## CBR cycle
1. **Retrieve** – weighted similarity (categorical match + normalized numeric distance) ranks all past cases.
2. **Reuse** – takes the solution of the most similar case.
3. **Revise** – adapts evacuees, shelters, food packs, rescue/medical teams, boats, and evacuation strategy to the new event.
4. **Retain** – saves the new case to `case_base.json` and shows the updated case base.

## How to run
```bash
python cbr_disaster_dss.py                # demo: typhoon with urban flooding
python cbr_disaster_dss.py --interactive  # enter your own disaster event
python cbr_disaster_dss.py --reset        # restore the 5 original cases
```
Requires Python 3 (built-in modules only).

## Files
- `cbr_disaster_dss.py` – program source
- `TA3_Sangkula_Sagpang.pdf` – documentation, code, screenshots, and pair reflection
