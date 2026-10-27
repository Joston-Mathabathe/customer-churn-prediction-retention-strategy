# Power BI dashboard specification (not a delivered .pbix)

## Page 1 — Executive retention overview
Customer count, observed churn rate, tenure distribution, contract mix, average monthly charges **in original dataset units**.

## Page 2 — Customer segments
Churn by contract, internet service, tenure and payment method. Show segment sample sizes; observational associations are not causal drivers.

## Page 3 — Model performance
Independent hold-out ROC-AUC, average precision, churn prevalence, Brier score, confusion matrix, calibration chart and top-20% capture. Clearly distinguish development cross-validation from hold-out.

## Page 4 — Retention decisions
Top-risk queue size, contact capacity, assumed retention uplift, R-denominated hypothetical costs, incremental contribution and net value. Do **not** treat the original dataset's billing amounts as rand.

**Status:** Design specification only. Source tables are provided in `reports/`. No `.pbix` file is included.
