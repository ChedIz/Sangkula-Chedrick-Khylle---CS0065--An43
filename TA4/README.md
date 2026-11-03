# TA4 – Knowledge Representation, Rule-Based Reasoning (RBR), and Case-Based Reasoning (CBR)

**Use case: Laptop Troubleshooting Assistant**

The same laptop problem is solved in two ways so the reasoning methods can be compared.

- **Knowledge Representation:** a Python dictionary of 11 facts in 3 categories (status, measurements, symptoms).
- **Rule-Based Reasoning:** 7 IF–THEN rules + an inference engine that collects every action whose rule fires.
- **Case-Based Reasoning:** 4 past repair cases; Retrieve (feature-match similarity) → Reuse → Revise (edit or keep) → Retain.

## How to run
```bash
python kr_rbr_cbr_laptop.py
```
At the Revise step, type a new solution or press Enter to keep the retrieved one. Requires Python 3 (no extra libraries).

## Files
- `kr_rbr_cbr_laptop.py` – program source
- `TA4_Sangkula.pdf` – documentation, code, output screenshots, and reflection
