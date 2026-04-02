# 安全指南

## ⚠️ 敏感信息警告

本 Skill 需要邮箱授权码/应用密码来发送邮件，这些信息**非常敏感**，请勿泄露！

## 安全措施

### 1. 配置文件排除

本仓库已配置 `.gitignore`，以下文件不会被提交：

```
daily-reviewer-config.json
email-config.json
config.json
*.log
```

### 2. 配置模板使用

我们提供了 `config.template.json` 作为配置模板，**不含任何真实凭证**。

用户需要：
1. 复制模板为 `config.json`
2. 填入自己的配置
3. 确保 `config.json` 不被提交

### 3. 验证是否泄露

提交前运行以下命令检查：

```bash
# 检查是否包含密码模式
grep -r "password.*:" --include="*.json" --include="*.py" .
grep -r "smtp.*password" --include="*.json" --include="*.py" .

# 检查是否包含邮箱授权码格式（通常是16位字母数字）
grep -rE "[a-zA-Z0-9]{16}" --include="*.json" --include="*.md" .
```

### 4. GitHub 提交前检查清单

- [ ] `config.json` 已添加到 `.gitignore`
- [ ] 没有提交任何含 `password` 字段的 JSON 文件
- [ ] 没有提交日志文件 (`.log`)
- [ ] 只提交了 `config.template.json`（模板）
- [ ] README 中已说明如何配置（使用模板）

## 如果意外泄露了敏感信息

1. **立即撤销凭证**：
   - Gmail：撤销应用专用密码
   - 163/QQ：重置授权码

2. **从 Git 历史中移除**（如果已提交）：
   ```bash
   git filter-branch --force --index-filter \
   'git rm --cached --ignore-unmatch path/to/config.json' \
   --prune-empty --tag-name-filter cat -- --all
   ```

3. **强制推送**（谨慎操作）：
   ```bash
   git push origin --force --all
   ```

4. **通知用户**：如果是公开仓库，需要通知可能受影响的用户

## 推荐的安全实践

1. **使用环境变量**（高级）：
   ```python
   import os
   password = os.environ.get('RF_EMAIL_PASSWORD')
   ```

2. **使用密钥管理服务**（企业级）：
   - AWS Secrets Manager
   - Azure Key Vault
   - HashiCorp Vault

3. **定期轮换凭证**：
   - 每 3-6 个月更换一次授权码
   - 监控邮箱登录异常
