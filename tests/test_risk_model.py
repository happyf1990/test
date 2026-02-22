from risk_model import ApplicantProfile, RiskModel


def test_low_risk_profile_has_better_score():
    model = RiskModel()
    low = ApplicantProfile(
        age=35,
        monthly_income=26000,
        debt_ratio=0.22,
        credit_history_months=72,
        overdue_count_12m=0,
        fraud_flag=False,
    )
    high = ApplicantProfile(
        age=20,
        monthly_income=3500,
        debt_ratio=0.78,
        credit_history_months=3,
        overdue_count_12m=4,
        fraud_flag=True,
    )

    low_result = model.score(low)
    high_result = model.score(high)

    assert low_result.score > high_result.score
    assert low_result.probability_of_default < high_result.probability_of_default


def test_fraud_flag_strong_penalty():
    model = RiskModel()
    base_profile = dict(
        age=30,
        monthly_income=14000,
        debt_ratio=0.4,
        credit_history_months=36,
        overdue_count_12m=0,
    )
    clean = ApplicantProfile(**base_profile, fraud_flag=False)
    fraud = ApplicantProfile(**base_profile, fraud_flag=True)

    clean_result = model.score(clean)
    fraud_result = model.score(fraud)

    assert clean_result.score - fraud_result.score >= 200
    assert "命中反欺诈风险" in fraud_result.reasons
