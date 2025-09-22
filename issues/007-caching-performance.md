# Add Data Caching and Performance Optimization

## Description
The application currently scrapes data from external websites every time it runs, which is slow and puts unnecessary load on external servers. Adding caching and performance optimizations would improve user experience and reduce external dependencies.

## Priority
Medium

## Labels
- performance
- enhancement
- caching

## Current Issues
1. Web scraping happens on every run, even if data hasn't changed
2. No caching mechanism for scraped data
3. No way to work offline with cached data
4. Slow startup time due to web scraping
5. No data freshness indicators
6. Inefficient pandas operations that could be optimized

## Tasks
- [ ] Implement file-based caching for scraped data
- [ ] Add cache expiration and freshness checking
- [ ] Add option to work offline with cached data
- [ ] Optimize pandas operations for better performance
- [ ] Add progress indicators for long-running operations
- [ ] Implement parallel processing for multiple lineup generation
- [ ] Add memory usage optimization
- [ ] Create cache management commands

## Implementation Details

### Caching System
```python
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

class DataCache:
    def __init__(self, cache_dir='./cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_key(self, url):
        """Generate cache key from URL."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def is_cache_valid(self, cache_file, max_age_hours=24):
        """Check if cache file is still valid."""
        if not cache_file.exists():
            return False
        
        file_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        return file_age < timedelta(hours=max_age_hours)
    
    def get_cached_data(self, url, max_age_hours=24):
        """Get cached data if valid, otherwise return None."""
        cache_key = self.get_cache_key(url)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if self.is_cache_valid(cache_file, max_age_hours):
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None
    
    def cache_data(self, url, data):
        """Cache data to file."""
        cache_key = self.get_cache_key(url)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def clear_cache(self):
        """Clear all cached data."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
```

### Enhanced Scraper with Caching
```python
class CachedScraper:
    def __init__(self, cache_dir='./cache', cache_hours=24):
        self.cache = DataCache(cache_dir)
        self.cache_hours = cache_hours
    
    def scrape_with_cache(self, url, force_refresh=False):
        """Scrape data with caching support."""
        if not force_refresh:
            cached_data = self.cache.get_cached_data(url, self.cache_hours)
            if cached_data:
                print(f"Using cached data for {url}")
                return pd.DataFrame(cached_data)
        
        print(f"Fetching fresh data from {url}")
        df = self._scrape_url(url)
        
        # Cache the data
        self.cache.cache_data(url, df.to_dict('records'))
        return df
    
    def _scrape_url(self, url):
        """
        Placeholder for the actual scraping implementation.

        Args:
            url (str): The URL to scrape data from.

        Returns:
            pandas.DataFrame: A DataFrame containing the scraped data.

        This method should be implemented to fetch and parse data from the given URL,
        returning the results as a pandas DataFrame. Override this method with the
        actual scraping logic as appropriate for your application.
        """
        # Existing scraping logic should be implemented here.
        pass
```

### Performance Optimized Operations
```python
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import numpy as np

class PerformanceOptimizer:
    @staticmethod
    def optimize_dataframe_operations(df):
        """Optimize common dataframe operations."""
        # Use categorical data for string columns with limited values
        categorical_columns = ['Position', 'Team', 'FantPos']
        for col in categorical_columns:
            if col in df.columns:
                df[col] = df[col].astype('category')
        
        # Convert object columns to appropriate numeric types
        numeric_columns = ['Salary', 'AvgPointsPerGame', 'VBD']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    @staticmethod
    def parallel_lineup_generation(players_df, num_lineups, strategy='value'):
        """Generate multiple lineups in parallel."""
        num_processes = min(mp.cpu_count(), num_lineups)
        lineups_per_process = num_lineups // num_processes
        
        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = []
            for i in range(num_processes):
                count = lineups_per_process + (1 if i < num_lineups % num_processes else 0)
                future = executor.submit(generate_lineups_batch, players_df, count, strategy)
                futures.append(future)
            
            lineups = []
            for future in futures:
                lineups.extend(future.result())
        
        return lineups
```

### Progress Indicators
```python
from tqdm import tqdm
import time

class ProgressTracker:
    def __init__(self, description="Processing"):
        self.description = description
    
    def track_scraping(self, urls):
        """Track progress during scraping operations."""
        results = []
        for url in tqdm(urls, desc="Scraping data"):
            result = scrape_url(url)
            results.append(result)
            time.sleep(0.1)  # Be nice to servers
        return results
    
    def track_lineup_generation(self, num_lineups):
        """Track progress during lineup generation."""
        lineups = []
        for i in tqdm(range(num_lineups), desc="Generating lineups"):
            lineup = generate_single_lineup()
            lineups.append(lineup)
        return lineups
```

### Cache Management CLI Commands
```python
@cli.group()
def cache():
    """Cache management commands"""
    pass

@cache.command()
def clear():
    """Clear all cached data"""
    cache = DataCache()
    cache.clear_cache()
    click.echo("Cache cleared successfully")

@cache.command()
def status():
    """Show cache status"""
    cache = DataCache()
    cache_files = list(cache.cache_dir.glob("*.json"))
    
    if not cache_files:
        click.echo("Cache is empty")
        return
    
    click.echo(f"Cache directory: {cache.cache_dir}")
    click.echo(f"Cached files: {len(cache_files)}")
    
    for cache_file in cache_files:
        file_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        size = cache_file.stat().st_size
        click.echo(f"  {cache_file.name}: {size} bytes, {file_age.total_seconds()/3600:.1f} hours old")

@cache.command()
@click.option('--max-age', type=int, default=24, help='Maximum age in hours')
def refresh(max_age):
    """Refresh stale cached data"""
    # Implementation to refresh old cache entries
    pass
```

## Acceptance Criteria
- Scraped data is cached and reused when fresh
- Application can work offline with cached data
- Cache expiration is configurable
- Performance improvements are measurable (faster startup, less memory usage)
- Progress indicators show during long operations
- Cache management commands provide control over cached data
- Parallel processing speeds up multiple lineup generation

## Files to Create/Modify
- `cache.py` - Caching system implementation
- `performance.py` - Performance optimization utilities
- `progress.py` - Progress tracking utilities
- Update scrapers to use caching
- Update CLI to include cache management commands
- Update `config.py` to include cache settings

## Dependencies to Add
- `tqdm` - Progress bars
- `joblib` - Parallel processing utilities

## Configuration Additions
```yaml
cache:
  enabled: true
  directory: "./cache"
  max_age_hours: 24
  auto_refresh: true

performance:
  parallel_processing: true
  max_workers: 4
  memory_optimization: true
```