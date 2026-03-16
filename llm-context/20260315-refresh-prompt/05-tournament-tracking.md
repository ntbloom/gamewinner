# Step 05: Tournament Tracking and Live Standings System

## Objective
Build a system to track live tournament results as games are played and generate "standings" showing how each strategy is performing, similar to the examples in GitHub issue #19. Include comparison capabilities against manually-submitted brackets from ESPN.com and Yahoo.

## Reference Analysis

### GitHub Issue #19 Standings Format
Based on the referenced issue, standings should include:
- Strategy rankings by current score
- Points earned per round/game
- Elimination status (strategies that can no longer win)
- Comparison to human bracket performance
- Projected final scores based on remaining games

## Implementation Tasks

### Task 5.1: Tournament Results Data Pipeline
**File**: `gamewinner/tracking/results_fetcher.py`

**Data Sources**:
- **ESPN API**: `https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/`
- **CBS Sports API**: Tournament results endpoint
- **NCAA.com**: Official results (backup)

**Core Functions**:
```python
class TournamentResultsFetcher:
    def __init__(self, year: int):
        self.year = year
        self.base_urls = {
            'espn': f'https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard',
            'cbs': f'https://www.cbssports.com/college-basketball/scores/{year}/',
        }
    
    def fetch_daily_results(self, date: str) -> List[GameResult]:
        """Get all completed games for a specific date"""
        
    def fetch_tournament_status(self) -> TournamentStatus:
        """Get current tournament round and remaining games"""
        
    def validate_results(self, results: List[GameResult]) -> bool:
        """Verify results data integrity"""

@dataclass
class GameResult:
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    winner: str
    round_name: str  # "First Round", "Second Round", etc.
    game_date: str
    completed: bool
```

### Task 5.2: Bracket Scoring System
**File**: `gamewinner/tracking/bracket_scorer.py`

**Scoring Rules** (Traditional NCAA Tournament scoring):
```python
ROUND_POINTS = {
    "First Four": 0,      # No points for play-in games
    "First Round": 1,     # Round of 64
    "Second Round": 2,    # Round of 32  
    "Sweet 16": 4,
    "Elite 8": 8,
    "Final Four": 16,
    "Championship": 32,
}

class BracketScorer:
    def __init__(self, bracket_predictions: Dict, actual_results: List[GameResult]):
        self.predictions = bracket_predictions
        self.results = actual_results
        
    def calculate_current_score(self) -> int:
        """Calculate points earned so far"""
        
    def calculate_maximum_possible_score(self) -> int:
        """Best possible final score if all remaining picks are correct"""
        
    def identify_eliminated_predictions(self) -> List[str]:
        """Teams picked that have been eliminated"""
        
    def get_remaining_picks(self) -> Dict:
        """Predictions that could still earn points"""
```

### Task 5.3: Strategy Standings Generator
**File**: `gamewinner/tracking/standings_generator.py`

**Standings Data Structure**:
```python
@dataclass
class StrategyStanding:
    strategy_name: str
    current_score: int
    max_possible_score: int
    eliminated_picks: int
    correct_picks: int
    total_picks_made: int
    final_four_alive: int  # How many Final Four picks still possible
    championship_pick_alive: bool
    rank: int
    
class StandingsGenerator:
    def __init__(self, strategies: Dict[str, BracketPrediction], results: List[GameResult]):
        self.strategies = strategies
        self.results = results
        
    def generate_current_standings(self) -> List[StrategyStanding]:
        """Create ranked list of strategy performance"""
        
    def generate_standings_report(self) -> str:
        """Create formatted standings report"""
        
    def identify_leader_changes(self, previous_standings: List[StrategyStanding]) -> List[str]:
        """Track which strategies moved up/down"""
```

### Task 5.4: External Bracket Integration
**File**: `gamewinner/tracking/external_brackets.py`

**ESPN Bracket Integration**:
```python
class ESPNBracketFetcher:
    def __init__(self, group_id: str = None):
        self.group_id = group_id
        
    def fetch_group_standings(self) -> List[ExternalBracket]:
        """Get ESPN group bracket standings"""
        
    def fetch_public_leaderboard(self) -> List[ExternalBracket]:
        """Get overall ESPN leaderboard sample"""

@dataclass        
class ExternalBracket:
    bracket_name: str
    owner_name: str
    current_score: int
    max_possible_score: int
    percentile: float  # Compared to all ESPN brackets
    source: str  # "ESPN", "Yahoo", etc.
```

**Yahoo Bracket Integration**:
```python
class YahooBracketFetcher:
    def fetch_group_standings(self, group_id: str) -> List[ExternalBracket]:
        """Get Yahoo group standings"""
```

### Task 5.5: Comparative Analysis System
**File**: `gamewinner/tracking/comparative_analysis.py`

**Analysis Features**:
```python
class ComparativeAnalyzer:
    def __init__(self, strategy_standings: List[StrategyStanding], 
                 external_brackets: List[ExternalBracket]):
        self.strategies = strategy_standings
        self.external = external_brackets
        
    def compare_to_human_average(self) -> Dict[str, float]:
        """Compare each strategy to average human performance"""
        
    def identify_outperforming_strategies(self) -> List[str]:
        """Strategies beating majority of human brackets"""
        
    def calculate_percentile_rankings(self) -> Dict[str, float]:
        """Where each strategy would rank among all brackets"""
        
    def generate_comparison_report(self) -> str:
        """Create human vs AI comparison report"""
```

### Task 5.6: Automated Daily Updates
**File**: `scripts/daily_tournament_update.py`

**Daily Update Workflow**:
```python
def daily_update_workflow():
    """Run complete daily update process"""
    
    # 1. Fetch latest game results
    results_fetcher = TournamentResultsFetcher(2026)
    new_results = results_fetcher.fetch_daily_results(today())
    
    # 2. Update results database
    update_results_database(new_results)
    
    # 3. Recalculate all strategy standings
    all_results = load_all_results()
    standings = calculate_all_standings(all_results)
    
    # 4. Fetch external bracket data  
    external_data = fetch_external_brackets()
    
    # 5. Generate updated reports
    generate_standings_report(standings, external_data)
    
    # 6. Send notifications if significant changes
    check_and_notify_changes(standings)
```

### Task 5.7: CI/CD Integration
**File**: `.github/workflows/tournament_tracking.yml`

**Automated CI Pipeline**:
```yaml
name: Tournament Tracking Update

on:
  schedule:
    # Run every morning at 8 AM EST during tournament
    - cron: '0 13 * 3 *'
  workflow_dispatch:  # Manual trigger

jobs:
  update-standings:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: |
        pip install poetry
        poetry install
        
    - name: Fetch tournament results
      run: |
        poetry run python scripts/daily_tournament_update.py
        
    - name: Generate standings report
      run: |
        poetry run python scripts/generate_standings_report.py
        
    - name: Commit updated standings
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add standings/
        git diff --staged --quiet || git commit -m "Update tournament standings $(date)"
        git push
```

### Task 5.8: Standings Report Templates
**File**: `gamewinner/tracking/templates/standings_report.md`

**Report Template**:
```markdown
# March Madness Standings - Day {day_number}
*Updated: {timestamp}*

## Current Leaderboard

| Rank | Strategy | Current Score | Max Possible | Correct Picks | Status |
|------|----------|---------------|--------------|---------------|--------|
| 1 | {strategy_1} | {score_1} | {max_1} | {correct_1}/{total_1} | {status_1} |
| 2 | {strategy_2} | {score_2} | {max_2} | {correct_2}/{total_2} | {status_2} |

## Today's Results Impact
{daily_changes}

## Comparison to Human Brackets
- **Best Strategy vs ESPN Average**: {best_vs_avg}
- **Strategies in Top 10%**: {top_performers}
- **Strategies Below Average**: {underperformers}

## Final Four Status
{final_four_analysis}

## Elimination Report
{elimination_summary}

## Tomorrow's Key Games
{key_games}
```

### Task 5.9: Notification System
**File**: `gamewinner/tracking/notifications.py`

**Notification Triggers**:
- Major upsets that affect multiple strategies
- Leader changes in standings
- Strategies eliminated from contention
- Daily summary reports

```python
class NotificationSystem:
    def __init__(self):
        self.channels = ['email', 'slack', 'discord']  # Configurable
        
    def send_daily_summary(self, standings: List[StrategyStanding]):
        """Send daily standings update"""
        
    def send_upset_alert(self, upset_game: GameResult, affected_strategies: List[str]):
        """Notify about major upsets"""
        
    def send_leader_change_alert(self, old_leader: str, new_leader: str):
        """Notify when standings leader changes"""
```

### Task 5.10: Web Dashboard (Optional Enhancement)
**File**: `gamewinner/web/dashboard.py`

**Simple Flask/FastAPI Dashboard**:
```python
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def standings_dashboard():
    """Main standings dashboard"""
    current_standings = load_current_standings()
    return render_template('dashboard.html', standings=current_standings)

@app.route('/api/standings')
def api_standings():
    """API endpoint for standings data"""
    return jsonify(load_current_standings())

@app.route('/api/results/<date>')  
def api_daily_results(date):
    """API endpoint for daily results"""
    return jsonify(load_results_for_date(date))
```

## Data Storage

### Results Database
**File**: `data/tournament_results/2026_results.json`
```json
{
  "tournament_year": 2026,
  "last_updated": "2026-03-21T10:30:00Z",
  "current_round": "Sweet 16",
  "completed_games": [
    {
      "game_id": "game_001",
      "round": "First Round", 
      "home_team": "Duke",
      "away_team": "Vermont",
      "home_score": 87,
      "away_score": 56,
      "winner": "Duke",
      "date": "2026-03-18"
    }
  ],
  "remaining_games": [...],
  "eliminated_teams": [...]
}
```

### Standings History
**File**: `data/standings/2026_standings_history.json`
```json
{
  "2026-03-18": {
    "day": 1,
    "standings": [...],
    "external_comparison": {...}
  },
  "2026-03-19": {
    "day": 2,  
    "standings": [...],
    "external_comparison": {...}
  }
}
```

## Testing Strategy

### Unit Tests
- Test bracket scoring logic with known results
- Verify standings calculations
- Test external API data parsing

### Integration Tests
- Full pipeline test with mock tournament data
- Test CI workflow in development environment
- Verify report generation end-to-end

### Manual Testing
- Compare scoring against known ESPN/Yahoo results
- Verify standings match manual calculations
- Test notification systems

## Error Handling

### API Failures
- Retry logic with exponential backoff
- Fallback to alternative data sources
- Cache previous results to continue operations

### Data Inconsistencies  
- Validation of fetched results against multiple sources
- Manual override capabilities for incorrect data
- Audit trail for all data changes

## Performance Considerations

### Daily Processing
- Optimize for incremental updates (only new games)
- Cache external bracket data to minimize API calls
- Parallel processing of multiple strategies

### Storage
- Compress historical data after tournament completion
- Archive old tournament data to separate storage
- Implement data retention policies

## Delivery Criteria
- [ ] Daily results fetching working from ESPN/CBS APIs
- [ ] Bracket scoring system calculates points correctly
- [ ] Standings generation ranks strategies properly
- [ ] External bracket comparison (ESPN/Yahoo) functional
- [ ] Automated CI pipeline runs daily updates
- [ ] Notification system sends relevant alerts
- [ ] Historical data preserved for analysis
- [ ] Error handling covers common failure scenarios

## Security Considerations
- API keys stored securely in environment variables
- Rate limiting to respect external API terms
- Input validation for all external data sources
- Access controls for notification systems

## Next Step
After implementing tournament tracking, proceed to **06-strategy-builder-yaml.md** to create the YAML-based strategy definition system.