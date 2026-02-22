from __future__ import annotations

import json

from risk_model import evaluate_dict


if __name__ == "__main__":
    sample = {
        "age": 31,
        "monthly_income": 18000,
        "debt_ratio": 0.42,
        "credit_history_months": 48,
        "overdue_count_12m": 1,
        "fraud_flag": False,
    }
    print(json.dumps(evaluate_dict(sample), ensure_ascii=False, indent=2))
