# Report Factory Reviewer

Report Factory 质量评审 Agent —— 苛刻的卡片质检员，确保每张卡片符合输出标准。

## 功能特性

- ✅ **7点质量检查**：准入门槛、标题规范、定量数据、Tags、链接、领域分类、查重
- 📊 **A/B/C分级**：优质/合格/待改进三级分类
- 🔒 **质量门禁**：C级卡片拒绝入库
- 📝 **结构化报告**：JSON格式评审结果，便于下游处理

## 安装

```bash
cp -r report-factory-reviewer ~/.claude/skills/
```

## 使用

### 作为子Agent调用

在 report-factory 中调用：

```markdown
卡片生成完成，调用 report-factory-reviewer 进行质量检查：

```bash
python3 ~/.report-factory/scripts/review_card.py path/to/card.md
```
```

### 独立运行

```bash
# 在 OpenClaw 中
/review_card path/to/card.md
```

## 评审标准

| 检查项 | A级标准 | 权重 |
|--------|---------|------|
| 准入门槛 | 技术创新+定量数据+权威来源 | 20% |
| 标题规范 | `[Topic]: [Insight]` 格式 | 15% |
| 定量数据 | ≥3条带上下文/对比基准 | 25% |
| Tags格式 | 无空格、无特殊字符 | 10% |
| 来源有效性 | 原始URL，非汇总页 | 10% |
| 领域分类 | 关键词匹配正确 | 10% |
| 查重检查 | 相似度<85% | 10% |

## 输出格式

```json
{
  "review_status": "approved",
  "overall_score": 87,
  "grade": "B",
  "checks": {
    "entry_threshold": {"passed": true, "score": 20},
    "quantitative_data": {"passed": true, "score": 23},
    ...
  },
  "issues": []
}
```

## 与 report-factory 的协作

```
report-factory 生成卡片
        ↓
report-factory-reviewer 质量检查
        ↓
  ├─ A级 → 直接入库
  ├─ B级 → 入库+改进建议
  └─ C级 → 拒绝+返回修改
```

## 许可证

MIT License
