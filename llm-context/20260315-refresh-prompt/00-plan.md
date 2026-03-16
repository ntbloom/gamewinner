# GameWinner March 2026 Refresh - Overall Plan

## Project Overview
The GameWinner repository is a March Madness bracket prediction system that allows users to implement various strategies for picking tournament winners. The system consists of:

1. **Data Layer**: Tournament bracket data (YAML/CSV), team statistics from Evan Miya (CSV)
2. **Strategy Framework**: Interface for implementing prediction algorithms
3. **Execution Engine**: CLI tool for running strategies and generating brackets
4. **Output System**: Various printers for displaying results

## Current State Assessment

### Data Files Structure
- `data/`: Tournament bracket information
  - `YYYY.yaml`: Tournament structure with regions and seeding
  - `csv/YYYY.csv`: Team records (wins/losses) with regional rankings
- `gamewinner/strategies/mathstats/data/YYYY.csv`: Evan Miya advanced statistics

### Strategy System
- Base interface: `IStrategy` in `gamewinner/strategies/istrategy.py`
- Math-based strategies: Inherit from `IMathStatsStrategy`
- Examples in `gamewinner/strategies/mathstats/derived/`
- Registration: `gamewinner/strategies/__init__.py`

## Implementation Plan Overview

### Phase 1: Data Refresh Pipeline (Steps 01-03)
- Create data fetching system for 2026 tournament bracket
- Build Evan Miya statistics scraper/API integration
- Implement data validation and format standardization

### Phase 2: Strategy System Enhancement (Steps 04-05) 
- Build strategy rendering and reporting system
- Create standings tracking for live tournament results
- Implement automated CI pipeline for results updates

### Phase 3: Strategy Builder Interface (Steps 06-07)
- Design YAML-based strategy definition format
- Build strategy code generation system
- Create interactive strategy builder (TUI/web interface)

## Key Technical Considerations

### Data Format Compatibility
- Evan Miya's current website may have different statistics categories than previous years
- Need to map new statistics to legacy column names for existing strategies
- Preserve backwards compatibility while enabling new features

### Strategy Dependencies
- Many strategies depend on specific column names from Evan Miya data
- Updates to data format require corresponding strategy file updates
- Need automated system to detect and flag incompatibilities

### Automation Requirements
- Tournament results need daily updates during March
- CI system should handle data fetching, processing, and report generation
- Error handling for API failures or data source changes

## Success Metrics
1. Successfully generate 2026 tournament data files matching legacy format
2. All existing strategies run without modification (or with minimal updates)
3. Automated reporting system produces readable strategy comparisons
4. Live standings update correctly as tournament progresses
5. New strategy creation workflow reduces development time by 50%

## Risk Mitigation
- **Data Source Changes**: Build flexible parsers with fallback options
- **API Rate Limits**: Implement caching and respectful request patterns
- **Format Evolution**: Version data schemas and maintain backwards compatibility
- **Tournament Changes**: Design system to handle format variations (play-in games, etc.)

## Next Steps
Proceed with implementation in numerical order starting with `01-data-refresh-tournament.md`. Each subsequent step builds upon the previous ones, creating a robust and automated system for future tournament years.