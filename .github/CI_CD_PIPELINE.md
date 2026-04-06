# CI/CD Pipeline Overview

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
           ┌────▼───┐    ┌────▼───┐   ┌────▼───┐
           │  Push  │    │   PR   │   │Release │
           └────┬───┘    └────┬───┘   └────┬───┘
                │             │             │
    ┌───────────┴─────────────┴──────────┐  │
    │                                    │  │
┌───▼─────────────────────────────────┐ │  │
│ tests.yml (Tests & Build)           │ │  │
├─────────────────────────────────────┤ │  │
│ • Backend tests (Python 3.10-3.12)  │ │  │
│ • Frontend tests (Node 18-20)        │ │  │
│ • Docker build                       │ │  │
│ • Security scan (Trivy)              │ │  │
└───┬─────────────────────────────────┘ │  │
    │                                   │  │
┌───▼──────────────────────────────────┐│  │
│ quality.yml (Code Quality)           ││  │
├──────────────────────────────────────┤│  │
│ • Python lint (Black, Pylint, mypy)  ││  │
│ • JS lint (ESLint, Prettier)         ││  │
│ • CodeQL analysis                    ││  │
│ • Dependency check                   ││  │
└───┬──────────────────────────────────┘│  │
    │                                   │  │
    └───────────────┬───────────────────┘  │
                    │                       │
              ✅ All checks pass?           │
                    │                       │
         ┌──────────┴──────────┐           │
         │ (main branch)        │ (Release)
    ┌────▼──────────┐       ┌──┴──────────────┐
    │ deploy.yml    │       │ release.yml     │
    │ (Auto deploy) │       │ (Manual)        │
    └────┬──────────┘       └──┬──────────────┘
         │                      │
    ┌────┴──────────────────────┴───┐
    │                               │
┌───▼──────────┐          ┌────────▼────────┐
│ Docker Build │          │ GitHub Pages    │
│ & Push       │          │ (Docs)          │
└───┬──────────┘          └─────────────────┘
    │
    ├─► AWS EC2 Deployment (SSH)
    ├─► GCP Cloud Run (gcloud CLI)
    └─► Docker Registry (Docker Hub/GHCR)

Daily Cron:
    ↓
┌──────────────────────────┐
│ benchmark.yml            │
├──────────────────────────┤
│ • Run benchmarks daily   │
│ • Upload artifacts       │
│ • Create releases        │
└──────────────────────────┘
```

## Workflow States

### Pull Request → Merge
```
1. PR Created
   ├─ tests.yml runs → ✓ Pass required
   └─ quality.yml runs → ✓ Pass required

2. Approval Required
   └─ 1+ reviewer approval

3. Merge to main
   └─ All checks still passing

4. Branch Protection Active
   └─ Cannot merge without passing checks
```

### Push to main
```
1. All tests pass
2. Deploy to production
   ├─ Build Docker image
   ├─ Push to AWS EC2
   ├─ Push to GCP Cloud Run
   └─ Notify Slack
```

### Release Published
```
1. Create semantic version tag (v1.0.0)
2. GitHub Release created
3. release.yml triggered
   ├─ Build tagged Docker image
   ├─ Publish documentation
   ├─ Update CHANGELOG.md
   └─ Push to Docker Hub
```

### Daily (Scheduled)
```
Every day at 2 AM UTC:
   ├─ benchmark.yml runs
   ├─ Benchmarks execute
   ├─ Results uploaded
   └─ GitHub comments created

Every Monday at 2 AM UTC:
   └─ Full benchmark suite runs
```

## Dependency Management

### Automated Updates (Dependabot)
- **Weekly** on Mondays at 3 AM UTC
- Different PRs for:
  - Python production dependencies
  - Frontend npm dependencies
  - GitHub Actions
- Auto-labels: `dependencies`, `python`, `javascript`
- Requires review before merge

### Manual Updates
```bash
# Update all Python dependencies
pip install --upgrade -r backend/requirements.txt

# Update all npm dependencies
cd frontend && npm update

# Check for security vulnerabilities
safety check --file backend/requirements.txt
npm audit
```

## Security Workflow

```
┌──────────────────────────────────────┐
│ Source Code Changes                  │
└─────────────┬──────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼──────────┐   ┌───▼──────────────┐
│CodeQL        │   │Trivy             │
│Static Analysis   │Vulnerability     │
│(SAST)        │   │Scanning (OSINT)  │
└───┬──────────┘   └───┬──────────────┘
    │                   │
    └─────────┬─────────┘
              │
         ┌────▼───────┐
         │ SARIF Report
         └────┬───────┘
              │
    ┌─────────▼──────────┐
    │GitHub Security Tab │
    │ (Alerts)           │
    └────────────────────┘
```

## Deployment Pipeline

### Development
```
Feature Branch → PR → Tests → Review → Merge to develop
```

### Staging
```
develop branch → Manual trigger → Test on staging
```

### Production
```
main branch → Auto-trigger → Deploy
              • AWS EC2 (SSH)
              • GCP Cloud Run
              • Docker Registry
```

## Notifications

### Slack Integration
```
Posts to Slack:
├─ Deploy status (success/failure)
├─ Build number
├─ Commit reference
├─ Timestamp
└─ Deployment target
```

### GitHub Notifications
```
├─ PR Status Checks
├─ Branch protection status
├─ Release published notifications
└─ Issues/Comments on PRs
```

## Performance Metrics

### Build Times (Approximate)
- Backend tests: 3-5 minutes
- Frontend build: 2-3 minutes
- Docker build: 5-10 minutes
- Total pipeline: 15-20 minutes

### Optimization Tips
1. **Use Cache**
   - pip cache: `cache: 'pip'`
   - npm cache: `cache: 'npm'`
   - Docker cache: `cache-from: type=gha`

2. **Parallel Jobs**
   - Backend and frontend tests run in parallel
   - Reduces total time

3. **Conditional Runs**
   - Skip deploy if tests fail
   - Skip docs if no changes to docs/

## Troubleshooting

### Workflow Not Triggering
- Check branch name matches trigger
- Verify secrets are set
- Check file path filters

### Deployment Fails
- Check AWS/GCP credentials
- Verify EC2/Cloud Run instance running
- Check firewall/security groups

### Tests Pass Locally but Fail in CI
- Different Python/Node version
- Missing environment variable
- Missing secret
- Cache issues

## Best Practices

1. **Commit Messages**
   ```
   [skip ci] - Skip all workflows
   [skip deploy] - Skip deployment only
   ```

2. **Pull Requests**
   - Always run tests first
   - One feature per PR
   - Keep PRs small and focused

3. **Secrets Management**
   - Use GitHub Secrets, not .env files
   - Rotate credentials regularly
   - Use service accounts where possible

4. **Monitoring**
   - Enable branch protection
   - Require status checks
   - Require approval before merge
   - Review workflow logs regularly

## Related Documentation

- [Workflows Configuration](./workflows/)
- [GitHub Actions Setup Guide](./GITHUB_ACTIONS.md)
- [Deployment Guide](../README.md#deployment)
- [Quick Start](../QUICKSTART.md)
