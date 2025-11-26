# CI/CD Setup Guide

This guide explains how to set up continuous integration and deployment for test reports using GitHub Actions and GitHub Pages.

## Overview

The project includes a GitHub Actions workflow that:
1. Runs all unit and integration tests
2. Generates Allure test reports
3. Publishes reports to GitHub Pages
4. Uploads coverage reports as artifacts

## Prerequisites

- GitHub repository with Actions enabled
- Push access to the repository

## Setup Steps

### 1. Enable GitHub Actions

GitHub Actions are enabled by default. If disabled:
1. Go to repository **Settings** → **Actions** → **General**
2. Enable "Allow all actions and reusable workflows"

### 2. Enable GitHub Pages

1. Go to repository **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. Save the settings

### 3. Workflow Configuration

The workflow file `.github/workflows/tests.yml` is already configured. It will:
- Trigger on pushes to `main`, `master`, and `develop` branches
- Run tests on Ubuntu with Python 3.13
- Generate Allure reports
- Deploy to GitHub Pages (only for `main`/`master` branches)

### 4. Viewing Reports

After a successful workflow run:
1. Go to **Actions** tab in your repository
2. Click on the latest workflow run
3. View the deployed report at: `https://<username>.github.io/<repo-name>/`

## Workflow Details

### Triggers

The workflow runs on:
- Push to `main`, `master`, or `develop` branches
- Pull requests to these branches
- Manual trigger via `workflow_dispatch`

### Test Execution

Tests are run with:
- Allure results directory: `allure-results/`
- Coverage reports: `htmlcov/`
- Coverage threshold: 80% (fails if below)

### Artifacts

The following artifacts are uploaded:
- `allure-results`: Raw Allure test results (30 days retention)
- `coverage-report`: HTML coverage report (30 days retention)

### GitHub Pages Deployment

- Only deploys from `main` or `master` branches
- Publishes Allure report to GitHub Pages
- Accessible at: `https://<username>.github.io/<repo-name>/`

## Manual Workflow Trigger

You can manually trigger the workflow:
1. Go to **Actions** tab
2. Select "Run Tests and Publish Allure Reports"
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## Troubleshooting

### Reports Not Appearing

1. Check that GitHub Pages is enabled with "GitHub Actions" as source
2. Verify workflow completed successfully (check Actions tab)
3. Wait a few minutes for Pages deployment
4. Check repository Settings → Pages for deployment status

### Workflow Fails

1. Check workflow logs in Actions tab
2. Verify all dependencies are installed correctly
3. Ensure test environment variables are set (if needed)
4. Check that Playwright browsers are installed

### Coverage Threshold Failures

If coverage drops below 80%, the workflow will fail. To fix:
- Add more tests to increase coverage
- Temporarily lower threshold in `pyproject.toml` (not recommended)
- Review coverage report to identify untested code

## Customization

### Change Coverage Threshold

Edit `pyproject.toml`:
```toml
[tool.pytest.ini_options]
addopts = [
    ...
    "--cov-fail-under=85",  # Change threshold
]
```

### Add More Test Environments

Edit `.github/workflows/tests.yml`:
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.12", "3.13"]
```

### Change Allure Report Location

Edit workflow to change output directory:
```yaml
- name: Generate Allure Report
  run: |
    allure generate allure-results --clean -o custom-report-dir
```

## Best Practices

1. **Review Reports Regularly**: Check Allure reports after each PR
2. **Monitor Coverage**: Keep coverage above threshold
3. **Fix Failing Tests**: Don't ignore test failures
4. **Update Dependencies**: Keep test dependencies up to date
5. **Document Changes**: Update this guide when workflow changes

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Allure Framework Documentation](https://docs.qameta.io/allure/)
- [Pytest Documentation](https://docs.pytest.org/)

