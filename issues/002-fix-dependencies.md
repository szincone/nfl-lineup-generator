# Fix Dependency Management and Requirements.txt Format

## Description
The current `requirements.txt` file has an unusual format (numbered list instead of standard pip format) and uses outdated package names. This needs to be fixed for proper dependency management.

## Priority
High

## Labels
- bug
- dependencies
- good-first-issue

## Current Issues
1. `requirements.txt` uses numbered list format instead of standard pip format
2. Uses `bs4` instead of `beautifulsoup4` (correct package name)
3. Uses `dotenv` instead of `python-dotenv` (correct package name)
4. No version pinning, which can lead to compatibility issues
5. Missing development dependencies

## Tasks
- [ ] Fix `requirements.txt` format to standard pip format
- [ ] Update package names to correct PyPI names:
  - `bs4` → `beautifulsoup4`
  - `dotenv` → `python-dotenv`
- [ ] Add version pinning for all dependencies
- [ ] Create `requirements-dev.txt` for development dependencies
- [ ] Test installation with `pip install -r requirements.txt`
- [ ] Update README.md with correct installation instructions
- [ ] Consider adding `setup.py` or `pyproject.toml` for proper package management

## Current requirements.txt
```
1.requests
2.bs4
3.pandas
4.dotenv
```

## Proposed requirements.txt
```
requests>=2.28.0,<3.0.0
beautifulsoup4>=4.11.0,<5.0.0
pandas>=1.4.0,<2.0.0
python-dotenv>=0.19.0,<1.0.0
```

## Acceptance Criteria
- `pip install -r requirements.txt` works without errors
- All imports in the codebase work correctly
- Dependencies are properly version-pinned
- README.md reflects correct installation process
- Development dependencies are separated from production dependencies

## Files to Modify
- `requirements.txt`
- `README.md`
- Create `requirements-dev.txt`