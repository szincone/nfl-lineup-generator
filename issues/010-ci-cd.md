# Add Continuous Integration and GitHub Actions

## Description
The repository lacks continuous integration (CI) setup, which means code quality, tests, and security checks are not automatically verified on pull requests and commits.

## Priority
Medium

## Labels
- ci-cd
- automation
- quality-assurance

## Current Issues
1. No automated testing on pull requests
2. No code quality checks
3. No security scanning
4. No dependency vulnerability checking
5. No automated formatting checks
6. No release automation
7. No cross-platform testing

## Tasks
- [ ] Set up GitHub Actions workflows
- [ ] Add automated testing workflow
- [ ] Add code quality and linting checks
- [ ] Add security scanning (CodeQL, Dependabot)
- [ ] Add dependency vulnerability scanning
- [ ] Add cross-platform testing (Windows, macOS, Linux)
- [ ] Add automated code formatting checks
- [ ] Set up automated releases
- [ ] Add test coverage reporting
- [ ] Add performance regression testing

## Implementation

### Main CI Workflow (`.github/workflows/ci.yml`)
```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    name: Test Python ${{ matrix.python-version }} on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macOS-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11']
        exclude:
          # Reduce matrix size for faster builds
          - os: windows-latest
            python-version: '3.8'
          - os: macOS-latest
            python-version: '3.8'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        flake8 nfl_lineup tests --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 nfl_lineup tests --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics
    
    - name: Run type checking
      run: mypy nfl_lineup
    
    - name: Run security checks
      run: bandit -r nfl_lineup -f json -o bandit-report.json
    
    - name: Run tests with coverage
      run: |
        pytest --cov=nfl_lineup --cov-report=xml --cov-report=term-missing
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  lint:
    name: Code Quality
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install black isort flake8 mypy bandit
    
    - name: Check code formatting with Black
      run: black --check --diff nfl_lineup tests
    
    - name: Check import sorting with isort
      run: isort --check-only --diff nfl_lineup tests
    
    - name: Lint with flake8
      run: flake8 nfl_lineup tests
    
    - name: Type checking with mypy
      run: mypy nfl_lineup
    
    - name: Security check with bandit
      run: bandit -r nfl_lineup

  dependency-check:
    name: Dependency Security Scan
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Safety check
      uses: pyupio/safety@v2
      with:
        api-key: ${{ secrets.SAFETY_API_KEY }}
        
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
        
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
```

### Code Quality Workflow (`.github/workflows/code-quality.yml`)
```yaml
name: Code Quality

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    name: Code Quality Analysis
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Needed for SonarCloud
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests with coverage
      run: pytest --cov=nfl_lineup --cov-report=xml
    
    - name: SonarCloud Scan
      uses: SonarSource/sonarcloud-github-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Security Scanning Workflow (`.github/workflows/security.yml`)
```yaml
name: Security

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Mondays

jobs:
  codeql:
    name: CodeQL Analysis
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        language: [ 'python' ]
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Initialize CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: ${{ matrix.language }}
    
    - name: Autobuild
      uses: github/codeql-action/autobuild@v2
    
    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v2

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install bandit[toml] safety
    
    - name: Run Bandit security scan
      run: |
        bandit -r nfl_lineup -f json -o bandit-report.json
        
    - name: Run Safety dependency scan
      run: safety check --json --output safety-report.json
      continue-on-error: true
    
    - name: Upload security scan results
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json
```

### Release Workflow (`.github/workflows/release.yml`)
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Generate changelog
      id: changelog
      run: |
        echo "CHANGELOG<<EOF" >> $GITHUB_OUTPUT
        git log --pretty=format:"- %s" $(git describe --tags --abbrev=0 HEAD^)..HEAD >> $GITHUB_OUTPUT
        echo "EOF" >> $GITHUB_OUTPUT
    
    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        body: |
          Changes in this release:
          ${{ steps.changelog.outputs.CHANGELOG }}
        draft: false
        prerelease: false
    
    - name: Publish to TestPyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.TEST_PYPI_API_TOKEN }}
      run: twine upload --repository testpypi dist/*
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

### Dependabot Configuration (`.github/dependabot.yml`)
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "szincone"
    assignees:
      - "szincone"
    commit-message:
      prefix: "deps"
      include: "scope"
  
  - package-ecosystem: "github-actions"
    directory: "/.github/workflows"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "ci"
```

### Configuration Files

#### `.github/PULL_REQUEST_TEMPLATE.md`
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

#### `pyproject.toml` (for tool configuration)
```toml
[tool.black]
line-length = 100
target-version = ['py38']
include = '\.pyi?$'

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.coverage.run]
source = ["nfl_lineup"]
omit = ["tests/*", "setup.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]

[tool.bandit]
exclude_dirs = ["tests"]
skips = ["B101"]  # Skip assert_used test
```

## Acceptance Criteria
- All tests run automatically on PRs and pushes
- Code quality checks prevent poor code from being merged
- Security scans identify vulnerabilities early
- Cross-platform compatibility is verified
- Dependencies are automatically updated
- Releases are automated with proper versioning
- Test coverage is tracked and reported
- Documentation is automatically checked

## Files to Create
- `.github/workflows/ci.yml`
- `.github/workflows/code-quality.yml`
- `.github/workflows/security.yml`
- `.github/workflows/release.yml`
- `.github/dependabot.yml`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `pyproject.toml`
- `sonar-project.properties`

## Dependencies to Add (requirements-dev.txt)
- `pytest>=7.0.0`
- `pytest-cov>=4.0.0`
- `black>=22.0.0`
- `isort>=5.10.0`
- `flake8>=5.0.0`
- `mypy>=0.991`
- `bandit>=1.7.0`
- `safety>=2.0.0`

## Repository Settings
- Enable branch protection for main branch
- Require PR reviews
- Require status checks to pass
- Enable Dependabot alerts
- Enable CodeQL scanning