# Improve Code Organization and Modular Design

## Description
The current code has several organizational issues including duplicate code, unclear module responsibilities, and poor separation of concerns. This refactoring would improve maintainability and testability.

## Priority
Medium

## Labels
- refactoring
- code-quality
- maintainability

## Current Issues
1. Duplicate position filtering logic between `combiner.py` and `lineup_generator.py`
2. Inconsistent variable naming and usage (e.g., `team_raw` vs `team`)
3. Mixed responsibilities in modules (data processing + team generation in same file)
4. Hardcoded magic numbers throughout the code
5. Global variables and module-level execution make testing difficult
6. No clear data model or class structure

## Tasks
- [ ] Create a `Player` class to represent individual players
- [ ] Create a `Team` or `Lineup` class to represent the generated lineup
- [ ] Extract configuration constants to a separate `config.py` file
- [ ] Refactor position filtering into reusable functions
- [ ] Separate data processing from lineup generation logic
- [ ] Remove duplicate code between modules
- [ ] Add proper docstrings to all functions and classes
- [ ] Implement consistent naming conventions
- [ ] Make modules importable without side effects

## Proposed Structure

### New File: `models.py`
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Player:
    name: str
    position: str
    salary: int
    team: str
    fantasy_points: float
    # ... other stats

@dataclass
class Lineup:
    qb: Player
    rb1: Player
    rb2: Player
    wr1: Player
    wr2: Player
    wr3: Player
    te: Player
    flex: Player
    dst: Player
    
    @property
    def total_salary(self) -> int:
        return sum(player.salary for player in self.players)
    
    @property
    def players(self) -> list[Player]:
        return [self.qb, self.rb1, self.rb2, self.wr1, self.wr2, self.wr3, self.te, self.flex, self.dst]
```

### New File: `config.py`
```python
# Filtering thresholds
WR_TARGET_QUANTILE = 0.75
RB_ATTEMPT_QUANTILE = 0.75
QB_COMPLETION_THRESHOLD = 0.6
QB_YARDS_PER_ATTEMPT_THRESHOLD = 5.0
VBD_THRESHOLDS = {
    'QB': 2.0,
    'RB': 1.5,
    'WR': 2.0,
    'TE': 2.0,
    'FLEX': 2.0
}
DEFENSE_QUANTILE = 0.25

# DraftKings lineup requirements
LINEUP_POSITIONS = {
    'QB': 1,
    'RB': 2,
    'WR': 3,
    'TE': 1,
    'FLEX': 1,
    'DST': 1
}
SALARY_CAP = 50000  # DraftKings salary cap
```

### Refactored `filters.py`
```python
def filter_by_position(df, position):
    """Filter dataframe by fantasy position."""
    return df[df['FantPos'] == position]

def filter_by_targets(df, quantile=0.75, vbd_threshold=2.0):
    """Filter players by target quantile and VBD threshold."""
    target_threshold = df.Tgt.quantile(q=quantile)
    return df[(df['Tgt'] >= target_threshold) & (df['VBD'] > vbd_threshold)]

def filter_quarterbacks(df):
    """Apply QB-specific filtering logic."""
    cmp_per = df['Pass_Cmp'] / df['Pass_Att']
    pypa = df['Pass_Yds'] / df['Pass_Att']
    return df[(cmp_per > 0.6) & (pypa > 5) & (df['VBD'] > 2)]
```

## Acceptance Criteria
- Code is organized into logical modules with clear responsibilities
- No duplicate code exists across modules
- All magic numbers are extracted to configuration
- Classes provide clear data models
- Functions are pure and testable (no global state dependencies)
- Docstrings explain all public functions and classes
- Code follows PEP 8 style guidelines

## Files to Create
- `models.py` - Data models for Player and Lineup
- `config.py` - Configuration constants
- `filters.py` - Player filtering functions
- `scrapers/` - Directory for scraping modules
- `utils.py` - Utility functions

## Files to Refactor
- `combiner.py` - Focus on data combination logic
- `lineup_generator.py` - Focus on lineup generation
- `scrape_fb_ref_off.py` - Move to `scrapers/` directory
- `scrape_fb_ref_def.py` - Move to `scrapers/` directory