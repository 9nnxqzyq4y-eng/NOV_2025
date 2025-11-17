# CodeRabbit Usage Guide

## 🐰 What is CodeRabbit?

CodeRabbit is an AI-powered code review assistant that automatically reviews your pull requests, providing:

- Security vulnerability detection
- Code quality suggestions
- Best practice recommendations
- TypeScript type safety checks
- Performance optimization tips

## ✅ Setup Complete

CodeRabbit is now fully configured for the ABT repository with:

✅ **Assertive review profile** - Thorough, detailed reviews
✅ **Request changes workflow** - Can block PRs with critical issues
✅ **Auto-review enabled** - Automatically reviews all new PRs
✅ **Multiple linting tools** - ESLint, Ruff, ShellCheck, Markdownlint, etc.
✅ **Path filters** - Ignores node_modules, build artifacts
✅ **Knowledge base** - Learns from your codebase over time

## 📝 How to Use CodeRabbit

### Method 1: Automatic Reviews (Default)

CodeRabbit will **automatically review** every pull request you create. No action needed!

### Method 2: Manual Review Request

Comment on any PR with:

```bash
@coderabbit review

### Method 3: Ask Questions

You can ask CodeRabbit questions about your code:

@coderabbit explain this function
@coderabbit how can I improve this code?
@coderabbit is this secure?

### Method 4: Request Specific Reviews

@coderabbit review security
@coderabbit review performance
@coderabbit review typescript

## 🎯 Common Commands

| Command                     | Description                   |
| --------------------------- | ----------------------------- |
| `@coderabbit review`        | Full code review              |
| `@coderabbit review --full` | Force full re-review          |
| `@coderabbit pause`         | Pause reviews on this PR      |
| `@coderabbit resume`        | Resume reviews                |
| `@coderabbit resolve`       | Mark conversation as resolved |
| `@coderabbit help`          | Show all available commands   |

## 📊 What CodeRabbit Reviews

### 1. **Security** 🔒

- Hardcoded secrets/credentials
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure dependencies
- Missing input validation

### 2. **Code Quality** ✨

- TypeScript strict mode compliance
- Type annotations
- Unused variables/imports
- Code complexity
- Naming conventions

### 3. **Best Practices** 📚

- React/Next.js patterns
- Server vs Client components
- Performance optimization
- Error handling
- Accessibility

### 4. **Testing** 🧪

- Test coverage
- Test quality
- Missing test cases
- Mock usage

### 5. **Documentation** 📖

- Missing comments
- Outdated docs
- README completeness

## 🚀 Getting Reviews on Commits

CodeRabbit reviews **Pull Requests**, not direct commits to main. To get a review:

1. **Create a feature branch:**

   ```bash
   git checkout -b feature/my-new-feature

1. **Make your changes and commit:**

   git add .
   git commit -m "feat: add new feature"
   git push origin feature/my-new-feature

1. **Create a Pull Request on GitHub:**
   - Go to https://github.com/JenineferDeras/ABT/pulls
   - Click "New pull request"
   - Select your branch
   - CodeRabbit will automatically review!

## 📋 Review Request File

We've created `.github/CODERABBIT_REQUEST.md` that documents what to ask CodeRabbit to review. You can reference this in PR descriptions:

```markdown
@coderabbit please review following the guidelines in .github/CODERABBIT_REQUEST.md

## 🔧 Configuration

CodeRabbit is configured via `.coderabbit.yaml`:

```yaml
reviews:
  profile: assertive # Thorough reviews
  auto_review:
    enabled: true # Auto-review all PRs
  tools:
    eslint: enabled # JS/TS linting
    ruff: enabled # Python linting
    shellcheck: enabled # Shell script linting
    markdownlint: enabled # Markdown linting
    github-actions: enabled # Workflow linting

## ⚙️ Customization

### Ignore Specific Files

Add to `.coderabbit.yaml`:

  path_filters:
    - '!**/test/**'
    - '!**/*.test.ts'

### Change Review Style

  profile: chill      # Fewer comments
  # or
  profile: assertive  # More thorough (current)

## 💡 Pro Tips

1. **Tag CodeRabbit in comments** to ask questions about specific code sections
1. **Use `@coderabbit generate` commands** to auto-generate tests or documentation
1. **Review CodeRabbit's suggestions** - they're usually spot-on but not always applicable
1. **Close PR #1** - It contains outdated code and will confuse CodeRabbit

## 📞 Support

- CodeRabbit Docs: https://docs.coderabbit.ai
- Repository Issues: https://github.com/JenineferDeras/ABT/issues
- Configuration: `.coderabbit.yaml`

## 🎉 Next Steps

1. ✅ CodeRabbit is configured and ready
1. ✅ Create a test PR to see CodeRabbit in action
1. ✅ Review the existing PR #1 or close it
1. ✅ Enjoy automated code reviews!


**Last Updated:** November 9, 2025
**Configuration:** `.coderabbit.yaml`
**Review Request Template:** `.github/CODERABBIT_REQUEST.md`

