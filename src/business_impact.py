from pathlib import Path
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
d=pd.read_csv(ROOT/'reports/holdout_retention_queue.csv')
# An explicitly hypothetical policy: contact top 20% of hold-out customers.
# MonthlyCharges is a revenue proxy, NOT contribution margin or lifetime value.
# Assume 6 months of retained revenue, 30% margin, R150 outreach cost,
# and 10% incremental retention uplift among customers who would otherwise churn.
margin=.30;months=6;cost=150;uplift=.10
assumed_monthly_revenue_R=1000  # Illustrative SA case, NOT observed IBM dataset billing
d['six_month_contribution_proxy_R']=assumed_monthly_revenue_R*months*margin
d['assumed_expected_incremental_contribution_R']=d.churn_probability*uplift*d.six_month_contribution_proxy_R
d['assumed_net_per_contact_R']=d.assumed_expected_incremental_contribution_R-cost
selected=d[d.priority_top_20pct].copy()
rows=[]
for contact_cost in [50,100,150,250]:
 for retention_uplift in [.05,.10,.20]:
  gain=(selected.churn_probability*retention_uplift*selected.six_month_contribution_proxy_R).sum()
  rows.append({'contact_cost_R':contact_cost,'assumed_incremental_retention_uplift':retention_uplift,
               'customers_contacted':len(selected),'hypothetical_incremental_contribution_R':gain,
               'hypothetical_contact_cost_R':len(selected)*contact_cost,
               'hypothetical_net_value_R':gain-len(selected)*contact_cost})
pd.DataFrame(rows).to_csv(ROOT/'reports/retention_scenario_sensitivity.csv',index=False)
segments=d.groupby(['Contract','InternetService'],dropna=False).agg(
 customers=('customerID','size'),observed_churn_rate=('ChurnFlag','mean'),
 average_monthly_charges_dataset_units=('MonthlyCharges','mean'),
 average_model_probability=('churn_probability','mean')).reset_index()
segments.to_csv(ROOT/'reports/holdout_segment_opportunities.csv',index=False)
selected.to_csv(ROOT/'reports/holdout_priority_customers.csv',index=False)
print('Scenario sensitivity and segment analysis saved; assumptions are not causal evidence.')
