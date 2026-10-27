# Interview talking points

**Tell me about the project.** I analysed a public fictional telecom dataset to connect churn prediction with a real management question: who should receive a retention offer, and when is outreach financially justified? I compared three models using training-only cross-validation and independently tested the winner. The hold-out ROC-AUC was about 0.84, but I also measured calibration, confusion matrix and risk capture.

**What business insight matters most?** A strong model does not automatically imply profitable action. Under one transparent South African cost-and-uplift scenario, contacting the top 20% would lose around R10,000. I would validate incremental uplift through an A/B test before recommending rollout.

**How did you handle correlated features?** I excluded TotalCharges from the primary model because it overlaps with tenure and MonthlyCharges and may not be available at the scoring date. I reported a sensitivity check rather than treating correlated coefficients as causal effects.

**What would you do next?** Time-based validation, a treatment-uplift experiment, fairness review, better customer lifetime value estimates and real contact-cost data.
