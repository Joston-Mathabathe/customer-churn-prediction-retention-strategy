from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split,StratifiedKFold,cross_validate
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score,average_precision_score,confusion_matrix,ConfusionMatrixDisplay,brier_score_loss,precision_score,recall_score,f1_score,RocCurveDisplay,PrecisionRecallDisplay
from sklearn.calibration import calibration_curve

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'reports'; F=ROOT/'visualisations'
df=pd.read_csv(ROOT/'data/processed/telco_customer_churn_clean.csv')
y=df.ChurnFlag
# TotalCharges is approximately tenure × MonthlyCharges; exclude from primary model.
X=df.drop(columns=['customerID','Churn','ChurnFlag','TotalCharges'])
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,stratify=y,random_state=42)
cv=StratifiedKFold(5,shuffle=True,random_state=42)
def make_pipe(est,features):
    cat=[c for c in features if not pd.api.types.is_numeric_dtype(df[c])]
    num=[c for c in features if c not in cat]
    prep=ColumnTransformer([
        ('num',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),num),
        ('cat',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),('onehot',OneHotEncoder(handle_unknown='ignore'))]),cat)])
    return Pipeline([('prep',prep),('model',est)])
models={'Logistic Regression':LogisticRegression(max_iter=2000,random_state=42),
        'Decision Tree':DecisionTreeClassifier(max_depth=5,min_samples_leaf=40,random_state=42),
        'Random Forest':RandomForestClassifier(n_estimators=150,max_depth=10,min_samples_leaf=10,n_jobs=1,random_state=42)}
rows=[]
for name,est in models.items():
    z=cross_validate(make_pipe(est,X.columns),Xtr,ytr,cv=cv,scoring={'auc':'roc_auc','ap':'average_precision'},n_jobs=1)
    rows.append({'model':name,'cv_roc_auc_mean':z['test_auc'].mean(),'cv_roc_auc_std':z['test_auc'].std(),'cv_average_precision_mean':z['test_ap'].mean()})
cvdf=pd.DataFrame(rows).sort_values('cv_roc_auc_mean',ascending=False)
cvdf.to_csv(R/'cross_validation.csv',index=False)
best=cvdf.iloc[0]['model']
model=make_pipe(models[best],X.columns).fit(Xtr,ytr)
prob=model.predict_proba(Xte)[:,1]
pred=(prob>=.5).astype(int)
cm=confusion_matrix(yte,pred)
ConfusionMatrixDisplay(cm,display_labels=['Retained','Churned']).plot(cmap='Blues',values_format='d')
plt.title('Independent hold-out confusion matrix (threshold 0.50)')
plt.tight_layout();plt.savefig(F/'holdout_confusion_matrix.png',dpi=150);plt.close()
obs,mean=calibration_curve(yte,prob,n_bins=10,strategy='quantile')
pd.DataFrame({'mean_predicted':mean,'observed_churn_rate':obs}).to_csv(R/'calibration_bins.csv',index=False)
plt.plot([0,1],[0,1],'k--',label='Perfect');plt.plot(mean,obs,'o-',label='Hold-out')
plt.xlabel('Mean predicted churn probability');plt.ylabel('Observed churn rate')
plt.title('Hold-out calibration (10 quantile bins)');plt.legend()
plt.tight_layout();plt.savefig(F/'holdout_calibration.png',dpi=150);plt.close()
RocCurveDisplay.from_predictions(yte,prob);plt.tight_layout();plt.savefig(F/'holdout_roc_curve.png',dpi=150);plt.close()
PrecisionRecallDisplay.from_predictions(yte,prob);plt.tight_layout();plt.savefig(F/'holdout_precision_recall.png',dpi=150);plt.close()
k=int(np.ceil(.2*len(prob))); top=np.argsort(-prob)[:k]
metrics={'selected_model':best,'test_rows':len(yte),'test_churn_count':int(yte.sum()),
 'holdout_roc_auc':float(roc_auc_score(yte,prob)),
 'holdout_average_precision':float(average_precision_score(yte,prob)),
 'baseline_churn_prevalence':float(yte.mean()),
 'holdout_brier_score':float(brier_score_loss(yte,prob)),
 'threshold':.5,'precision':float(precision_score(yte,pred,zero_division=0)),
 'recall':float(recall_score(yte,pred,zero_division=0)),
 'f1':float(f1_score(yte,pred,zero_division=0)),
 'true_negative':int(cm[0,0]),'false_positive':int(cm[0,1]),
 'false_negative':int(cm[1,0]),'true_positive':int(cm[1,1]),
 'top_20pct_holdout_churn_capture':float(yte.iloc[top].sum()/yte.sum()),
 'top_20pct_holdout_churn_rate':float(yte.iloc[top].mean())}
pd.DataFrame([metrics]).to_csv(R/'model_metrics.csv',index=False)
(R/'model_summary.json').write_text(json.dumps(metrics,indent=2))
scored=df.loc[Xte.index,['customerID','Contract','InternetService','tenure','MonthlyCharges','ChurnFlag']].copy()
scored['churn_probability']=prob
scored['priority_top_20pct']=False
scored.iloc[top,scored.columns.get_loc('priority_top_20pct')]=True
scored.to_csv(R/'holdout_retention_queue.csv',index=False)
# Correlation/availability sensitivity, not part of model selection.
full=df.drop(columns=['customerID','Churn','ChurnFlag'])
smodel=make_pipe(LogisticRegression(max_iter=2000,random_state=42),full.columns).fit(full.loc[Xtr.index],ytr)
pd.DataFrame([{'primary_excludes_TotalCharges':True,
 'selected_model_holdout_auc':metrics['holdout_roc_auc'],
 'logistic_with_TotalCharges_holdout_auc':roc_auc_score(yte,smodel.predict_proba(full.loc[Xte.index])[:,1]),
 'note':'Sensitivity only; correlated variables are not causal drivers'}]).to_csv(R/'correlated_feature_sensitivity.csv',index=False)
print(json.dumps(metrics,indent=2))
