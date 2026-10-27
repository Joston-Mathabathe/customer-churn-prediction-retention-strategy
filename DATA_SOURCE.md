# Dataset provenance
File: `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`

The public **IBM Telco Customer Churn sample** describes a fictional telecom business and is widely mirrored on Kaggle. The original file has 7,043 records and 21 columns. It is **not proprietary customer data** and is **not real-world operational evidence** from a named telecom provider.

`TotalCharges` has 11 blank numeric entries in the source. These are preserved as missing in the processed dataset, with imputation handled inside training folds. The source file's `MonthlyCharges` and `TotalCharges` are **not denominated in rand by this project**.

Review the upstream dataset's redistribution terms before publicly hosting the raw CSV. The separate R-denominated business case is entirely hypothetical.
