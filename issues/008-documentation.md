# Improve Documentation and Setup Instructions

## Description
The current documentation is minimal and lacks important setup instructions, usage examples, and contribution guidelines. This makes it difficult for new users to get started and for contributors to participate.

## Priority
High

## Labels
- documentation
- good-first-issue
- help-wanted

## Current Issues
1. Missing detailed setup instructions
2. No troubleshooting guide
3. Missing API documentation
4. No contribution guidelines
5. No code examples beyond basic usage
6. Missing dependency explanations
7. No documentation for environment variables

## Tasks
- [ ] Expand README.md with comprehensive setup instructions
- [ ] Add detailed API documentation
- [ ] Create troubleshooting guide
- [ ] Add contribution guidelines (CONTRIBUTING.md)
- [ ] Create code examples and tutorials
- [ ] Document all environment variables and configuration options
- [ ] Add screenshots and GIFs demonstrating usage
- [ ] Create documentation for different use cases
- [ ] Add FAQ section
- [ ] Set up documentation website (optional)

## Enhanced README.md Structure

```markdown
# NFL DraftKings Lineup Generator

A Python tool for generating optimized NFL DraftKings lineups using web scraping and data analysis.

## Features

- 🏈 Scrapes player data from Pro Football Reference
- 💰 Validates salary cap constraints ($50,000)
- 🎯 Multiple optimization strategies (value, upside, safe)
- 📊 Generates multiple diverse lineups
- 💾 Caching for improved performance
- 🖥️ Command-line interface
- 📈 Advanced filtering and player selection

## Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/szincone/nfl-lineup-generator.git
   cd nfl-lineup-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` file with your data sources:
   ```bash
   OFFENSE_URL=https://www.pro-football-reference.com/years/2023/opp.htm
   DEFENSE_URL=https://www.pro-football-reference.com/years/2023/opp.htm
   CSV_FILE=DKSalaries.csv
   ```

5. Add your DraftKings CSV file to the `csv_files/` directory

### Basic Usage

Generate a single optimized lineup:
```bash
python -m nfl_lineup generate
```

Generate multiple lineups:
```bash
python -m nfl_lineup generate --count 20 --strategy diverse
```

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OFFENSE_URL` | URL for offensive player stats | `https://www.pro-football-reference.com/...` |
| `DEFENSE_URL` | URL for defensive team stats | `https://www.pro-football-reference.com/...` |
| `CSV_FILE` | DraftKings salary CSV filename | `DKSalaries.csv` |

### DraftKings CSV Format

Your CSV file should contain these columns:
- `Name` - Player name
- `Position` - Player position (QB, RB, WR, TE, DST)
- `Salary` - Player salary
- `AvgPointsPerGame` - Average fantasy points per game
- `Team` - Player's team

## Usage Examples

### Command Line Interface

```bash
# Generate single lineup with value strategy
nfl-lineup generate --strategy value

# Generate 10 lineups with maximum diversity
nfl-lineup generate --count 10 --strategy diverse --max-overlap 4

# Save lineups to CSV
nfl-lineup generate --count 5 --output csv --file my_lineups.csv

# Work with cached data (offline mode)
nfl-lineup generate --use-cache --no-refresh

# Clear cache
nfl-lineup cache clear
```

### Python API

```python
from nfl_lineup import LineupGenerator, DataScraper

# Initialize components
scraper = DataScraper()
generator = LineupGenerator()

# Load and process data
offensive_data = scraper.scrape_offense()
defensive_data = scraper.scrape_defense()
dk_data = scraper.load_draftkings_csv('DKSalaries.csv')

# Generate optimized lineup
lineup = generator.generate_optimal_lineup(
    strategy='value',
    salary_cap=50000
)

print(lineup)
```

## Strategies

### Value Strategy
Maximizes points per dollar spent. Good for cash games.

### Upside Strategy  
Prioritizes high-ceiling players. Good for tournaments.

### Safe Strategy
Prioritizes consistent, low-variance players. Good for cash games.

### Diverse Strategy
Generates multiple lineups with limited player overlap.

## Troubleshooting

### Common Issues

**ImportError: No module named 'bs4'**
```bash
pip install beautifulsoup4
```

**EnvironmentError: Missing required environment variables**
- Ensure your `.env` file exists and contains all required variables
- Check that variable names match exactly (case-sensitive)

**FileNotFoundError: CSV file not found**
- Ensure your DraftKings CSV is in the `csv_files/` directory
- Check that the filename in `.env` matches exactly

**Empty lineup generated**
- Check that your CSV file has the correct format
- Verify that player data was scraped successfully
- Try lowering filtering thresholds in configuration

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Fork the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Run tests:
   ```bash
   pytest
   ```

## License

This project is licensed under the GNU General Public License v3.0 - see [LICENSE.md](LICENSE.md) for details.

## Disclaimer

This tool is for educational and research purposes. Please ensure compliance with DraftKings terms of service and applicable laws in your jurisdiction.
```

## CONTRIBUTING.md

```markdown
# Contributing to NFL Lineup Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful and inclusive. We welcome contributions from everyone.

## How to Contribute

### Reporting Issues

Before creating an issue, please:
1. Check if the issue already exists
2. Provide a clear, descriptive title
3. Include steps to reproduce the problem
4. Provide your environment details (OS, Python version, etc.)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass: `pytest`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to your branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Development Guidelines

#### Code Style
- Follow PEP 8 style guidelines
- Use type hints where possible
- Add docstrings to all public functions and classes
- Keep line length under 100 characters

#### Testing
- Write unit tests for new functionality
- Ensure all existing tests pass
- Aim for at least 80% code coverage
- Use meaningful test names

#### Documentation
- Update README.md for user-facing changes
- Add docstrings for new functions and classes
- Update API documentation for interface changes

## Development Setup

See the [Development Setup](README.md#development-setup) section in the README.

## Project Structure

```
nfl-lineup-generator/
├── nfl_lineup/           # Main package
│   ├── __init__.py
│   ├── cli.py           # Command-line interface
│   ├── scrapers/        # Web scraping modules
│   ├── optimization/    # Lineup optimization
│   └── models/          # Data models
├── tests/               # Test suite
├── docs/                # Documentation
├── csv_files/           # DraftKings CSV files
└── cache/               # Cached data
```

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.
```

## Files to Create/Modify
- Expand `README.md` with comprehensive documentation
- Create `CONTRIBUTING.md` with contribution guidelines
- Create `.env.example` with example environment variables
- Create `docs/` directory with additional documentation
- Add inline code documentation (docstrings)
- Create `CHANGELOG.md` for version tracking

## Acceptance Criteria
- README.md provides clear setup and usage instructions
- All major features are documented with examples
- Contribution process is clearly explained
- Troubleshooting guide addresses common issues
- API documentation covers all public interfaces
- Code examples are tested and working

## Implementation Notes
- Use clear, beginner-friendly language
- Include plenty of code examples
- Add screenshots/GIFs where helpful
- Keep documentation up-to-date with code changes
- Consider using MkDocs or Sphinx for advanced documentation