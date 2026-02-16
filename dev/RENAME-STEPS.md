# GitHub Repo Rename Steps

**Execute these steps now to rename the repository.**

## Step 1: Rename on GitHub

1. Go to: https://github.com/surahli123/DS-Analysis-Review-Agent
2. Click **Settings** (top right)
3. Scroll down to **Repository name**
4. Change: `DS-Analysis-Review-Agent` → `ds-productivity-agents`
5. Click **Rename**

GitHub will automatically redirect old URLs, so nothing breaks.

## Step 2: Update Local Git Remote

Run this in your terminal:

```bash
cd ~/DS-Analysis-Review-Agent
git remote set-url origin https://github.com/surahli123/ds-productivity-agents.git
git remote -v  # Verify the change
```

## Step 3: Rename Local Directory (Optional)

```bash
cd ~
mv DS-Analysis-Review-Agent ds-productivity-agents
cd ds-productivity-agents
```

## Step 4: Update Claude Code Project Path (If Needed)

Claude Code might still reference the old path. If you renamed the local directory:
- Restart Claude Code session
- Or manually update project settings if needed

## Verification

```bash
git remote -v
# Should show: https://github.com/surahli123/ds-productivity-agents.git

git status
# Should work normally
```

---

**After rename:** File reorganization is deferred to v0.5 implementation.
See `dev/migration-plan.md` for the full reorganization plan.
