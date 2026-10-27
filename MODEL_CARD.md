# Model card — Telco churn prioritisation

## Intended use
Educational risk ranking and exploratory retention planning on a public IBM fictional telecom sample. Not a production score, causal uplift model or automated adverse-decision tool.

## Evaluation design
Stratified 80/20 split (seed 42). Five-fold stratified cross-validation on the **training 80%** selects between Logistic Regression, Decision Tree and Random Forest. Median/mode imputation, scaling and one-hot encoding are fitted inside each training fold. The final model is fitted to the full development set and evaluated once on the untouched hold-out.

## Reproduced results
- Selected: **Random Forest**
- Development CV ROC-AUC: **0.846 ± 0.008**
- Hold-out ROC-AUC: **0.841**
- Hold-out average precision: **0.643** (churn prevalence **0.265**)
- Hold-out Brier: **0.137**
- At 0.50: TP **188**, FP **103**, TN **932**, FN **186**
- Top 20% hold-out captures **49.5%** of churners.

## Feature caveats
`TotalCharges` is excluded from the primary model because it is a cumulative measure strongly associated with `tenure` and `MonthlyCharges`; it may also be unknown at a genuine earlier scoring point. A sensitivity analysis with the feature is in the reports. `Contract`, `tenure`, service and billing characteristics are observational correlates, not proof of causal churn drivers. Any production features must be confirmed available *before* the intended prediction date.

## Limitations and safeguards
Fictional sample; random split rather than temporal validation; no intervention labels or causal uplift; no fairness assessment; no operational cost data; calibration assessed on one hold-out. Before deployment: verify data rights, perform temporal/external validation, calibrate as needed, test fairness, monitor drift and use controlled retention experiments.
