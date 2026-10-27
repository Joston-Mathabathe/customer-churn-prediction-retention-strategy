# Business decision analysis — retention planning

## Problem and objective
A retention manager must allocate limited contact capacity to customers who may churn, while ensuring the cost of outreach is justified by **incremental** contribution, not simply predicted churn.

## Who should be investigated?
In the independent hold-out, month-to-month fibre-optic customers show 52.7% observed churn (421 customers); month-to-month DSL customers show 34.0% (250 customers). These are descriptive associations, not causal findings. Investigate contract experience, pricing, service quality and customer feedback before designing offers.

## Score versus action
A churn model ranks risk; it does not predict who will respond to a retention offer. Targeting high-risk customers alone can waste money if customers would leave regardless or would stay without intervention. A controlled trial is needed to estimate **incremental retention uplift**.

## Illustrative South African business case
All R amounts are **invented scenario inputs**, not converted from the dataset's billing values:
- Monthly revenue: **R1,000 per customer**.
- Contribution margin: **30%**.
- Retention horizon: **six months**.
- Outreach/incentive cost: **R150 per customer**.
- Assumed incremental retention uplift among would-be churners: **10%**.
- Contact capacity: top **20%** of the independent hold-out queue (282 customers).

Under those assumptions the estimated incremental contribution is **R32,297**, contact cost **R42,300**, and **net value is approximately -R10,003**. Do not launch on these assumptions. The sensitivity table explores R50–R250 contact cost and 5%–20% assumed uplift. The computation multiplies risk by *assumed* uplift and contribution; it is a decision illustration, not a validated forecast.

## Stakeholders and actions
| Stakeholder | Decision or safeguard |
|---|---|
| Retention operations | Capacity, outreach cadence and customer experience |
| Finance | Verify margin, contact costs and incremental customer lifetime value |
| Marketing | A/B test offers and measure true incremental response |
| Customer service | Investigate service friction and complaints |
| Data science | Validate scores, calibration, temporal drift and subgroup fairness |
| Privacy/compliance | Consent, lawful use and customer opt-out |

## Decision gates
1. Validate model and baseline on a later time period.
2. Run a randomised controlled pilot with hold-out customers to estimate treatment uplift.
3. Estimate real contribution margin, cost, incentive redemption and service burden.
4. Launch only if the **lower-confidence-bound** on incremental value is acceptable.
5. Monitor fairness, complaints, churn outcomes and customer lifetime value.
