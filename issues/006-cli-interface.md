# Add Command Line Interface (CLI)

## Description
The current application has no user interface and requires editing Python files to use. Adding a command-line interface would make the tool much more user-friendly and accessible.

## Priority
Medium

## Labels
- enhancement
- usability
- cli

## Current Issues
1. No user interface - requires modifying Python code to use
2. No way to specify different strategies or parameters
3. No way to generate multiple lineups easily
4. No output formatting options
5. No way to save lineups to different formats

## Tasks
- [ ] Implement CLI using `argparse` or `click`
- [ ] Add commands for different operations (scrape, generate, optimize)
- [ ] Add options for different lineup strategies
- [ ] Add output formatting options (console, CSV, JSON)
- [ ] Add configuration file support
- [ ] Add verbose/debug output options
- [ ] Add help documentation
- [ ] Make the package installable with entry points

## Proposed CLI Structure

### Main Command Structure
```bash
# Generate a single optimized lineup
nfl-lineup generate --strategy value --output console

# Generate multiple lineups
nfl-lineup generate --count 20 --strategy diverse --output csv --file lineups.csv

# Scrape fresh data
nfl-lineup scrape --offense-url URL --defense-url URL

# Show lineup statistics
nfl-lineup analyze --file lineup.csv

# Interactive mode
nfl-lineup interactive
```

### Implementation with Click
```python
import click
from typing import Optional

@click.group()
@click.version_option()
def cli():
    """NFL DraftKings Lineup Generator"""
    pass

@cli.command()
@click.option('--strategy', type=click.Choice(['random', 'value', 'upside', 'safe']), 
              default='value', help='Lineup generation strategy')
@click.option('--count', type=int, default=1, help='Number of lineups to generate')
@click.option('--output', type=click.Choice(['console', 'csv', 'json']), 
              default='console', help='Output format')
@click.option('--file', type=click.Path(), help='Output file path')
@click.option('--salary-cap', type=int, default=50000, help='Salary cap limit')
@click.option('--max-overlap', type=int, default=6, help='Max player overlap between lineups')
def generate(strategy, count, output, file, salary_cap, max_overlap):
    """Generate NFL lineups"""
    click.echo(f"Generating {count} lineup(s) using {strategy} strategy...")
    
    # Implementation here
    lineups = generate_lineups(
        strategy=strategy,
        count=count,
        salary_cap=salary_cap,
        max_overlap=max_overlap
    )
    
    if output == 'console':
        display_lineups_console(lineups)
    elif output == 'csv':
        save_lineups_csv(lineups, file or 'lineups.csv')
    elif output == 'json':
        save_lineups_json(lineups, file or 'lineups.json')

@cli.command()
@click.option('--offense-url', required=True, help='Offensive stats URL')
@click.option('--defense-url', required=True, help='Defensive stats URL')
@click.option('--output-dir', default='./data', help='Directory to save scraped data')
def scrape(offense_url, defense_url, output_dir):
    """Scrape fresh player data"""
    click.echo("Scraping player data...")
    # Implementation here

@cli.command()
@click.argument('lineup_file', type=click.Path(exists=True))
def analyze(lineup_file):
    """Analyze lineup file"""
    click.echo(f"Analyzing lineup file: {lineup_file}")
    # Implementation here

@cli.command()
def interactive():
    """Interactive lineup generation"""
    click.echo("Welcome to NFL Lineup Generator Interactive Mode!")
    
    while True:
        strategy = click.prompt('Choose strategy', 
                              type=click.Choice(['random', 'value', 'upside', 'safe']))
        count = click.prompt('Number of lineups', type=int, default=1)
        
        lineups = generate_lineups(strategy=strategy, count=count)
        display_lineups_console(lineups)
        
        if not click.confirm('Generate more lineups?'):
            break
```

### Configuration File Support
```yaml
# config.yaml
scraping:
  offense_url: "https://example.com/offense"
  defense_url: "https://example.com/defense"
  csv_file: "dk.csv"

generation:
  default_strategy: "value"
  salary_cap: 50000
  max_overlap: 6

output:
  default_format: "console"
  default_file: "lineups.csv"

filtering:
  qb_completion_threshold: 0.6
  qb_yards_per_attempt_threshold: 5.0
  vbd_thresholds:
    QB: 2.0
    RB: 1.5
    WR: 2.0
    TE: 2.0
```

### Output Formatting
```python
def display_lineups_console(lineups):
    """Display lineups in formatted console output."""
    for i, lineup in enumerate(lineups, 1):
        click.echo(f"\n--- Lineup {i} ---")
        click.echo(f"Total Salary: ${lineup.total_salary:,}")
        click.echo(f"Projected Points: {lineup.projected_points:.1f}")
        click.echo()
        
        # Table format
        headers = ['Position', 'Player', 'Team', 'Salary', 'Points']
        rows = [
            ['QB', lineup.qb.name, lineup.qb.team, f"${lineup.qb.salary:,}", f"{lineup.qb.projected_points:.1f}"],
            ['RB', lineup.rb1.name, lineup.rb1.team, f"${lineup.rb1.salary:,}", f"{lineup.rb1.projected_points:.1f}"],
            # ... other positions
        ]
        
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))

def save_lineups_csv(lineups, filename):
    """Save lineups to CSV format."""
    rows = []
    for lineup in lineups:
        row = {
            'QB': lineup.qb.name,
            'RB1': lineup.rb1.name,
            'RB2': lineup.rb2.name,
            'WR1': lineup.wr1.name,
            'WR2': lineup.wr2.name,
            'WR3': lineup.wr3.name,
            'TE': lineup.te.name,
            'FLEX': lineup.flex.name,
            'DST': lineup.dst.name,
            'Total_Salary': lineup.total_salary,
            'Projected_Points': lineup.projected_points
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)
    click.echo(f"Lineups saved to {filename}")
```

## Acceptance Criteria
- CLI provides intuitive commands for all major operations
- Help documentation is comprehensive and clear
- Multiple output formats are supported (console, CSV, JSON)
- Configuration files eliminate need for command-line options
- Interactive mode provides guided lineup generation
- Package can be installed and used system-wide
- Error messages are helpful and actionable

## Files to Create/Modify
- `cli.py` - Main CLI implementation
- `setup.py` - Package installation and entry points
- `config.py` - Configuration file handling
- `formatters.py` - Output formatting functions
- Update `requirements.txt` to include CLI dependencies
- Create example configuration files

## Dependencies to Add
- `click` - CLI framework
- `tabulate` - Console table formatting
- `pyyaml` - YAML configuration file support
- `colorama` - Cross-platform colored terminal output