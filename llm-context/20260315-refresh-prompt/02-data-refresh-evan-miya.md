# Step 02: Evan Miya Statistics Data Refresh for 2026

## Objective
Fetch advanced basketball statistics from Evan Miya's website (`https://evanmiya.com/?team_ratings`) and format them to match the existing structure in `gamewinner/strategies/mathstats/data/2026.csv`, ensuring compatibility with existing strategies.

## Current Data Analysis

### Existing Format (`gamewinner/strategies/mathstats/data/2024.csv`)
Based on the 2024 file, the expected columns are:
```csv
rank,team,obpr,dbpr,bpr,opponent_adjust,pace_adjust,off_rank,def_rank,tempo,tempo_rank,rank_inj,home_rank,roster_rank,runs_per_game,runs_conceded_per_game,runs_total,runs_conceded_total,wins,losses
```

Key statistics used by existing strategies:
- **Ranking columns**: `rank`, `off_rank`, `def_rank`, `tempo_rank`, `home_rank`, `roster_rank`
- **Performance metrics**: `obpr`, `dbpr`, `bpr` (offensive/defensive/combined BPR)
- **Game flow**: `tempo`, `runs_per_game`, `runs_conceded_per_game`
- **Record**: `wins`, `losses`

## Data Source Investigation

### Evan Miya Website Structure
- **URL**: `https://evanmiya.com/?team_ratings`
- **Access**: May require subscription/payment
- **Format**: Likely table-based data that can be scraped
- **API**: Check if API access is available (preferred method)

### Subscription Requirements
- Research current pricing and access tiers
- Budget approval may be needed for subscription
- Document cost/benefit analysis for automated access

## Implementation Tasks

### Task 2.1: Evan Miya Access Setup
**Requirements**:
- Account creation and subscription if needed
- API key/authentication setup if available
- Rate limiting and usage terms compliance

### Task 2.2: Statistics Mapping Analysis
**File**: `scripts/analyze_evan_miya_format.py`

**Purpose**: Compare 2026 Evan Miya data structure to legacy format
- Identify renamed or missing columns
- Create mapping dictionary for column transformations
- Flag statistics that may need calculation from new data

**Expected Challenges**:
- Column names may have changed since 2024
- New statistics might be available that weren't in older data
- Some legacy columns might no longer be provided directly

### Task 2.3: Data Fetcher Implementation
**File**: `scripts/fetch_evan_miya_data.py`

**Key Functions**:
```python
def authenticate_evan_miya() -> Session:
    """Handle authentication/subscription access"""

def fetch_raw_statistics(session: Session) -> pd.DataFrame:
    """Get raw data from Evan Miya site/API"""

def map_to_legacy_format(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Transform to match existing column structure"""

def filter_tournament_teams(data: pd.DataFrame, tournament_teams: List[str]) -> pd.DataFrame:
    """Keep only teams in 2026 tournament bracket"""
```

**Data Transformation Logic**:
```python
COLUMN_MAPPING = {
    # Map new Evan Miya columns to legacy names
    'new_efficiency_rating': 'bpr',
    'off_efficiency': 'obpr', 
    'def_efficiency': 'dbpr',
    # ... other mappings as discovered
}

CALCULATED_COLUMNS = {
    # Columns that need calculation from multiple sources
    'runs_total': lambda df: df['runs_per_game'] * df['games_played'],
    'runs_conceded_total': lambda df: df['runs_conceded_per_game'] * df['games_played'],
}
```

### Task 2.4: Team Name Matching
**Challenge**: Evan Miya team names must match tournament bracket names exactly

**Solution**:
```python
TEAM_NAME_ALIASES = {
    # Map Evan Miya names to tournament bracket names
    'UConn': 'Connecticut',
    'Miami (FL)': 'Miami (Fla.)',
    'Saint Mary\'s (CA)': 'Saint Mary\'s',
    # ... build comprehensive mapping
}
```

### Task 2.5: Data Validation and Quality Checks
**File**: `scripts/validate_evan_miya_data.py`

**Validation Rules**:
- All 68 tournament teams have statistics
- Numerical ranges are reasonable (ranks 1-362, efficiency ratings realistic)
- Win/Loss records match tournament bracket data
- No missing values in critical columns used by strategies

### Task 2.6: Missing Data Handling
**Strategies for incomplete data**:
1. **Fallback Sources**: Use KenPom, Torvik, or other sites for missing teams
2. **Estimation**: Calculate missing statistics from available data
3. **Historical Data**: Use previous year's ratios for new teams
4. **Manual Research**: Look up missing data from official team statistics

## Strategy Impact Analysis

### Task 2.7: Strategy Compatibility Check
**File**: `scripts/check_strategy_compatibility.py`

**Purpose**: Ensure all existing strategies can run with new data format

**Process**:
1. Load each strategy class
2. Test against sample 2026 data
3. Identify columns used by each strategy
4. Flag any missing dependencies
5. Generate compatibility report

**Example Check**:
```python
def test_strategy_compatibility(strategy_class, data_2026):
    """Test if strategy can run with 2026 data"""
    try:
        strategy = strategy_class()
        # Mock tournament run with 2026 data
        test_result = run_mock_tournament(strategy, data_2026)
        return True, None
    except KeyError as e:
        return False, f"Missing column: {e}"
    except Exception as e:
        return False, f"Other error: {e}"
```

## Column Priority Classification

### Critical Columns (Must Have)
These are heavily used by multiple strategies:
- `rank`, `team`, `wins`, `losses`
- `off_rank`, `def_rank`, `tempo_rank`
- `bpr`, `obpr`, `dbpr`

### Important Columns (Should Have)
Used by some strategies:
- `roster_rank`, `home_rank`
- `tempo`, `runs_per_game`, `runs_conceded_per_game`

### Optional Columns (Nice to Have)
Used by fewer strategies or for specific features:
- `opponent_adjust`, `pace_adjust`
- `runs_total`, `runs_conceded_total`

## Delivery Plan

### Phase 1: Investigation and Setup
- [ ] Research Evan Miya subscription options
- [ ] Set up account and payment if required
- [ ] Document current data format and API availability

### Phase 2: Data Mapping
- [ ] Analyze 2026 data structure vs legacy format
- [ ] Create column mapping dictionary
- [ ] Build team name alias system

### Phase 3: Implementation
- [ ] Build data fetcher with authentication
- [ ] Implement data transformation pipeline
- [ ] Add validation and quality checks

### Phase 4: Integration Testing
- [ ] Test compatibility with existing strategies
- [ ] Generate comprehensive data quality report
- [ ] Update any strategies that need minor adjustments

## Error Handling Strategy

### Network Issues
- Retry logic with exponential backoff
- Fallback to cached data if available
- Alert system for prolonged failures

### Data Quality Issues
- Log warnings for suspicious values
- Manual review process for edge cases
- Fallback to alternative data sources

### Access Issues
- Monitor subscription status
- Automated renewal if possible
- Backup data sources identified

## Budget Considerations
- Evan Miya subscription cost (research needed)
- Development time for mapping and integration
- Potential costs for backup data sources
- Long-term maintenance and renewal costs

## Success Metrics
- [ ] All 68 tournament teams have complete statistics
- [ ] 95%+ of existing strategies run without modification
- [ ] Data quality metrics within acceptable ranges
- [ ] Automated pipeline runs reliably
- [ ] Documentation complete for future years

## Next Step
After completing Evan Miya data refresh, proceed to **03-strategy-updates.md** to update existing strategies to work with the 2026 data format.