# GitHub Actions CI/CD Setup

This project includes comprehensive GitHub Actions workflows for automated testing, building, deployment, and quality checks.

## Workflows Overview

### 1. **tests.yml** - Tests & Build
Runs on every push and pull request to `main` and `develop` branches.

**Jobs:**
- `backend-tests`: Tests Python 3.10, 3.11, 3.12
  - Installs dependencies from `backend/requirements.txt`
  - Runs flake8 linting
  - Executes pytest tests
- `frontend-tests`: Tests Node.js 18.x, 20.x
  - Installs frontend dependencies
  - Builds React app
- `docker-build`: Builds Docker image (uses cache)
- `security-scan`: Trivy vulnerability scanning

**Secrets Required:**
- `GROQ_API_KEY`
- `GITHUB_TOKEN`
- `GOOGLE_API_KEY`

### 2. **deploy.yml** - Deploy to Cloud
Runs automatically on push to `main` branch (can be triggered manually).

**Jobs:**
- `build-and-push`: Builds and pushes Docker image to GitHub Container Registry
- `deploy-aws-ec2`: Deploys to AWS EC2 via SSH
- `deploy-gcp-cloudrun`: Deploys to Google Cloud Run
- `notify-slack`: Sends build status to Slack

**Secrets Required:**
- `AWS_SSH_KEY`: Private SSH key for EC2
- `AWS_EC2_HOST`: EC2 instance hostname
- `AWS_EC2_USER`: SSH user (usually `ec2-user` or `ubuntu`)
- `GCP_SA_KEY`: Google Cloud Service Account JSON key
- `GCP_PROJECT_ID`: Google Cloud Project ID
- `SLACK_WEBHOOK_URL`: Slack incoming webhook

### 3. **benchmark.yml** - Scheduled Benchmarks
Runs on schedule (daily at 2 AM UTC, weekly on Mondays).

**Jobs:**
- Runs daily benchmarks
- Uploads results as GitHub artifacts
- Creates GitHub Release with results
- Posts comment with results

**Secrets Required:**
- `GROQ_API_KEY`
- `GITHUB_TOKEN`
- `GOOGLE_API_KEY`

### 4. **quality.yml** - Code Quality & Lint
Runs on every push/PR to check code quality.

**Jobs:**
- `python-lint`: Black, isort, Flake8, Pylint, mypy
- `javascript-lint`: ESLint, Prettier
- `code-scanning`: GitHub CodeQL analysis
- `dependency-check`: Python safety, npm audit

No additional secrets required.

### 5. **release.yml** - Release & Documentation
Runs when a release is published.

**Jobs:**
- `build-release`: Builds and pushes Docker image with release tag
- `publish-docs`: Publishes documentation to GitHub Pages
- `github-release-notes`: Updates CHANGELOG.md
- `enable-github-pages`: Enables GitHub Pages for the repo

**Secrets Required:**
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub token/password

## Setup Instructions

### 1. Add Repository Secrets

Go to Settings → Secrets and variables → Actions and add:

```
GROQ_API_KEY=<your-key>
GITHUB_TOKEN=<your-token>
GOOGLE_API_KEY=<your-key>
AWS_SSH_KEY=<your-private-key>
AWS_EC2_HOST=<your-ec2-ip>
AWS_EC2_USER=ec2-user
GCP_SA_KEY=<your-service-account-json>
GCP_PROJECT_ID=<your-project-id>
SLACK_WEBHOOK_URL=<your-webhook>
DOCKER_USERNAME=<your-username>
DOCKER_PASSWORD=<your-token>
```

### 2. GitHub Pages Setup

For documentation publishing:
1. Go to Settings → Pages
2. Set Source to `GitHub Actions`
3. Set branch to `main` or `develop`

### 3. Branch Protection

Recommended branch protection rules:
```
Require status checks to pass before merging:
- tests / backend-tests
- tests / frontend-tests
- tests / docker-build
- quality / python-lint
- quality / javascript-lint
```

### 4. Deployment Configuration

**For AWS EC2:**
1. Create SSH key pair
2. Add private key to `AWS_SSH_KEY` secret
3. Configure security groups to allow SSH from GitHub Actions IPs
4. Install Docker and Docker Compose on EC2 instance

**For Google Cloud Run:**
1. Create service account with Cloud Run Admin role
2. Create key and download JSON
3. Add JSON to `GCP_SA_KEY` secret
4. Set project ID in `GCP_PROJECT_ID` secret

## Manual Workflow Triggers

Trigger workflows manually from GitHub Actions tab:

```bash
# Deploy workflow (main branch only)
gh workflow run deploy.yml

# Benchmark workflow
gh workflow run benchmark.yml

# Release workflow
gh workflow run release.yml -f version=1.0.0
```

## Monitoring & Logs

View workflow runs and logs:
1. Go to Actions tab in repository
2. Click on workflow name
3. Click on run to see detailed logs
4. Click on job to see step-by-step output

## Common Issues

### API Key Secrets Not Found
- Ensure secrets are set in repo settings
- Use exact secret names shown in workflow files
- Secrets are case-sensitive

### Deployment Fails
- Check SSH key format (should be PEM)
- Verify EC2 security group allows SSH from GitHub Actions
- Check GCP service account permissions

### Docker Build Fails
- Ensure Docker is installed on EC2
- Check available disk space
- Verify Docker daemon is running

### Tests Fail
- Check Python/Node version compatibility
- Ensure all dependencies are in requirements.txt
- Verify API keys are valid

## Advanced Configuration

### Custom Slack Messages
Modify `notify-slack` job payload in `deploy.yml`

### Run Tests on Schedule
Add cron schedule to `tests.yml`:
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
```

### Skip Deployment
Add skip directive to commit message:
```
[skip ci] commit message
[skip deploy] commit message
```

### Conditional Deployments
Modify `if:` conditions in workflow files:
```yaml
if: github.event_name == 'release'
if: github.ref == 'refs/heads/main'
if: startsWith(github.ref, 'refs/tags/v')
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Security Best Practices](https://docs.github.com/en/actions/security-guides)
- [Docker Build Action](https://github.com/docker/build-push-action)
- [Setup Actions](https://github.com/actions/setup-python)
