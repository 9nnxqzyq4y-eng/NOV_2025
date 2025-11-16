# Code Review Standards

## Overview

All code reviews follow the ABACO Financial Intelligence Platform standards aligned with Copilot instructions. CodeRabbit assists with automated review following these standards.

## Review Checklist

### Before Submitting PR

- [ ] Ran `npm run lint` - no errors or warnings
- [ ] Ran `npm run type-check` - all types valid
- [ ] Ran `npm run build` - production build succeeds
- [ ] Reviewed changes: `git diff main`
- [ ] No hardcoded secrets or credentials
- [ ] All functions have return types
- [ ] Error handling implemented
- [ ] Components properly marked `"use client"` if needed

### TypeScript Requirements

- [ ] No `any` types
- [ ] All parameters typed
- [ ] All returns typed
- [ ] Interfaces defined for complex types
- [ ] Strict mode enabled

### React/Next.js Requirements

- [ ] Server Components by default
- [ ] `"use client"` only when needed
- [ ] PascalCase for component names
- [ ] Proper prop types
- [ ] No console warnings

### Security Requirements

- [ ] No hardcoded credentials
- [ ] Environment variables used
- [ ] Input validation implemented
- [ ] RLS policies configured
- [ ] No sensitive data in logs

### Performance Requirements

- [ ] Server Components prioritized
- [ ] Next.js Image component used
- [ ] Suspense boundaries implemented
- [ ] No unnecessary re-renders
- [ ] Bundle impact considered

## CodeRabbit Integration

CodeRabbit will automatically:

1. ✅ Check TypeScript types
1. ✅ Verify security practices
1. ✅ Validate React patterns
1. ✅ Review performance
1. ✅ Suggest improvements

## Feedback Response

When CodeRabbit or human reviewers provide feedback:

1. **Review feedback** - Understand the suggestion
1. **Make changes** - Update your code
1. **Re-run checks** - Verify fixes locally
1. **Push updates** - CodeRabbit will re-review
1. **Resolve conversations** - Mark feedback as addressed

## Approval Requirements

PR requires:

- ✅ All automated checks passing
- ✅ CodeRabbit approval (if configured)
- ✅ At least one human review
- ✅ No merge conflicts
- ✅ All conversations resolved

## References

- [Copilot Instructions](./.github/copilot-instructions.md)
- [CodeRabbit Guide](./CODERABBIT_REVIEW_GUIDE.md)
- [Quality Assurance](./QUALITY_ASSURANCE.md)

