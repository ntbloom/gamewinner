# Step 01: Tournament Data Refresh for 2026

## Objective
Create a pipeline to fetch and format the 2026 NCAA March Madness tournament bracket data, producing files that match the existing format in `data/2026.yaml` and `data/csv/2026.csv`.

## Data Sources
Primary sources for tournament bracket information:
- **ESPN.com**: `https://www.espn.com/mens-college-basketball/tournament/bracket`
- **CBS Sports**: `https://www.cbssports.com/college-basketball/bracketology/`
- **NCAA.com**: Official tournament bracket
- **ESPN API**: Potentially available endpoints for programmatic access

## Required Output Files

### 1. `data/2026.yaml`
**Format Reference**: Based on `data/2024.yaml`
```yaml
Year: 2026
WestPlays: East  # Which regions play in Final Four

East:
  1: [Team Name]
  2: [Team Name]
  # ... up to 16

Midwest:
  1: [Team Name]
  # ... similar structure

South:
  1: [Team Name]
  # ... similar structure  

West:
  1: [Team Name]
  # ... similar structure
```

### 2. `data/csv/2026.csv`
**Format Reference**: Based on `data/csv/2024.csv`
```csv
Team Name,Region,Regional Rank,Wins,Losses
Connecticut,East,1,31,3
# ... all tournament teams
```

**Key Fields**:
- Team Name: Exact match to YAML file
- Region: East/West/South/Midwest (with -Playoff suffix for First Four teams)
- Regional Rank: 1-16 (seed in region)
- Wins: Regular season wins
- Losses: Regular season losses

## Implementation Tasks

### Task 1.1: Create Tournament Data Fetcher
**File**: `scripts/fetch_tournament_data.py`

**Requirements**:
- Web scraping capability (BeautifulSoup, requests)
- Multiple source fallbacks (ESPN primary, CBS backup)
- Error handling for network issues
- Rate limiting to be respectful
- Command line interface for manual execution

**Key Functions**:
```python
def fetch_bracket_from_espn(year: int) -> TournamentBracket:
    """Fetch bracket structure from ESPN"""

def fetch_team_records(teams: List[str]) -> Dict[str, TeamRecord]:
    """Get win/loss records for tournament teams"""

def generate_yaml_format(bracket: TournamentBracket) -> str:
    """Convert bracket to YAML format"""

def generate_csv_format(bracket: TournamentBracket, records: Dict) -> str:
    """Convert bracket + records to CSV format"""
```

### Task 1.2: Data Validation System
**File**: `scripts/validate_tournament_data.py`

**Validation Rules**:
- Exactly 68 teams total (64 main bracket + 4 First Four)
- Each region has teams ranked 1-16
- Team names consistent between YAML and CSV
- Win/Loss numbers are reasonable (0-40 range)
- No duplicate team names
- Required regions present: East, West, South, Midwest

### Task 1.3: Integration with Existing System
**Updates needed**:
- Modify CLI to accept `--year 2026` parameter
- Update file loading logic to handle 2026 data files
- Add 2026 to any hardcoded year lists

### Task 1.4: Automation Script
**File**: `scripts/refresh_2026_data.sh`

```bash
#!/bin/bash
# Comprehensive data refresh script
python scripts/fetch_tournament_data.py --year 2026
python scripts/validate_tournament_data.py --year 2026
echo "2026 tournament data refreshed successfully"
```

## Data Mapping Considerations

### First Four Handling
Some teams compete in "First Four" games for final bracket spots:
- Mark region as `East-Playoff`, `West-Playoff`, etc.
- Both teams competing for same seed number
- Winner advances to main bracket

### Team Name Standardization
Ensure team names match across all sources:
- Handle common variations ("UConn" vs "Connecticut")
- Maintain consistency with previous years' naming
- Create mapping file for known aliases

### Regional Assignment
Tournament committee assigns regions, which may not match geographic location:
- Use official bracket assignments, not geographic logic
- Verify "WestPlays" assignment for Final Four matchups

## Testing Strategy

### Unit Tests
- Test data fetching with mock responses
- Validate YAML/CSV generation with known inputs
- Test error handling for malformed source data

### Integration Tests  
- Run full pipeline with previous years' data
- Verify output matches known-good files
- Test CLI integration with new 2026 files

### Manual Verification
- Spot-check team assignments against official bracket
- Verify win/loss records against ESPN team pages
- Confirm bracket structure matches tournament format

## Delivery Criteria
- [ ] `data/2026.yaml` file created with correct structure
- [ ] `data/csv/2026.csv` file created with all 68 teams
- [ ] Data validation passes all checks
- [ ] Existing CLI commands work with `--year 2026`
- [ ] Automation script runs without errors
- [ ] Documentation updated with data source notes

## Dependencies
- `requests` library for HTTP requests
- `beautifulsoup4` for HTML parsing
- `pyyaml` for YAML generation
- Existing gamewinner CLI infrastructure

## Next Step
After completing tournament data refresh, proceed to **02-data-refresh-evan-miya.md** to fetch advanced statistics for the 2026 teams.