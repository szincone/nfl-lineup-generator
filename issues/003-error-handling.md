# Add Error Handling and Input Validation

## Description
The codebase lacks proper error handling and input validation, which can lead to crashes when external data sources are unavailable, CSV files are malformed, or environment variables are missing.

## Priority
High

## Labels
- bug
- enhancement
- reliability

## Current Issues
1. No error handling for network requests in scraping modules
2. No validation for required environment variables
3. No handling for empty or malformed CSV files
4. No graceful handling when dataframes are empty after filtering
5. Potential `IndexError` when random selection exceeds available players
6. No validation for DraftKings CSV format

## Tasks
- [ ] Add error handling for network requests in `scrape_fb_ref_off.py` and `scrape_fb_ref_def.py`
- [ ] Add validation for required environment variables (`offense_url`, `defense_url`, `csv`)
- [ ] Add CSV file validation (exists, readable, has required columns)
- [ ] Add dataframe validation after merging and filtering operations
- [ ] Add bounds checking for random player selection
- [ ] Add retry logic for network requests
- [ ] Add logging for better debugging
- [ ] Create custom exception classes for specific error types
- [ ] Add fallback mechanisms when filtering results in empty dataframes

## Implementation Details

### Network Error Handling
```python
import time
from requests.exceptions import RequestException, Timeout, ConnectionError

def fetch_with_retry(url, max_retries=3, timeout=30):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except (RequestException, Timeout, ConnectionError) as e:
            if attempt == max_retries - 1:
                raise ScrapingError(f"Failed to fetch data from {url} after {max_retries} attempts: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Environment Variable Validation
```python
def validate_environment():
    required_vars = ['offense_url', 'defense_url', 'csv']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {missing_vars}")
```

### Dataframe Validation
```python
def validate_dataframe(df, name, required_columns=None):
    if df.empty:
        raise DataValidationError(f"{name} dataframe is empty")
    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            raise DataValidationError(f"{name} missing columns: {missing_cols}")
```

## Acceptance Criteria
- Application handles network failures gracefully
- Clear error messages are provided for all failure scenarios
- Application doesn't crash on malformed input data
- Logging provides useful debugging information
- Retry logic prevents temporary network issues from causing failures
- Empty datasets are handled gracefully with appropriate warnings

## Files to Modify
- `scrape_fb_ref_off.py`
- `scrape_fb_ref_def.py`
- `combiner.py`
- `lineup_generator.py`
- Create `exceptions.py` for custom exception classes
- Create `validators.py` for validation functions
- Update `requirements.txt` to include logging dependencies