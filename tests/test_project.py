import unittest,json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
class ChurnProjectTests(unittest.TestCase):
 def test_data_size_and_target(self):
  d=pd.read_csv(ROOT/'data/processed/telco_customer_churn_clean.csv')
  self.assertEqual(len(d),7043)
  self.assertEqual(int(d.ChurnFlag.sum()),1869)
 def test_missingness_preserved(self):
  d=pd.read_csv(ROOT/'data/processed/telco_customer_churn_clean.csv')
  self.assertEqual(int(d.TotalCharges.isna().sum()),11)
 def test_holdout_and_cv(self):
  m=json.loads((ROOT/'reports/model_summary.json').read_text())
  self.assertEqual(m['test_rows'],1409)
  self.assertGreater(m['holdout_roc_auc'],.7)
  self.assertEqual(len(pd.read_csv(ROOT/'reports/cross_validation.csv')),3)
 def test_scenario_and_calibration(self):
  s=pd.read_csv(ROOT/'reports/retention_scenario_sensitivity.csv')
  self.assertEqual(len(s),12)
  self.assertTrue(s.hypothetical_net_value_R.notna().all())
  self.assertEqual(len(pd.read_csv(ROOT/'reports/calibration_bins.csv')),10)
if __name__=='__main__': unittest.main()
