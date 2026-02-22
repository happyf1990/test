# 风控分析模型示例

这是一个可解释的基础风控模型，适用于贷款/分期申请场景的快速评估。

## 模型思路

- 使用规则评分卡，对申请人多个维度打分：
  - 年龄
  - 月收入
  - 负债率
  - 信贷历史长度
  - 近 12 个月逾期次数
  - 反欺诈命中标签
- 最终输出：
  - `score`：风险评分（300~900）
  - `probability_of_default`：违约概率（PD）
  - `level`：风险等级（A~E）
  - `reasons`：关键风险原因，便于解释

## 目录结构

- `src/risk_model.py`：核心模型实现（Python）
- `src/main.py`：命令行演示脚本
- `web/index.html`：前端评估页面（浏览器中输入信息并实时返回违约概率）
- `tests/test_risk_model.py`：单元测试
- `data/sample_applicants.json`：样例输入数据

## 运行示例（Python）

```bash
python3 src/main.py
```

## 启动前端页面

```bash
python3 -m http.server 8000
```

然后浏览器访问：`http://localhost:8000/web/`

## 运行测试

```bash
PYTHONPATH=src pytest -q
```

## 与 API 集成

模型提供 `evaluate_dict(payload)` 方法，可直接接收字典并返回结构化结果，便于对接 Web API 或工作流系统。
