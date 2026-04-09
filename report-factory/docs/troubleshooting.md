# Troubleshooting

Common issues and their solutions.

## Installation Issues

### "Skill not found"

**Cause:** Skill not in correct directory

**Solution:**
```bash
# Verify location
ls ~/.claude/skills/report-factory/skill.md

# If not found, reinstall:
git clone https://github.com/your-username/report-factory \
  ~/.claude/skills/report-factory
```

---

## Configuration Issues

### "No domains configured"

**Cause:** First-time use without setup

**Solution:**
```bash
/setup-domains
```

### "Wrong domain detected"

**Cause:** Keywords overlap or insufficient keywords

**Solutions:**
1. **Adjust keywords:**
```bash
/show-domains  # See current keywords
```

Then edit `~/.report-factory/config.json` to add/remove keywords.

2. **Force specific domain:**
```bash
/force-domain EAI https://arxiv.org/abs/2602.xxxxx
```

3. **Reorder priority:**
```bash
# In config.json, reorder priority array:
"priority": ["EAI", "AIH", "MM"]  # EAI now first
```

---

## Processing Issues

### "Card generation failed"

**Common causes:**

1. **Invalid paths:**
```bash
# Check paths in config.json
{
  "paths": {
    "cards": "D:\\003_Resource\\04_Obsidian\\Atomic-card\\Cards\\",
    "index": "D:\\001_Project\\Prj_claudecode\\master_index.json"
  }
}

# Verify directories exist:
ls D:\003_Resource\04_Obsidian\Atomic-card\Cards\
```

2. **Permission denied:**
```bash
# On Windows, check folder permissions
# On Mac/Linux:
chmod 755 /path/to/output/directory
```

3. **Disk space:**
```bash
# Check available space
df -h  # Mac/Linux
dir  # Windows
```

---

### "URL fetch timeout"

**Cause:** Network issues or slow response

**Solutions:**

1. **Increase timeout in config:**
```json
{
  "fetchTimeout": 30000  // 30 seconds
}
```

2. **Check network:**
```bash
# Test connectivity
ping arxiv.org

# Test with curl
curl -I https://arxiv.org/abs/2602.xxxxx
```

3. **Use local PDF:**
```bash
/process /path/to/local/paper.pdf
```

---

### "Duplicate detection not working"

**Cause:** Similarity threshold too high/low

**Solution:**
```json
{
  "similarityThreshold": 0.85  // Adjust between 0.7-0.95
}
```

**Check for duplicates manually:**
```bash
# Search master index
grep "paper title" ~/.report-factory/master_index.json
```

---

## RSS Issues

### "WeChat RSS fetch failed"

**Cause:** Local server not running

**Solution:**
```bash
# Start WeChat MCP server
cd weixin-read-mcp
python server.py

# Verify server is running
curl http://localhost:4000/feeds/all.atom
```

### "arXiv harvest empty"

**Cause:** Current month has no papers yet

**Solution:**
```bash
# Try previous month
/harvest arxiv --month 2026-01
```

### "Inbox.md not found"

**Cause:** Default path doesn't exist

**Solution:**
```json
{
  "paths": {
    "inbox": "D:\\MyDocuments\\Inbox.md"
  }
}
```

---

## Quality Gate Issues

### "Card rejected: low quality"

**Reasons:**
- No quantitative metrics
- Missing source URL
- Title format incorrect
- No technical innovation

**Solutions:**

1. **Check requirements:**
   - Evidence cards need ≥3 metrics
   - Arguments cards need ≥2 evidence links
   - All cards need valid source URL

2. **Manual override:**
```bash
/process https://arxiv.org/abs/2602.xxxxx --force
```

### "Tags validation failed"

**Cause:** Invalid characters in tags

**Solution:**
```markdown
# ❌ Bad
tags: [350tokens/s, Gemini2.5, #Edge]

# ✅ Good
tags: [TokensPerSecond, Gemini2-5, EdgeInference]
```

**Allowed:** Letters, numbers, Chinese, CamelCase
**Not allowed:** `# % . / \ , : * ? " < > |` spaces

---

## Output Issues

### "Canvas not generated"

**Cause:** Canvas output disabled

**Solution:**
```json
{
  "outputFormat": ["card", "canvas", "ppt"]
}
```

### "PPT export failed"

**Cause:** Missing pptx exporter or invalid template

**Solution:**
```bash
# Check exporter exists
ls ~/.claude/skills/report-factory/ppt_exporter.py

# Install dependencies
pip install python-pptx
```

### "Cards not showing in Obsidian"

**Cause:** Path mismatch or file permissions

**Solutions:**

1. **Verify Obsidian vault path:**
```json
{
  "paths": {
    "cards": "D:\\003_Resource\\04_Obsidian\\Atomic-card\\Cards\\"
  }
}
```

2. **Check file exists:**
```bash
ls "D:\003_Resource\04_Obsidian\Atomic-card\Cards\Evidence\"
```

3. **Refresh Obsidian:**
   - Press `Ctrl+R` (Windows) or `Cmd+R` (Mac)
   - Or close and reopen Obsidian

---

## Performance Issues

### "Harvest takes too long"

**Solutions:**

1. **Reduce batch size:**
```bash
/harvest wechat --limit 10
```

2. **Skip quality validation:**
```bash
/harvest wechat --fast
```

3. **Parallel processing:**
```json
{
  "parallelProcessing": true,
  "maxWorkers": 4
}
```

### "Master index too large"

**Cause:** Too many cards indexed

**Solution:**
```bash
# Archive old cards
# In config.json:
{
  "archiveAfterDays": 90,
  "archivePath": "D:\\003_Resource\\04_Obsidian\\Atomic-card\\Archive\\"
}
```

---

## Error Messages Reference

| Error | Meaning | Solution |
|-------|---------|----------|
| `E001` | Config not found | Run `/setup-domains` |
| `E002` | Invalid domain code | Check `/show-domains` |
| `E003` | URL fetch failed | Check network, use local PDF |
| `E004` | Parse error | Check if URL is valid article |
| `E005` | Quality check failed | Review quality requirements |
| `E006` | Duplicate detected | Skip or use `--force` |
| `E007` | Write permission denied | Check folder permissions |
| `E008` | Template not found | Reinstall skill |
| `E009` | RSS fetch failed | Check RSS server status |
| `E010` | Out of disk space | Free up space or change path |

---

## Getting Help

1. **Check logs:**
```bash
# Logs location
~/.report-factory/logs/

# Latest error
tail ~/.report-factory/logs/error.log
```

2. **Verify configuration:**
```bash
# Validate JSON
python -m json.tool ~/.report-factory/config.json
```

3. **Test basic functionality:**
```bash
# Simple test
/process https://arxiv.org/abs/2301.00001
```

4. **Report issues:**
   - Include error message
   - Attach config.json (remove sensitive paths)
   - Describe steps to reproduce
