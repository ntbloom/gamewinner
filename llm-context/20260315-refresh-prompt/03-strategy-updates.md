# Step 03: Strategy Updates for 2026 Data Compatibility

## Objective
Update existing strategy files in `gamewinner/strategies/mathstats/derived/` to reference the correct statistics columns for 2026 data, ensuring all strategies can run with the updated Evan Miya dataset.

## Background Analysis

### Current Strategy Structure
All math-based strategies inherit from `IMathStatsStrategy` and use:
- `self.get_props(team)` to access team statistics
- Various ranking columns for team evaluation
- Statistical metrics like efficiency ratings and tempo

### Data File References
Strategies currently load data based on year:
- Data loaded from `gamewinner/strategies/mathstats/data/{year}.csv`
- Column references hardcoded in strategy implementations
- Rankings calculated relative to full dataset

## Implementation Tasks

### Task 3.1: Strategy Impact Assessment
**File**: `scripts/assess_strategy_impact.py`

**Purpose**: Catalog all column references across existing strategies

**Process**:
```python
def analyze_strategy_dependencies():
    """Scan all strategy files for column usage"""
    strategies_dir = "gamewinner/strategies/mathstats/derived/"
    column_usage = {}
    
    for strategy_file in glob.glob(f"{strategies_dir}/*.py"):
        with open(strategy_file) as f:
            content = f.read()
            # Find references to props.column_name
            column_refs = re.findall(r'props\.(\w+)', content)
            column_usage[strategy_file] = set(column_refs)
    
    return column_usage
```

**Expected Output**:
```
slothfire_steady.py: ['rank_defense', 'rank_tempo', 'rank_offense', 'obj_kills_concede_per_game']
the_cuts.py: ['rank_overall', 'bpr', 'wins', 'losses']
# ... other strategies
```

### Task 3.2: Column Mapping Documentation
**File**: `docs/2026_column_mapping.md`

**Purpose**: Document how 2024 columns map to 2026 columns

**Format**:
```markdown
## Column Mapping: 2024 -> 2026

| 2024 Column | 2026 Column | Status | Notes |
|-------------|-------------|---------|-------|
| rank_defense | def_rank | ✅ Direct | Same column |
| obj_kills_concede_per_game | runs_conceded_per_game | ✅ Direct | Renamed |
| some_old_metric | - | ❌ Missing | Need alternative calculation |
| - | new_advanced_metric | ➕ New | Available for future strategies |
```

### Task 3.3: IMathStatsStrategy Base Class Updates
**File**: `gamewinner/strategies/mathstats/imathstats.py`

**Current Analysis**: Examine how `get_props()` method works and update property mappings

**Expected Updates**:
```python
class TeamProperties:
    """Update property mappings for 2026 data format"""
    
    def __init__(self, team_data):
        # Map 2026 columns to legacy property names
        self.rank_defense = team_data.get('def_rank')
        self.rank_tempo = team_data.get('tempo_rank')  
        self.obj_kills_concede_per_game = team_data.get('runs_conceded_per_game', 0)
        
        # Handle missing columns with sensible defaults
        self.legacy_metric = self._calculate_legacy_metric(team_data)
    
    def _calculate_legacy_metric(self, data):
        """Calculate metrics no longer provided directly"""
        # Example: derive from available statistics
        return data.get('new_metric_a', 0) * 0.7 + data.get('new_metric_b', 0) * 0.3
```

### Task 3.4: Strategy-Specific Updates

#### High-Priority Strategies (Most Used)
Based on `available_strategies` in `__init__.py`:

**SlothfireSteady variants** (`slothfire_steady.py`):
- Uses: `rank_defense`, `rank_tempo`, `rank_offense`, `obj_kills_concede_per_game`
- Update column references to match 2026 format
- Test tempo calculation logic

**TheCuts variants** (`the_cuts.py`):
- Complex statistical combinations
- Likely needs significant column mapping
- May need new metric calculations

**Core Strategies** (`vanilla.py`, `rocky.py`, etc.):
- Simpler column dependencies
- Should be easier to update

#### Update Process for Each Strategy:
```python
def update_strategy_file(strategy_path, column_mapping):
    """Update a strategy file with new column mappings"""
    with open(strategy_path, 'r') as f:
        content = f.read()
    
    # Replace old column references with new ones
    for old_col, new_col in column_mapping.items():
        if new_col:  # Has direct mapping
            content = content.replace(f'props.{old_col}', f'props.{new_col}')
        else:  # Needs custom handling
            # Flag for manual review
            print(f"Manual update needed: {old_col} in {strategy_path}")
    
    # Write updated content
    with open(strategy_path, 'w') as f:
        f.write(content)
```

### Task 3.5: Data Loading Year Parameter
**File**: `gamewinner/strategies/mathstats/imathstats.py`

**Current Issue**: Strategies may hardcode data file year

**Solution**: Make year configurable through CLI or environment
```python
def load_mathstats_data(year=None):
    """Load math stats data for specified year"""
    if year is None:
        year = get_current_tournament_year()  # Default to current
    
    data_file = f"gamewinner/strategies/mathstats/data/{year}.csv"
    return pd.read_csv(data_file)
```

### Task 3.6: Backward Compatibility
**Requirement**: Ensure strategies still work with historical data (2023, 2024)

**Solution**: Implement adaptive column loading
```python
class AdaptiveTeamProperties:
    """Handle multiple data format versions"""
    
    def __init__(self, team_data, data_year):
        self.year = data_year
        self._load_properties(team_data)
    
    def _load_properties(self, data):
        """Load properties based on data year"""
        if self.year >= 2026:
            self.rank_defense = data.get('def_rank')
            self.obj_kills = data.get('runs_conceded_per_game', 0)
        else:  # Legacy format
            self.rank_defense = data.get('rank_defense')
            self.obj_kills = data.get('obj_kills_concede_per_game', 0)
```

### Task 3.7: Testing Framework
**File**: `tests/test_strategy_compatibility.py`

**Test Suite**:
```python
def test_all_strategies_with_2026_data():
    """Ensure all strategies run with 2026 data"""
    data_2026 = load_mathstats_data(2026)
    
    for strategy_class in available_strategies:
        strategy = strategy_class()
        # Test that strategy can calculate metrics for all teams
        for team in tournament_teams_2026:
            try:
                metric = strategy._team_metric(team)
                assert isinstance(metric, (int, float))
            except Exception as e:
                pytest.fail(f"{strategy.name} failed on {team}: {e}")

def test_backward_compatibility():
    """Ensure strategies still work with historical data"""
    for year in [2023, 2024]:
        data = load_mathstats_data(year)
        # Run subset of strategies to verify compatibility
        for strategy_class in core_strategies:
            strategy = strategy_class()
            # Verify can load and run basic operations
            assert strategy.can_process_data(data)
```

### Task 3.8: Documentation Updates
**Files to update**:
- Strategy class docstrings with column requirements
- README sections about data dependencies  
- Comments in strategy files about metric calculations

## Column Priority by Usage

### Critical Updates (Block release if missing)
- `rank_defense` / `def_rank`: Used by multiple defensive strategies
- `rank_tempo` / `tempo_rank`: Core to "slothfire" strategy family
- `bpr`, `obpr`, `dbpr`: Efficiency ratings used widely
- `wins`, `losses`: Basic record information

### Important Updates (Affect strategy quality)
- `rank_offense` / `off_rank`: Offensive evaluation
- `runs_conceded_per_game`: Defensive metrics
- `roster_rank`: Talent evaluation component

### Nice-to-Have Updates (Enhanced features)
- `home_rank`: Home court advantage factors
- Advanced metrics used by only a few strategies

## Quality Assurance Process

### Automated Testing
- Unit tests for each updated strategy
- Integration tests with full tournament simulation
- Performance regression tests (execution time)

### Manual Review
- Statistical output reasonableness checks
- Strategy behavior comparison (2024 vs 2026 predictions)
- Edge case handling (missing data, extreme values)

### Staged Rollout
1. Update and test one strategy at a time
2. Compare outputs between old and new versions
3. Get approval before updating additional strategies
4. Keep rollback plan ready

## Delivery Criteria
- [ ] All existing strategies execute without errors on 2026 data
- [ ] Strategy outputs are statistically reasonable
- [ ] Backward compatibility maintained for 2023/2024 data
- [ ] New column mappings documented
- [ ] Test coverage added for all updated strategies
- [ ] Performance impact assessed and acceptable

## Risk Mitigation

### Missing Columns
- Implement sensible defaults for missing statistics
- Create calculated alternatives where possible
- Document impact of substitutions on strategy quality

### Strategy Degradation
- Compare 2026 strategy outputs to previous years
- Flag significant behavioral changes for review
- Maintain option to revert specific strategies if needed

### Breaking Changes
- Test thoroughly with representative data samples
- Get stakeholder approval for significant modifications
- Document all changes for future reference

## Next Step
After completing strategy updates, proceed to **04-strategy-rendering.md** to build the reporting and visualization system for strategy outputs.