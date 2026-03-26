# Report Factory GitHub 发布指南

## 📦 已创建的文件结构

```
report-factory-github/
├── README.md                      # 项目说明文档
├── LICENSE                        # MIT 许可证
├── requirements.txt               # Python 依赖
├── requirements-dev.txt           # 开发依赖
├── setup.cfg                      # 包配置
├── .gitignore                     # Git 忽略规则
├── config/
│   ├── domain-packs.json          # 预配置领域包（主文件）
│   └── domain-packs/              # 独立领域包文件
│       ├── bio-medical.json
│       └── climate-tech.json
├── scripts/
│   └── setup.py                   # 交互式设置向导
├── templates/
│   ├── evidence.md                # Evidence 卡片模板
│   └── arguments.md               # Arguments 卡片模板
├── examples/
│   ├── cards/                     # 示例卡片
│   │   ├── EAI-E-20260224-01.md
│   │   └── AIH-A-20260224-01.md
│   └── canvas/                    # 示例 Canvas
│       └── sample.canvas
├── .github/
│   └── workflows/
│       └── test.yml               # GitHub Actions CI
└── src/
    └── report_factory/            # Python 包
        ├── __init__.py
        ├── __main__.py            # CLI 入口
        ├── config.py              # 配置管理
        └── detector.py            # 领域检测
```

---

## 🚀 发布步骤

### Step 1: 初始化 Git 仓库

```bash
cd D:\001_Project\Prj_claudecode\report-factory-github

# 初始化 Git
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "Initial release: Report Factory v2.0"
```

### Step 2: 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名：`report-factory`
3. 描述：`Universal Knowledge Card Factory for Obsidian — Transform articles into standardized cards with custom domain detection`
4. 设为 **Public**
5. **不要** 勾选 "Add README"（我们已有）
6. 点击 "Create repository"

### Step 3: 推送代码

```bash
# 关联远程仓库（替换为你的用户名）
git remote add origin https://github.com/hoilex04/report-factory.git

# 推送主分支
git branch -M main
git push -u origin main
```

### Step 4: 完善仓库

#### 4.1 添加 Topics
在 GitHub 仓库页面，点击 "About" 右侧的齿轮，添加：
- `obsidian`
- `knowledge-management`
- `ai`
- `research-tools`
- `markdown`
- `card-generator`

#### 4.2 启用 GitHub Actions
在 Actions 标签页确认 CI workflow 已启用

#### 4.3 添加 Issue 模板（可选）
创建 `.github/ISSUE_TEMPLATE/bug_report.md` 和 `feature_request.md`

---

## 📝 使用前准备

### 1. 替换占位符

占位符已全部替换为 `hoilex04`。

### 2. 测试安装

```bash
# 本地安装测试
pip install -e .

# 测试 CLI
rf --help
rf setup
```

### 3. 更新版本号

发布新版本时更新：
- `src/report_factory/__init__.py`
- `setup.cfg`
- `README.md` badges

---

## 🔄 后续维护

### 发布新版本

```bash
# 更新版本号（所有相关文件）
# 1. src/report_factory/__init__.py: __version__ = "2.0.1"
# 2. setup.cfg: version = 2.0.1

# 打标签
git tag -a v2.0.1 -m "Release version 2.0.1"
git push origin v2.0.1

# 创建 GitHub Release
# 访问 https://github.com/hoilex04/report-factory/releases/new
# 选择标签 v2.0.1，填写发布说明
```

### 添加新领域包

1. 在 `config/domain-packs/` 创建新的 JSON 文件
2. 在 `config/domain-packs.json` 中添加引用
3. 更新 README.md 的领域包列表
4. 提交并推送

### 添加新功能

1. 创建功能分支：`git checkout -b feature/your-feature`
2. 开发并测试
3. 提交：`git commit -m "Add your feature"`
4. 推送：`git push origin feature/your-feature`
5. 在 GitHub 创建 Pull Request

---

## 📊 推广建议

### 1. Obsidian 社区
- 在 Obsidian 论坛发布：https://forum.obsidian.md/
- 提交到 Obsidian 插件列表（如果做插件）

### 2. 社交媒体
- Twitter/X 发布 #Obsidian #AI #KnowledgeManagement
- 知乎、小红书分享使用经验

### 3. 相关社区
- Reddit: r/ObsidianMD, r/PersonalKnowledgeManagement
- 微信公众账号投稿

---

## ⚠️ 注意事项

### 1. 路径依赖
当前代码中仍有硬编码路径（如 `D:\Cards`），需要在发布前：
- 改为使用配置文件中的路径
- 或使用跨平台路径处理

### 2. 功能完整性
当前创建的是**框架文件**，核心功能模块需要补充：
- `fetcher.py` - 内容抓取
- `extractor.py` - 数据提取
- `validator.py` - 质量验证
- `exporter.py` - PPT/Canvas 导出

### 3. 测试覆盖
发布前建议添加单元测试：
```bash
# 创建 tests/ 目录
mkdir tests
# 添加 test_config.py, test_detector.py 等
pytest tests/
```

---

## 🎯 快速发布检查清单

- [ ] 测试 `pip install -e .`
- [ ] 测试 CLI 命令
- [ ] 确认 LICENSE 正确
- [ ] 检查 README 链接
- [ ] 添加 GitHub Actions
- [ ] 设置仓库 Topics
- [ ] 准备 Release Notes

---

## 📬 获取帮助

如果发布过程中遇到问题：
- GitHub Docs: https://docs.github.com/
- Python Packaging: https://packaging.python.org/

祝发布顺利！🎉
