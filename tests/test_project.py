import json
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


class ChurnProjectTests(unittest.TestCase):
    def test_data_size_and_target(self):
        d = pd.read_csv(ROOT / "data/processed/telco_customer_churn_clean.csv")
        self.assertEqual(len(d), 7043)
        self.assertEqual(int(d.ChurnFlag.sum()), 1869)
        self.assertTrue(d.customerID.is_unique)

    def test_missingness_preserved(self):
        d = pd.read_csv(ROOT / "data/processed/telco_customer_churn_clean.csv")
        self.assertEqual(int(d.TotalCharges.isna().sum()), 11)

    def test_holdout_and_cv(self):
        m = json.loads((ROOT / "reports/model_summary.json").read_text())
        self.assertEqual(m["test_rows"], 1409)
        self.assertGreater(m["holdout_roc_auc"], 0.7)
        cv = pd.read_csv(ROOT / "reports/cross_validation.csv")
        self.assertEqual(len(cv), 3)
        self.assertTrue(cv.cv_roc_auc_mean.between(0, 1).all())

    def test_holdout_queue_integrity(self):
        m = json.loads((ROOT / "reports/model_summary.json").read_text())
        q = pd.read_csv(ROOT / "reports/holdout_retention_queue.csv")
        self.assertEqual(len(q), m["test_rows"])
        self.assertTrue(q.customerID.is_unique)
        self.assertTrue(q.churn_probability.between(0, 1).all())
        self.assertEqual(int(q.ChurnFlag.sum()), m["test_churn_count"])
        selected = q.priority_top_20pct.astype(str).str.lower().eq("true")
        self.assertEqual(int(selected.sum()), int(np.ceil(0.2 * len(q))))
        captured = q.loc[selected, "ChurnFlag"].sum() / q.ChurnFlag.sum()
        self.assertAlmostEqual(captured, m["top_20pct_holdout_churn_capture"], places=10)
        top_min = q.loc[selected, "churn_probability"].min()
        other_max = q.loc[~selected, "churn_probability"].max()
        self.assertGreaterEqual(top_min, other_max)

    def test_scenario_and_calibration(self):
        s = pd.read_csv(ROOT / "reports/retention_scenario_sensitivity.csv")
        q = pd.read_csv(ROOT / "reports/holdout_retention_queue.csv")
        self.assertEqual(len(s), 12)
        self.assertTrue(np.isfinite(s.hypothetical_net_value_R).all())
        self.assertTrue(np.allclose(
            s.hypothetical_net_value_R,
            s.hypothetical_incremental_contribution_R - s.hypothetical_contact_cost_R
        ))
        self.assertEqual(int(s.customers_contacted.iloc[0]), int(q.priority_top_20pct.astype(str).str.lower().eq("true").sum()))
        bins = pd.read_csv(ROOT / "reports/calibration_bins.csv")
        self.assertEqual(len(bins), 10)
        self.assertTrue(bins.mean_predicted.between(0, 1).all())
        self.assertTrue(bins.observed_churn_rate.between(0, 1).all())


if __name__ == "__main__":
    unittest.main()
