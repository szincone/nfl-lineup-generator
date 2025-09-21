# Add Lineup Optimization and Salary Cap Validation

## Description
The current lineup generation is purely random and doesn't consider DraftKings salary cap constraints or optimization strategies. This enhancement would add intelligent lineup optimization.

## Priority
Medium

## Labels
- enhancement
- algorithm
- optimization

## Current Issues
1. Lineup generation is completely random - no optimization
2. No salary cap validation (DraftKings has a $50,000 cap)
3. No consideration of player value vs. cost
4. Risk of selecting duplicate players in different positions
5. No lineup diversity or multiple lineup generation
6. No consideration of game theory or ownership projections

## Tasks
- [ ] Implement salary cap validation ($50,000 for DraftKings)
- [ ] Add value-based optimization (points per dollar)
- [ ] Implement linear programming optimization for optimal lineups
- [ ] Add duplicate player detection and prevention
- [ ] Create multiple diverse lineup generation
- [ ] Add tournament vs. cash game strategies
- [ ] Implement stack strategies (QB + WR from same team)
- [ ] Add player exposure limits
- [ ] Create lineup evaluation metrics

## Implementation Details

### Salary Cap Validation
```python
class LineupValidator:
    SALARY_CAP = 50000
    
    @staticmethod
    def validate_salary_cap(lineup: Lineup) -> bool:
        return lineup.total_salary <= LineupValidator.SALARY_CAP
    
    @staticmethod
    def validate_unique_players(lineup: Lineup) -> bool:
        player_names = [player.name for player in lineup.players]
        return len(player_names) == len(set(player_names))
```

### Optimization Algorithm
```python
from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, value

class LineupOptimizer:
    def optimize_lineup(self, players_df, strategy='value'):
        """
        Optimize lineup using linear programming
        strategy: 'value', 'upside', 'safe'
        """
        prob = LpProblem("DraftKings_Lineup", LpMaximize)
        
        # Decision variables
        x = {i: LpVariable(f"player_{i}", cat='Binary') 
             for i in players_df.index}
        
        # Objective function (maximize projected points)
        prob += sum(players_df.loc[i, 'ProjectedPoints'] * x[i] 
                   for i in players_df.index)
        
        # Salary constraint
        prob += sum(players_df.loc[i, 'Salary'] * x[i] 
                   for i in players_df.index) <= 50000
        
        # Position constraints
        prob += sum(x[i] for i in players_df[players_df['Position'] == 'QB'].index) == 1
        prob += sum(x[i] for i in players_df[players_df['Position'] == 'RB'].index) >= 2
        # ... other position constraints
        
        prob.solve()
        return self._extract_lineup(prob, players_df, x)
```

### Value-Based Selection
```python
def calculate_value_metrics(df):
    """Calculate various value metrics for players."""
    df['PointsPerDollar'] = df['ProjectedPoints'] / (df['Salary'] / 1000)
    df['ValueRank'] = df.groupby('Position')['PointsPerDollar'].rank(ascending=False)
    df['SalaryRank'] = df.groupby('Position')['Salary'].rank(ascending=True)
    df['PointsRank'] = df.groupby('Position')['ProjectedPoints'].rank(ascending=False)
    return df
```

### Multiple Lineup Generation
```python
class LineupGenerator:
    def generate_diverse_lineups(self, players_df, num_lineups=20, max_overlap=6):
        """Generate multiple diverse lineups with limited player overlap."""
        lineups = []
        used_players = set()
        
        for i in range(num_lineups):
            # Adjust player pool based on previous selections
            available_players = self._get_available_players(players_df, used_players, max_overlap)
            lineup = self.optimize_lineup(available_players)
            lineups.append(lineup)
            used_players.update(lineup.player_names)
        
        return lineups
```

### Stack Strategy Implementation
```python
def generate_stack_lineup(players_df, stack_type='qb_wr'):
    """Generate lineup with stacking strategy."""
    if stack_type == 'qb_wr':
        # Find QB + WR combinations from same team
        for team in players_df['Team'].unique():
            team_players = players_df[players_df['Team'] == team]
            qbs = team_players[team_players['Position'] == 'QB']
            wrs = team_players[team_players['Position'] == 'WR']
            
            if not qbs.empty and not wrs.empty:
                # Select best QB and WR from team for stack
                selected_qb = qbs.nlargest(1, 'ProjectedPoints')
                selected_wr = wrs.nlargest(1, 'ProjectedPoints')
                # ... continue building lineup around stack
```

## Acceptance Criteria
- All generated lineups respect the $50,000 salary cap
- No duplicate players across positions in a single lineup
- Optimization algorithm produces lineups with higher expected value than random selection
- Multiple lineup generation creates diverse lineups with configurable overlap limits
- Stacking strategies can be applied for tournament play
- Lineup evaluation metrics provide insight into lineup quality

## Files to Create/Modify
- `optimization.py` - Lineup optimization algorithms
- `validators.py` - Lineup validation functions
- `strategies.py` - Different lineup generation strategies
- `models.py` - Update Lineup class with optimization methods
- `lineup_generator.py` - Integrate optimization logic
- Update `requirements.txt` to include `pulp` for linear programming

## Dependencies to Add
- `pulp` - Linear programming optimization
- `numpy` - Numerical computations for optimization
- `scipy` - Scientific computing for advanced optimization