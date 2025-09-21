# Add Security and Input Sanitization

## Description
The current application lacks proper security measures and input sanitization, which could lead to vulnerabilities when processing user inputs and external data sources.

## Priority
High

## Labels
- security
- vulnerability
- input-validation

## Current Issues
1. No input sanitization for URLs and file paths
2. Potential code injection through CSV data
3. No validation of external data sources
4. Unsafe file operations
5. No protection against malicious CSV content
6. Environment variables not validated for security
7. Web scraping without rate limiting or user agent

## Tasks
- [ ] Add URL validation and sanitization
- [ ] Implement safe file operations with path validation
- [ ] Add CSV content sanitization
- [ ] Validate environment variables for security
- [ ] Add rate limiting for web scraping
- [ ] Implement proper user agent for web requests
- [ ] Add input length limits and type validation
- [ ] Scan for potential code injection vectors
- [ ] Add security headers for any web components
- [ ] Implement secure temporary file handling

## Security Implementation

### URL Validation
```python
import re
from urllib.parse import urlparse
from typing import Optional

class URLValidator:
    # Whitelist of allowed domains for scraping
    ALLOWED_DOMAINS = [
        'www.pro-football-reference.com',
        'pro-football-reference.com',
        'sports-reference.com'
    ]
    
    # Allowed URL schemes
    ALLOWED_SCHEMES = ['http', 'https']
    
    @classmethod
    def validate_url(cls, url: str) -> bool:
        """Validate URL for safety and allowed domains."""
        try:
            parsed = urlparse(url)
            
            # Check scheme
            if parsed.scheme not in cls.ALLOWED_SCHEMES:
                raise ValueError(f"Invalid URL scheme: {parsed.scheme}")
            
            # Check domain whitelist
            if parsed.netloc not in cls.ALLOWED_DOMAINS:
                raise ValueError(f"Domain not allowed: {parsed.netloc}")
            
            # Check for suspicious patterns
            if any(char in url for char in ['<', '>', '"', "'"]):
                raise ValueError("URL contains suspicious characters")
                
            return True
            
        except Exception as e:
            raise ValueError(f"Invalid URL: {e}")
    
    @classmethod
    def sanitize_url(cls, url: str) -> str:
        """Sanitize and validate URL."""
        # Remove whitespace and normalize
        url = url.strip()
        
        # Validate before returning
        cls.validate_url(url)
        return url
```

### File Path Validation
```python
import os
from pathlib import Path

class FileValidator:
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.csv', '.json', '.txt'}
    
    # Maximum file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @classmethod
    def validate_file_path(cls, file_path: str, base_dir: Optional[str] = None) -> Path:
        """Validate file path for security."""
        path = Path(file_path)
        
        # Resolve to absolute path
        if base_dir:
            base_path = Path(base_dir).resolve()
            full_path = (base_path / path).resolve()
            
            # Ensure path is within base directory (prevent directory traversal)
            if not str(full_path).startswith(str(base_path)):
                raise ValueError(f"Path outside allowed directory: {file_path}")
        else:
            full_path = path.resolve()
        
        # Check file extension
        if full_path.suffix.lower() not in cls.ALLOWED_EXTENSIONS:
            raise ValueError(f"File extension not allowed: {full_path.suffix}")
        
        # Check if file exists and is readable
        if full_path.exists():
            if not full_path.is_file():
                raise ValueError(f"Path is not a file: {full_path}")
            
            # Check file size
            if full_path.stat().st_size > cls.MAX_FILE_SIZE:
                raise ValueError(f"File too large: {full_path}")
        
        return full_path
    
    @classmethod
    def safe_file_read(cls, file_path: str, base_dir: Optional[str] = None) -> str:
        """Safely read file content."""
        validated_path = cls.validate_file_path(file_path, base_dir)
        
        try:
            with open(validated_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise IOError(f"Failed to read file {validated_path}: {e}")
```

### CSV Sanitization
```python
import pandas as pd
import re
from typing import List, Dict, Any

class CSVSanitizer:
    # Allowed column names (whitelist)
    ALLOWED_COLUMNS = {
        'Name', 'Position', 'Salary', 'Team', 'AvgPointsPerGame',
        'FantPos', 'Tgt', 'Att', 'Pass_Cmp', 'Pass_Att', 'Pass_Yds',
        'Pass_TD', 'Rush_Att', 'Rush_Yds', 'Rush_TD', 'VBD'
    }
    
    # Maximum allowed values for numeric columns
    NUMERIC_LIMITS = {
        'Salary': (0, 100000),
        'AvgPointsPerGame': (-10, 100),
        'Tgt': (0, 500),
        'Att': (0, 1000),
        'VBD': (-50, 100)
    }
    
    @classmethod
    def sanitize_csv_data(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Sanitize CSV data for security and validity."""
        # Validate column names
        unknown_columns = set(df.columns) - cls.ALLOWED_COLUMNS
        if unknown_columns:
            # Log warning and drop unknown columns
            print(f"Warning: Dropping unknown columns: {unknown_columns}")
            df = df.drop(columns=unknown_columns)
        
        # Sanitize string columns
        string_columns = ['Name', 'Position', 'Team', 'FantPos']
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).apply(cls._sanitize_string)
        
        # Validate numeric columns
        for col, (min_val, max_val) in cls.NUMERIC_LIMITS.items():
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].clip(lower=min_val, upper=max_val)
        
        # Remove rows with suspicious data
        df = cls._remove_suspicious_rows(df)
        
        return df
    
    @classmethod
    def _sanitize_string(cls, value: str) -> str:
        """Sanitize string values."""
        if pd.isna(value) or not isinstance(value, str):
            return ""
        
        # Remove potentially dangerous characters
        value = re.sub(r'[<>"\'\\\x00-\x1f]', '', value)
        
        # Limit length
        value = value[:100]
        
        # Remove leading/trailing whitespace
        return value.strip()
    
    @classmethod
    def _remove_suspicious_rows(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Remove rows with suspicious data patterns."""
        initial_count = len(df)
        
        # Remove rows with suspiciously long names
        if 'Name' in df.columns:
            df = df[df['Name'].str.len() <= 50]
        
        # Remove rows with invalid positions
        if 'Position' in df.columns:
            valid_positions = {'QB', 'RB', 'WR', 'TE', 'DST', 'K'}
            df = df[df['Position'].isin(valid_positions)]
        
        removed_count = initial_count - len(df)
        if removed_count > 0:
            print(f"Warning: Removed {removed_count} suspicious rows")
        
        return df
```

### Environment Variable Validation
```python
import os
import re
from typing import Dict, List

class EnvironmentValidator:
    @classmethod
    def validate_environment(cls) -> Dict[str, Any]:
        """Validate all environment variables."""
        errors = []
        
        # Required variables
        required_vars = ['offense_url', 'defense_url', 'csv']
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                errors.append(f"Missing required environment variable: {var}")
                continue
            
            # Validate specific variables
            if var.endswith('_url'):
                try:
                    URLValidator.validate_url(value)
                except ValueError as e:
                    errors.append(f"Invalid {var}: {e}")
            
            elif var == 'csv':
                try:
                    FileValidator.validate_file_path(value, './csv_files')
                except ValueError as e:
                    errors.append(f"Invalid CSV file: {e}")
        
        if errors:
            raise ValueError(f"Environment validation failed: {'; '.join(errors)}")
        
        return {var: os.getenv(var) for var in required_vars}
```

### Secure Web Scraping
```python
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class SecureScraper:
    def __init__(self, rate_limit_delay=1.0):
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0
        self.session = self._create_session()
    
    def _create_session(self):
        """Create a secure session with proper configuration."""
        session = requests.Session()
        
        # Set a proper user agent
        session.headers.update({
            'User-Agent': 'NFL-Lineup-Generator/1.0 (Educational Research Tool)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def safe_request(self, url: str, timeout: int = 30) -> requests.Response:
        """Make a rate-limited, secure request."""
        # Validate URL first
        URLValidator.validate_url(url)
        
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            self.last_request_time = time.time()
            return response
            
        except requests.exceptions.RequestException as e:
            raise SecurityError(f"Request failed for {url}: {e}")
```

## Acceptance Criteria
- All user inputs are properly validated and sanitized
- File operations are secure against directory traversal attacks
- CSV data is sanitized against potential injection attacks
- URLs are validated against allowed domains only
- Rate limiting prevents abuse of external services
- Environment variables are validated for security
- Error messages don't leak sensitive information
- Security testing covers all input vectors

## Files to Create/Modify
- `security/validators.py` - Input validation classes
- `security/sanitizers.py` - Data sanitization functions
- `security/exceptions.py` - Security-related exceptions
- Update all modules to use secure input handling
- Add security configuration to `config.py`
- Update tests to include security test cases

## Dependencies to Add
- `bleach` - HTML/text sanitization
- `validators` - Additional validation utilities
- `ratelimit` - Rate limiting decorator

## Security Testing
- [ ] Test with malicious URLs
- [ ] Test with malformed CSV files
- [ ] Test directory traversal attempts
- [ ] Test with oversized inputs
- [ ] Test injection attack vectors
- [ ] Verify rate limiting works correctly