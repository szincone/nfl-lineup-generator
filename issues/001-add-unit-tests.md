# Add Unit Tests and Testing Infrastructure

## Description
The repository currently lacks any testing infrastructure. Adding comprehensive unit tests would improve code reliability and make it easier for contributors to verify their changes don't break existing functionality.

## Priority
High

## Labels
- testing
- enhancement
- good-first-issue

## Tasks
- [ ] Set up pytest framework
- [ ] Add unit tests for `scrape_fb_ref_off.py`
- [ ] Add unit tests for `scrape_fb_ref_def.py`
- [ ] Add unit tests for `combiner.py`
- [ ] Add unit tests for `lineup_generator.py`
- [ ] Add integration tests for the complete lineup generation flow
- [ ] Set up test data fixtures (mock CSV files, mock web scraping responses)
- [ ] Add GitHub Actions CI/CD pipeline to run tests on PRs
- [ ] Add code coverage reporting

## Acceptance Criteria
- All main functions have unit tests with at least 80% code coverage
- Tests can be run with a simple `pytest` command
- Tests include both positive and negative test cases
- Mock data is used for web scraping to avoid external dependencies in tests
- CI pipeline runs tests automatically on pull requests

## Implementation Notes
- Use `pytest` as the testing framework
- Use `unittest.mock` or `pytest-mock` for mocking external dependencies
- Consider using `responses` library for mocking HTTP requests
- Test edge cases like empty dataframes, missing columns, network failures

## Files to Create/Modify
- `tests/test_scrape_fb_ref_off.py`
- `tests/test_scrape_fb_ref_def.py`
- `tests/test_combiner.py`
- `tests/test_lineup_generator.py`
- `tests/conftest.py` (pytest configuration)
- `tests/fixtures/` (test data)
- `.github/workflows/tests.yml` (GitHub Actions)
- `requirements-dev.txt` (development dependencies)