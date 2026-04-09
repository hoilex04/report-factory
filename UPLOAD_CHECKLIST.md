# GitHub 上传检查清单

## ✅ 已完成的准备工作

### 1. 敏感信息清理
- [x] 删除所有包含真实邮箱的配置文件
- [x] 删除包含授权码的测试脚本
- [x] 创建 `.gitignore` 排除敏感文件
- [x] 创建 `config.template.json` 作为配置模板

### 2. 文档准备
- [x] 根目录 `README.md` - 项目整体介绍
- [x] `report-factory/README.md` - 主Skill说明
- [x] `report-factory-reviewer/README.md` - 评审Agent说明
- [x] `report-factory-daily-reviewer/README.md` - 日报Agent说明
- [x] `SECURITY.md` - 安全指南

### 3. 安全检查
- [x] 确认没有提交任何含 `password` 的 JSON 文件
- [x] 确认 `.gitignore` 包含 `config.json`
- [x] 确认 `config.template.json` 不含真实凭证

## 📦 上传文件清单

### report-factory/
```
skill.md              - 主Skill定义
README.md             - 使用说明
CHANGELOG.md          - 变更日志
CONTRIBUTING.md       - 贡献指南
docs/                 - 文档目录
examples/             - 示例卡片
prompts/              - Prompt模板
variants/             - 多语言/多场景变体
```

### report-factory-reviewer/
```
skill.md              - 评审Agent定义
README.md             - 使用说明
.gitignore            - 排除敏感文件
```

### report-factory-daily-reviewer/
```
skill.md              - 日报Agent定义
README.md             - 使用说明
SECURITY.md           - 安全指南
config.template.json  - 配置模板
.gitignore            - 排除敏感文件
```

### 根目录
```
README.md             - 项目总览
UPLOAD_CHECKLIST.md   - 本文件
```

## 🚀 上传步骤

### 1. 本地验证

```bash
# 进入 skills 目录
cd .claude/skills

# 验证没有敏感信息
grep -r "password" --include="*.json" .  # 应该无结果
grep -r "XLddq33kwF8yRBxs" .             # 应该无结果
```

### 2. 复制到 GitHub 仓库

```bash
# 假设你的 GitHub 仓库在 ~/github/report-factory
mkdir -p ~/github/report-factory

# 复制三个 Skill
cp -r report-factory ~/github/report-factory/
cp -r report-factory-reviewer ~/github/report-factory/
cp -r report-factory-daily-reviewer ~/github/report-factory/

# 复制根目录文档
cp README.md ~/github/report-factory/
cp UPLOAD_CHECKLIST.md ~/github/report-factory/
```

### 3. Git 提交

```bash
cd ~/github/report-factory

git init
git add .
git commit -m "feat: 初始提交 Report Factory 三件套

- report-factory: 收割+制卡 Agent
- report-factory-reviewer: 单卡质量评审 Agent
- report-factory-daily-reviewer: 日报生成+邮件推送 Agent

包含完整文档、配置模板、安全指南"

git remote add origin https://github.com/hoilex04/report-factory.git
git push -u origin main
```

## 🔒 安全提醒

上传后请立即验证：

1. 在 GitHub 网页上检查是否有任何 `.json` 配置文件包含真实数据
2. 检查 `config.template.json` 中的示例数据是否已被替换为占位符
3. 检查 `SECURITY.md` 是否正确显示

如果发现问题，立即删除并重新提交！

## 📋 开源后维护建议

1. **Issue 模板**：创建 bug 报告和功能请求模板
2. **示例数据**：提供脱敏的示例卡片
3. **版本管理**：使用语义化版本号 (v1.0.0)
4. **更新日志**：记录每次变更

## ✅ 最终确认

上传前请再次确认：

- [ ] 所有配置文件都是模板（含占位符）
- [ ] 所有真实凭证已删除
- [ ] `.gitignore` 正确配置
- [ ] README 文档完整
- [ ] 许可证文件包含（建议添加 LICENSE）

祝上传顺利！🎉
