# 🔄 Git Workflow Guide

## 🚀 Getting Started

This project is now under Git version control. Here's how to work with it:

## 📋 Basic Commands

### Check Status
```bash
git status                    # Check current status
git log --oneline            # View commit history
git branch -a                # List all branches
```

### Make Changes
```bash
git add .                    # Stage all changes
git add <filename>           # Stage specific file
git commit -m "Message"      # Commit with message
```

### View Changes
```bash
git diff                     # View unstaged changes
git diff --staged            # View staged changes
git show <commit-hash>       # View specific commit
```

## 🌿 Branching Strategy

### Create Feature Branch
```bash
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature"
git checkout main
git merge feature/new-feature
```

### Create Hotfix Branch
```bash
git checkout -b hotfix/critical-fix
# Fix the issue
git add .
git commit -m "Fix critical issue"
git checkout main
git merge hotfix/critical-fix
```

## 🔄 Daily Workflow

### 1. Start Your Day
```bash
git status                    # Check what you were working on
git log --oneline -5         # Review recent commits
```

### 2. Make Changes
```bash
# Edit files
git add .                    # Stage changes
git commit -m "Descriptive message"
```

### 3. End Your Day
```bash
git push                     # Push to remote (if configured)
git log --oneline -3         # Review today's work
```

## 📝 Commit Message Guidelines

### Format
```
<type>: <description>

[optional body]

[optional footer]
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples
```
feat: add real-time data streaming capability

fix: resolve memory leak in large dataset processing

docs: update API documentation with examples

refactor: optimize acoustic spectrum calculation
```

## 🚫 What NOT to Commit

- **Large data files** (already in .gitignore)
- **Virtual environments** (.venv folder)
- **IDE settings** (.vscode, .idea)
- **OS files** (.DS_Store, Thumbs.db)
- **Log files** (*.log)
- **Temporary files** (*.tmp, *.bak)

## 🔗 Remote Repository Setup

### Add Remote Origin
```bash
git remote add origin <repository-url>
git branch -M main
git push -u origin main
```

### Push Changes
```bash
git push origin main
git push origin <branch-name>
```

### Pull Updates
```bash
git pull origin main
git fetch origin
git merge origin/main
```

## 🆘 Troubleshooting

### Undo Last Commit
```bash
git reset --soft HEAD~1      # Keep changes staged
git reset --hard HEAD~1      # Discard changes completely
```

### Revert File Changes
```bash
git checkout -- <filename>   # Discard unstaged changes
git restore <filename>        # Modern Git command
```

### View File History
```bash
git log --follow <filename>  # See file change history
git blame <filename>         # See who changed what
```

## 📊 Project Structure in Git

```
anomaly_detection/
├── .git/                     # Git repository (hidden)
├── .gitignore               # Git ignore rules
├── .venv/                   # Virtual environment (ignored)
├── data/                    # Data files (ignored)
├── docs/                    # Documentation
├── acoustic_dashboard.py    # Main dashboard
├── requirements.txt         # Dependencies
├── pyproject.toml          # UV configuration
├── run_dashboard.sh        # Launcher script
├── test_dashboard.py       # Test suite
├── README.md               # Project overview
├── DEMO.md                 # Demo guide
└── GIT_WORKFLOW.md        # This file
```

## 🎯 Best Practices

1. **Commit Frequently**: Small, focused commits are better than large ones
2. **Write Clear Messages**: Describe what and why, not how
3. **Use Branches**: Keep main branch stable, work on features in branches
4. **Review Before Committing**: Use `git diff` to review changes
5. **Pull Regularly**: Keep your local repository up to date
6. **Test Before Pushing**: Ensure your code works before sharing

## 🔐 Security Notes

- Never commit sensitive information (API keys, passwords)
- Use environment variables for configuration
- Review `.gitignore` before committing
- Be careful with `git add .` - review what's being staged

---

**Happy Coding! 🎵✨**
