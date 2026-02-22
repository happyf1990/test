"""一个简单的风控分析模型。

该模型采用可解释的规则评分 + Sigmoid 概率映射方式，
可以用于贷款、分期等场景的初步风险评估。
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Dict, List


@dataclass
class ApplicantProfile:
    """申请人画像。"""

    age: int
    monthly_income: float
    debt_ratio: float
    credit_history_months: int
    overdue_count_12m: int
    fraud_flag: bool


@dataclass
class RiskResult:
    """模型输出。"""

    score: int
    probability_of_default: float
    level: str
    reasons: List[str]


class RiskModel:
    """风控评分模型。"""

    BASE_SCORE = 600

    def score(self, profile: ApplicantProfile) -> RiskResult:
        score = self.BASE_SCORE
        reasons: List[str] = []

        # 年龄（太小或偏高可能有更高违约波动）
        if profile.age < 22:
            score -= 80
            reasons.append("年龄过低，稳定性较弱")
        elif profile.age <= 30:
            score += 10
        elif profile.age <= 45:
            score += 25
        elif profile.age <= 60:
            score += 5
        else:
            score -= 20
            reasons.append("年龄偏高，长期偿付能力有不确定性")

        # 收入
        if profile.monthly_income < 5000:
            score -= 60
            reasons.append("收入偏低")
        elif profile.monthly_income < 12000:
            score -= 10
        elif profile.monthly_income < 30000:
            score += 20
        else:
            score += 35

        # 负债率
        if profile.debt_ratio > 0.7:
            score -= 120
            reasons.append("负债率过高")
        elif profile.debt_ratio > 0.5:
            score -= 65
            reasons.append("负债率较高")
        elif profile.debt_ratio > 0.35:
            score -= 20
        else:
            score += 20

        # 信贷历史
        if profile.credit_history_months < 6:
            score -= 70
            reasons.append("信贷历史过短")
        elif profile.credit_history_months < 24:
            score -= 15
        elif profile.credit_history_months < 60:
            score += 15
        else:
            score += 30

        # 最近12个月逾期
        if profile.overdue_count_12m >= 3:
            score -= 130
            reasons.append("近12个月逾期次数较多")
        elif profile.overdue_count_12m == 2:
            score -= 70
            reasons.append("近12个月存在多次逾期")
        elif profile.overdue_count_12m == 1:
            score -= 30
            reasons.append("近12个月存在逾期")
        else:
            score += 20

        # 欺诈标签
        if profile.fraud_flag:
            score -= 250
            reasons.append("命中反欺诈风险")
        else:
            score += 10

        score = max(300, min(900, score))
        pd = self._score_to_pd(score)
        level = self._level(score)

        if not reasons:
            reasons.append("画像表现稳健")

        return RiskResult(
            score=score,
            probability_of_default=round(pd, 4),
            level=level,
            reasons=reasons,
        )

    @staticmethod
    def _score_to_pd(score: int) -> float:
        """将评分映射为违约概率（PD）。"""
        # 以 600 分附近作为中性点，分数越高违约概率越低
        x = (600 - score) / 60
        return 1 / (1 + exp(-x))

    @staticmethod
    def _level(score: int) -> str:
        if score >= 760:
            return "A"
        if score >= 690:
            return "B"
        if score >= 620:
            return "C"
        if score >= 540:
            return "D"
        return "E"


def evaluate_dict(payload: Dict) -> Dict:
    """便于与 API/脚本集成的字典输入输出函数。"""
    profile = ApplicantProfile(**payload)
    result = RiskModel().score(profile)
    return {
        "score": result.score,
        "probability_of_default": result.probability_of_default,
        "level": result.level,
        "reasons": result.reasons,
    }
