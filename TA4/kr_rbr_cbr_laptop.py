"""
TA4 - Implementing Knowledge Representation (KR),
      Rule-Based Reasoning (RBR), and Case-Based Reasoning (CBR)

Use case: LAPTOP TROUBLESHOOTING ASSISTANT
The same laptop problem is solved in two ways:
  - RBR: expert IF-THEN rules fire on the current facts
  - CBR: the most similar past repair case is retrieved, reused,
         revised (optional), and retained

Run:
    python kr_rbr_cbr_laptop.py
"""

# =====================================================================
# PART 1 - KNOWLEDGE REPRESENTATION (KR)
# Task 1A: Knowledge base stored as a Python dictionary.
# Facts are grouped into 3 categories: status, measurements, symptoms.
# =====================================================================
knowledge_base = {
    "status": {                      # Category 1: current state of the laptop
        "is_plugged_in": False,
        "is_charging": False,
        "wifi_connected": False,
    },
    "measurements": {                # Category 2: numeric readings
        "battery_percent": 12,
        "cpu_temperature_c": 92,
        "free_storage_gb": 4,
        "ram_usage_percent": 91,
    },
    "symptoms": {                    # Category 3: what the user observes
        "fan_noise_loud": True,
        "runs_slow": True,
        "screen_flicker": False,
        "wont_turn_on": False,
    },
}


def get_fact(kb, name):
    """Look up a fact by name, no matter which category it is in."""
    for category in kb.values():
        if name in category:
            return category[name]
    raise KeyError(f"Unknown fact: {name}")


def show_knowledge_base(kb):
    print("KNOWLEDGE BASE (facts about the laptop)")
    print("-" * 60)
    for category, facts in kb.items():
        print(f"[{category.upper()}]")
        for name, value in facts.items():
            print(f"   {name:<22}: {value}")
    print()


# =====================================================================
# PART 2 - RULE-BASED REASONING (RBR)
# Task 2A: IF-THEN rules written as Python functions.
# Each rule returns an action if its condition is true, else None.
# =====================================================================
def rule_overheating(kb):
    # IF CPU temperature > 85 C AND fan is loud THEN clean vents/fans
    if get_fact(kb, "cpu_temperature_c") > 85 and get_fact(kb, "fan_noise_loud"):
        return "Overheating: clean the vents/fan and use a cooling pad"


def rule_low_battery(kb):
    # IF battery < 20% AND not plugged in THEN plug in the charger
    if get_fact(kb, "battery_percent") < 20 and not get_fact(kb, "is_plugged_in"):
        return "Low battery: plug in the charger now"


def rule_charger_fault(kb):
    # IF plugged in BUT not charging THEN check charger/adapter
    if get_fact(kb, "is_plugged_in") and not get_fact(kb, "is_charging"):
        return "Plugged in but not charging: check the adapter and cable"


def rule_low_storage(kb):
    # IF free storage < 10 GB THEN clean up disk
    if get_fact(kb, "free_storage_gb") < 10:
        return "Low storage: delete temp files / uninstall unused apps"


def rule_slow_performance(kb):
    # IF runs slow AND RAM usage > 85% THEN close background apps
    if get_fact(kb, "runs_slow") and get_fact(kb, "ram_usage_percent") > 85:
        return "High RAM usage: close background apps and startup programs"


def rule_no_wifi(kb):
    # IF Wi-Fi is not connected THEN restart the adapter/router
    if not get_fact(kb, "wifi_connected"):
        return "No Wi-Fi: toggle airplane mode or restart the router"


def rule_no_power(kb):
    # IF laptop won't turn on THEN do a hard reset
    if get_fact(kb, "wont_turn_on"):
        return "Won't turn on: hold the power button for 30s (hard reset)"


RULES = [rule_overheating, rule_low_battery, rule_charger_fault,
         rule_low_storage, rule_slow_performance, rule_no_wifi, rule_no_power]


# Task 2B: Inference engine - reads the KB, checks every rule,
# and collects all actions that were inferred (forward chaining).
def inference_engine(kb, rules):
    actions, fired = [], []
    for rule in rules:
        result = rule(kb)
        if result:                      # condition was true -> rule fired
            fired.append(rule.__name__)
            actions.append(result)
    return actions, fired


# =====================================================================
# PART 3 - CASE-BASED REASONING (CBR)
# Task 3A: Case base of past repairs (problem features + solution).
# =====================================================================
case_base = [
    {"problem": {"wont_turn_on": False, "fan_noise_loud": True,  "runs_slow": True,
                 "overheating": True,  "screen_flicker": False, "battery_low": False},
     "solution": "Cleaned dust from fan and replaced thermal paste."},
    {"problem": {"wont_turn_on": True,  "fan_noise_loud": False, "runs_slow": False,
                 "overheating": False, "screen_flicker": False, "battery_low": True},
     "solution": "Replaced faulty charger; battery recharged normally."},
    {"problem": {"wont_turn_on": False, "fan_noise_loud": False, "runs_slow": True,
                 "overheating": False, "screen_flicker": False, "battery_low": False},
     "solution": "Removed startup programs and upgraded RAM to 16 GB."},
    {"problem": {"wont_turn_on": False, "fan_noise_loud": False, "runs_slow": False,
                 "overheating": False, "screen_flicker": True,  "battery_low": False},
     "solution": "Updated display driver and reseated the screen cable."},
]


def features_from_kb(kb):
    """Convert the knowledge base into CBR problem features."""
    return {
        "wont_turn_on": get_fact(kb, "wont_turn_on"),
        "fan_noise_loud": get_fact(kb, "fan_noise_loud"),
        "runs_slow": get_fact(kb, "runs_slow"),
        "overheating": get_fact(kb, "cpu_temperature_c") > 85,
        "screen_flicker": get_fact(kb, "screen_flicker"),
        "battery_low": get_fact(kb, "battery_percent") < 20,
    }


# Task 3B: Retrieve - similarity = matching features / total features
def similarity(new_problem, old_problem):
    matches = sum(1 for f in new_problem if new_problem[f] == old_problem.get(f))
    return matches / len(new_problem)


def retrieve(new_problem, cases):
    scored = [(similarity(new_problem, c["problem"]), c) for c in cases]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored


# Task 3C: Reuse - return the solution of the most similar case
def reuse(best_case):
    return best_case["solution"]


# Task 3D: Revise - user may edit the solution, or press Enter to keep it
def revise(solution):
    print(f"Proposed solution: {solution}")
    edited = input("Revise solution (press Enter to keep unchanged): ").strip()
    if edited:
        print("-> Solution revised by user.")
        return edited
    print("-> Solution kept unchanged.")
    return solution


# Task 3E: Retain - store the new case so the system learns
def retain(cases, problem, solution):
    cases.append({"problem": problem, "solution": solution})
    print(f"-> New case saved! Case base now has {len(cases)} cases.")


def show_case_base(cases):
    for i, c in enumerate(cases, start=1):
        true_feats = [f for f, v in c["problem"].items() if v] or ["(none)"]
        print(f"   Case {i}: {', '.join(true_feats)}")
        print(f"           -> {c['solution']}")


# =====================================================================
# MAIN
# =====================================================================
def main():
    print("=" * 64)
    print("  LAPTOP TROUBLESHOOTING ASSISTANT - KR, RBR and CBR")
    print("=" * 64)

    # ---------- PART 1: KR ----------
    print("\nPART 1 - KNOWLEDGE REPRESENTATION")
    show_knowledge_base(knowledge_base)

    # ---------- PART 2: RBR ----------
    print("=" * 64)
    print("PART 2 - RULE-BASED REASONING")
    print("=" * 64)
    actions, fired = inference_engine(knowledge_base, RULES)
    print(f"Rules checked: {len(RULES)}   Rules fired: {len(fired)}")
    print("Fired rules  : " + ", ".join(fired))
    print("\nRule-Based Reasoning Actions:")
    for a in actions:
        print(f"- {a}")

    # ---------- PART 3: CBR ----------
    print("\n" + "=" * 64)
    print("PART 3 - CASE-BASED REASONING")
    print("=" * 64)
    new_problem = features_from_kb(knowledge_base)
    print("New problem features:")
    for f, v in new_problem.items():
        print(f"   {f:<16}: {v}")

    print("\n[RETRIEVE] Similarity to past cases:")
    ranked = retrieve(new_problem, case_base)
    for score, case in ranked:
        idx = case_base.index(case) + 1
        print(f"   Case {idx}: {score:.0%}  -> {case['solution']}")
    best_score, best_case = ranked[0]
    print(f"Most similar case: Case {case_base.index(best_case) + 1} ({best_score:.0%})")

    print("\n[REUSE]")
    solution = reuse(best_case)
    print(f"Reused solution from Case {case_base.index(best_case) + 1}: {solution}")

    print("\n[REVISE]")
    final_solution = revise(solution)

    print("\n[RETAIN]")
    retain(case_base, new_problem, final_solution)
    print("\nUpdated case base:")
    show_case_base(case_base)

    print("\nCBR Final Solution:")
    print(f"- {final_solution}")
    print("=" * 64)


if __name__ == "__main__":
    main()
