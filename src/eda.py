from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
d=pd.read_csv(root/'data/processed/telco_customer_churn_clean.csv')
for col,file in [('Contract','churn_by_contract.png'),('InternetService','churn_by_internet_service.png'),('PaymentMethod','churn_by_payment_method.png')]:
 t=d.groupby(col).ChurnFlag.agg(['mean','size']).reset_index()
 t.columns=[col,'churn_rate','customer_count']
 t.to_csv(root/'reports'/('churn_by_'+col.lower()+'.csv'),index=False)
 ax=t.plot.bar(x=col,y='churn_rate',legend=False,title='Churn rate by '+col)
 ax.set_ylabel('Observed churn rate')
 plt.tight_layout();plt.savefig(root/'visualisations'/file,dpi=150);plt.close()
d['tenure_group']=pd.cut(d.tenure,bins=[-1,12,24,48,72],labels=['0-12','13-24','25-48','49-72'])
d.groupby('tenure_group',observed=True).ChurnFlag.agg(['mean','size']).to_csv(root/'reports/churn_by_tenure_group.csv')
d.groupby('tenure_group',observed=True).ChurnFlag.mean().plot.bar(title='Churn by tenure')
plt.ylabel('Observed churn rate');plt.tight_layout()
plt.savefig(root/'visualisations/churn_by_tenure.png',dpi=150);plt.close()
pd.DataFrame([{'customers':len(d),'churn_rate':d.ChurnFlag.mean(),'average_monthly_charges_dataset_units':d.MonthlyCharges.mean()}]).to_csv(root/'reports/overall_kpis.csv',index=False)
