from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')
df['TotalCharges']=pd.to_numeric(df['TotalCharges'],errors='coerce')
df['ChurnFlag']=(df['Churn']=='Yes').astype(int)
df.to_csv(ROOT/'data/processed/telco_customer_churn_clean.csv',index=False)
print('Rows:',len(df),'Missing TotalCharges preserved:',df.TotalCharges.isna().sum())
