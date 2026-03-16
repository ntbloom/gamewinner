# Step 06: YAML-Based Strategy Builder System

## Objective
Create a YAML-based interface for defining new strategies without writing Python code, then automatically generate the corresponding Python strategy files. This will enable users to quickly create and test new prediction algorithms using a declarative configuration format.

## Strategy Analysis

### Current Strategy Patterns
Analyzing existing strategies reveals common patterns:

#### Statistical Weighting Approaches
```python
# SlothfireSteady example
overall_score = (
    self._rank_to_percentile(props.rank_defense) +
    0.5 * self._rank_to_percentile(props.rank_tempo, reverse=True) +
    0.3 * self._rank_to_percentile(props.rank_offense) +
    0.3 * self._rank_to_percentile(props.rank_overall) -
    props.obj_kills_concede_per_game
)
```

#### Randomization Components
```python
# Adding upset factors
overall_score += random.random() * (
    self._rank_to_percentile(props.rank_roster) +
    min(self._rank_to_percentile(props.rank_home, reverse=True), 0.5)
)
```

#### Conditional Logic
```python
# Team-specific adjustments
if team.region == "East":
    overall_score *= 1.1
```

## YAML Strategy Definition Format

### Task 6.1: YAML Schema Design
**File**: `schemas/strategy_definition.yaml`

**Schema Structure**:
```yaml
# Strategy metadata
strategy:
  name: "MyCustomStrategy"
  description: "A strategy that values defense and experience"
  author: "User Name"
  version: "1.0"
  parent_class: "IMathStatsStrategy"  # or "IStrategy"

# Base scoring components
scoring:
  # Statistical components with weights
  components:
    - stat: "rank_defense"
      weight: 1.0
      transform: "percentile"  # percentile, inverse_percentile, raw, log
      
    - stat: "rank_offense" 
      weight: 0.7
      transform: "percentile"
      
    - stat: "rank_tempo"
      weight: 0.3
      transform: "inverse_percentile"  # Lower tempo = higher score
      
    - stat: "wins"
      weight: 0.1
      transform: "raw"
      normalize: true  # Scale to 0-1 range
      
  # Direct statistical additions/subtractions
  adjustments:
    - stat: "obj_kills_concede_per_game"
      operation: "subtract"  # subtract, add, multiply, divide
      
    - stat: "bpr"
      operation: "add"
      weight: 0.2

# Randomization and upset factors
randomization:
  enabled: true
  base_factor: 0.1  # How much randomness to add
  components:
    - stat: "rank_roster"
      weight: 1.0
      transform: "percentile"
    - stat: "rank_home"
      weight: 0.5
      transform: "inverse_percentile"
      cap: 0.5  # Maximum value

# Conditional logic rules
rules:
  - condition: "team.region == 'East'"
    action: "multiply"
    value: 1.1
    
  - condition: "props.rank_overall <= 10"  # Top 10 teams
    action: "add"
    value: 0.5
    
  - condition: "team.regional_rank >= 12"  # 12+ seeds
    action: "multiply" 
    value: 0.9  # Slight penalty

# Advanced features
advanced:
  # Bayesian updating with multiple iterations
  bayesian:
    enabled: false
    iterations: 100
    
  # Opponent-based adjustments  
  opponent_aware: false
  
  # Historical performance weighting
  historical_weight: 0.0  # 0.0 = no historical data, 1.0 = only historical

# Score prediction for championship game
score_prediction:
  winner_score: 78
  loser_score: 65
  method: "fixed"  # fixed, calculated, average
```

### Task 6.2: YAML Parser and Validator
**File**: `gamewinner/strategy_builder/yaml_parser.py`

**Core Classes**:
```python
from pydantic import BaseModel, validator
from typing import List, Dict, Any, Optional

class ScoringComponent(BaseModel):
    stat: str
    weight: float = 1.0
    transform: str = "percentile"  # percentile, inverse_percentile, raw, log
    normalize: bool = False
    cap: Optional[float] = None

class ScoringAdjustment(BaseModel):
    stat: str
    operation: str  # subtract, add, multiply, divide
    weight: float = 1.0

class RandomizationComponent(BaseModel):
    stat: str
    weight: float = 1.0
    transform: str = "percentile"
    cap: Optional[float] = None

class ConditionalRule(BaseModel):
    condition: str  # Python expression as string
    action: str     # multiply, add, subtract
    value: float

class StrategyDefinition(BaseModel):
    strategy: Dict[str, Any]
    scoring: Dict[str, Any]
    randomization: Optional[Dict[str, Any]] = None
    rules: Optional[List[ConditionalRule]] = None
    advanced: Optional[Dict[str, Any]] = None
    score_prediction: Optional[Dict[str, Any]] = None
    
    @validator('strategy')
    def validate_strategy_metadata(cls, v):
        required_fields = ['name', 'description', 'parent_class']
        for field in required_fields:
            if field not in v:
                raise ValueError(f"Missing required field: {field}")
        return v

class YAMLStrategyParser:
    def __init__(self, yaml_path: str):
        self.yaml_path = yaml_path
        
    def parse(self) -> StrategyDefinition:
        """Parse YAML file into validated strategy definition"""
        with open(self.yaml_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
        return StrategyDefinition(**yaml_data)
        
    def validate_stats_availability(self, definition: StrategyDefinition) -> List[str]:
        """Check if all referenced stats are available in data"""
        # Return list of missing/invalid statistics
```

### Task 6.3: Python Code Generator
**File**: `gamewinner/strategy_builder/code_generator.py`

**Code Generation Templates**:
```python
from jinja2 import Template

STRATEGY_CLASS_TEMPLATE = """
import random
from typing import Dict, Any

from gamewinner.strategies.mathstats.imathstats import IMathStatsStrategy
from gamewinner.teams.team import Team


class {{ strategy_name }}({{ parent_class }}):
    '''
    {{ description }}
    
    Generated automatically from YAML definition.
    Author: {{ author }}
    Version: {{ version }}
    '''

    @property
    def name(self) -> str:
        return "{{ strategy_name }}"

    def _team_metric(self, team: Team) -> float:
        props = self.get_props(team)
        
        # Base scoring components
        overall_score = 0.0
        
        {% for component in scoring_components %}
        # {{ component.stat }} component (weight: {{ component.weight }})
        {{ component.stat }}_value = self._apply_transform(
            props.{{ component.stat }}, 
            "{{ component.transform }}"{{ ", reverse=True" if component.transform == "inverse_percentile" else "" }}
        )
        {% if component.normalize %}
        {{ component.stat }}_value = self._normalize_value({{ component.stat }}_value)
        {% endif %}
        {% if component.cap %}
        {{ component.stat }}_value = min({{ component.stat }}_value, {{ component.cap }})
        {% endif %}
        overall_score += {{ component.weight }} * {{ component.stat }}_value
        {% endfor %}
        
        {% for adjustment in scoring_adjustments %}
        # {{ adjustment.stat }} adjustment
        {% if adjustment.operation == "subtract" %}
        overall_score -= {{ adjustment.weight }} * props.{{ adjustment.stat }}
        {% elif adjustment.operation == "add" %}
        overall_score += {{ adjustment.weight }} * props.{{ adjustment.stat }}
        {% endif %}
        {% endfor %}
        
        {% if randomization_enabled %}
        # Randomization component
        randomization_factor = {{ randomization_base_factor }} * random.random()
        upset_component = 0.0
        
        {% for rand_component in randomization_components %}
        {{ rand_component.stat }}_rand = self._apply_transform(
            props.{{ rand_component.stat }},
            "{{ rand_component.transform }}"{{ ", reverse=True" if rand_component.transform == "inverse_percentile" else "" }}
        )
        {% if rand_component.cap %}
        {{ rand_component.stat }}_rand = min({{ rand_component.stat }}_rand, {{ rand_component.cap }})
        {% endif %}
        upset_component += {{ rand_component.weight }} * {{ rand_component.stat }}_rand
        {% endfor %}
        
        overall_score += randomization_factor * upset_component
        {% endif %}
        
        {% if conditional_rules %}
        # Conditional rules
        {% for rule in conditional_rules %}
        if {{ rule.condition }}:
            {% if rule.action == "multiply" %}
            overall_score *= {{ rule.value }}
            {% elif rule.action == "add" %}
            overall_score += {{ rule.value }}
            {% elif rule.action == "subtract" %}
            overall_score -= {{ rule.value }}
            {% endif %}
        {% endfor %}
        {% endif %}
        
        return overall_score
        
    def _apply_transform(self, value: float, transform_type: str, reverse: bool = False) -> float:
        '''Apply statistical transformation to raw value'''
        if transform_type == "percentile" or transform_type == "inverse_percentile":
            return self._rank_to_percentile(value, reverse=reverse)
        elif transform_type == "raw":
            return value
        elif transform_type == "log":
            return math.log(max(value, 1))  # Avoid log(0)
        else:
            raise ValueError(f"Unknown transform type: {transform_type}")
            
    def _normalize_value(self, value: float) -> float:
        '''Normalize value to 0-1 range based on expected data range'''
        # Implementation depends on specific statistic
        # This is a simplified version
        return min(max(value / 100.0, 0.0), 1.0)
    
    {% if score_prediction %}
    def predict_score(self, winner: Team, loser: Team) -> tuple[int, int]:
        {% if score_prediction_method == "fixed" %}
        return {{ winner_score }}, {{ loser_score }}
        {% else %}
        # TODO: Implement calculated score prediction
        return {{ winner_score }}, {{ loser_score }}
        {% endif %}
    {% endif %}
"""

class CodeGenerator:
    def __init__(self):
        self.template = Template(STRATEGY_CLASS_TEMPLATE)
        
    def generate(self, definition: StrategyDefinition) -> str:
        """Generate Python code from strategy definition"""
        
        template_vars = {
            'strategy_name': definition.strategy['name'],
            'parent_class': definition.strategy['parent_class'], 
            'description': definition.strategy['description'],
            'author': definition.strategy.get('author', 'Unknown'),
            'version': definition.strategy.get('version', '1.0'),
            'scoring_components': definition.scoring.get('components', []),
            'scoring_adjustments': definition.scoring.get('adjustments', []),
            'randomization_enabled': definition.randomization and definition.randomization.get('enabled', False),
            'randomization_base_factor': definition.randomization.get('base_factor', 0.1) if definition.randomization else 0,
            'randomization_components': definition.randomization.get('components', []) if definition.randomization else [],
            'conditional_rules': definition.rules or [],
            'score_prediction': definition.score_prediction,
            'score_prediction_method': definition.score_prediction.get('method', 'fixed') if definition.score_prediction else None,
            'winner_score': definition.score_prediction.get('winner_score', 75) if definition.score_prediction else 75,
            'loser_score': definition.score_prediction.get('loser_score', 65) if definition.score_prediction else 65,
        }
        
        return self.template.render(**template_vars)
```

### Task 6.4: Strategy Registration System
**File**: `gamewinner/strategy_builder/registration.py`

**Auto-registration Process**:
```python
class StrategyRegistrar:
    def __init__(self):
        self.strategies_init_path = "gamewinner/strategies/__init__.py"
        
    def register_strategy(self, strategy_name: str, strategy_class_name: str, module_path: str):
        """Add strategy to __init__.py registration"""
        
        # 1. Add import statement
        import_line = f"from {module_path} import {strategy_class_name}"
        
        # 2. Add to available_strategies tuple
        self._update_init_file(import_line, strategy_class_name)
        
    def _update_init_file(self, import_line: str, class_name: str):
        """Modify __init__.py to include new strategy"""
        with open(self.strategies_init_path, 'r') as f:
            content = f.read()
            
        # Add import (check if not already present)
        if import_line not in content:
            # Insert after existing imports
            import_section_end = content.rfind("from gamewinner.strategies")
            next_newline = content.find('\n', import_section_end)
            content = content[:next_newline] + f"\n{import_line}" + content[next_newline:]
        
        # Add to available_strategies tuple
        if f"{class_name}()," not in content:
            # Find available_strategies tuple and add entry
            tuple_start = content.find("available_strategies = (")
            tuple_end = content.find(")", tuple_start)
            new_entry = f"    {class_name}(),"
            content = content[:tuple_end] + f"\n{new_entry}" + content[tuple_end:]
        
        # Write back
        with open(self.strategies_init_path, 'w') as f:
            f.write(content)
```

### Task 6.5: CLI Integration
**File**: `gamewinner/cli/strategy_builder_cli.py`

**New CLI Commands**:
```python
import click

@click.group()
def strategy_builder():
    """Strategy builder commands"""
    pass

@strategy_builder.command()
@click.argument('yaml_file')
@click.option('--output-dir', default='gamewinner/strategies/generated/')
@click.option('--register', is_flag=True, help='Auto-register strategy')
def generate(yaml_file, output_dir, register):
    """Generate Python strategy from YAML definition"""
    
    # Parse YAML
    parser = YAMLStrategyParser(yaml_file)
    definition = parser.parse()
    
    # Validate statistics
    missing_stats = parser.validate_stats_availability(definition)
    if missing_stats:
        click.echo(f"Warning: Missing statistics: {missing_stats}")
        if not click.confirm("Continue anyway?"):
            return
    
    # Generate code
    generator = CodeGenerator()
    python_code = generator.generate(definition)
    
    # Write to file
    strategy_name = definition.strategy['name']
    output_file = f"{output_dir}/{strategy_name.lower()}.py"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(python_code)
    
    click.echo(f"Strategy generated: {output_file}")
    
    # Register if requested
    if register:
        registrar = StrategyRegistrar()
        registrar.register_strategy(
            strategy_name, 
            strategy_name,
            f"gamewinner.strategies.generated.{strategy_name.lower()}"
        )
        click.echo(f"Strategy registered in __init__.py")

@strategy_builder.command()
@click.argument('yaml_file')
def validate(yaml_file):
    """Validate YAML strategy definition"""
    try:
        parser = YAMLStrategyParser(yaml_file)
        definition = parser.parse()
        
        # Check statistics availability
        missing_stats = parser.validate_stats_availability(definition)
        
        if missing_stats:
            click.echo("❌ Validation failed:")
            for stat in missing_stats:
                click.echo(f"  - Missing statistic: {stat}")
        else:
            click.echo("✅ Strategy definition is valid")
            
    except Exception as e:
        click.echo(f"❌ Validation error: {e}")

@strategy_builder.command()
def list_stats():
    """List available statistics for strategy building"""
    # Load sample data to show available columns
    sample_data = load_mathstats_data(2024)  # Use most recent year
    click.echo("Available statistics:")
    for col in sorted(sample_data.columns):
        click.echo(f"  - {col}")
```

### Task 6.6: Example Strategy Definitions
**File**: `examples/strategy_definitions/`

**Simple Defense-First Strategy**:
```yaml
# examples/strategy_definitions/defense_first.yaml
strategy:
  name: "DefenseFirst"
  description: "Prioritizes defensive efficiency and low tempo"
  author: "Strategy Builder"
  version: "1.0"
  parent_class: "IMathStatsStrategy"

scoring:
  components:
    - stat: "rank_defense"
      weight: 1.0
      transform: "percentile"
      
    - stat: "rank_offense"
      weight: 0.3
      transform: "percentile"
      
    - stat: "rank_tempo"
      weight: 0.5
      transform: "inverse_percentile"  # Prefer slower tempo

randomization:
  enabled: false

score_prediction:
  winner_score: 68
  loser_score: 58
  method: "fixed"
```

**Upset-Prone Strategy**:
```yaml
# examples/strategy_definitions/upset_special.yaml
strategy:
  name: "UpsetSpecial"
  description: "Loves picking upsets based on roster talent"
  author: "Strategy Builder"
  version: "1.0"
  parent_class: "IMathStatsStrategy"

scoring:
  components:
    - stat: "rank_overall"
      weight: 0.6
      transform: "percentile"
      
    - stat: "rank_roster" 
      weight: 1.2
      transform: "percentile"

randomization:
  enabled: true
  base_factor: 0.3  # High randomness
  components:
    - stat: "rank_home"
      weight: 0.8
      transform: "inverse_percentile"

rules:
  - condition: "team.regional_rank >= 10"  # 10+ seeds
    action: "multiply"
    value: 1.3  # Boost lower seeds
    
  - condition: "team.regional_rank <= 3"   # 1-3 seeds  
    action: "multiply"
    value: 0.8  # Slight penalty to top seeds
```

### Task 6.7: Testing Framework
**File**: `tests/test_strategy_builder.py`

**Test Cases**:
```python
def test_yaml_parsing():
    """Test YAML strategy definition parsing"""
    
def test_code_generation():
    """Test Python code generation from YAML"""
    
def test_generated_strategy_execution():
    """Test that generated strategies can run tournaments"""
    
def test_registration_system():
    """Test strategy registration in __init__.py"""
    
def test_cli_commands():
    """Test CLI strategy builder commands"""
```

### Task 6.8: Documentation and Examples
**File**: `docs/strategy_builder_guide.md`

**User Guide**:
```markdown
# Strategy Builder Guide

## Quick Start

1. Create a YAML strategy definition
2. Generate Python code: `poetry run strategy-builder generate my_strategy.yaml`
3. Register strategy: `poetry run strategy-builder generate my_strategy.yaml --register`
4. Run tournament: `poetry run play --strategy MyStrategy --year 2026`

## Available Statistics
[List of all available statistics with descriptions]

## Transform Types
- `percentile`: Convert rank to percentile (1st place = 100%)
- `inverse_percentile`: Higher rank = lower score
- `raw`: Use statistic value directly
- `log`: Logarithmic transformation

## Examples
[Include multiple example YAML files with explanations]
```

## Directory Structure
```
gamewinner/strategy_builder/
├── __init__.py
├── yaml_parser.py
├── code_generator.py
├── registration.py
└── templates/
    └── strategy_class.py.j2

gamewinner/strategies/generated/
├── __init__.py
└── [generated strategy files]

examples/strategy_definitions/
├── defense_first.yaml
├── upset_special.yaml
├── balanced_approach.yaml
└── tempo_based.yaml

schemas/
└── strategy_definition.yaml
```

## Usage Examples

### Generate Strategy
```bash
poetry run strategy-builder generate examples/strategy_definitions/defense_first.yaml --register
```

### Test Generated Strategy
```bash
poetry run play --strategy DefenseFirst --year 2026 --report detailed
```

### Validate Before Generation
```bash
poetry run strategy-builder validate my_custom_strategy.yaml
```

## Delivery Criteria
- [ ] YAML schema defined and validated
- [ ] Python code generator produces working strategies
- [ ] CLI commands functional for generate/validate/list-stats
- [ ] Auto-registration system updates __init__.py correctly
- [ ] Example strategy definitions provided
- [ ] Generated strategies can run tournaments successfully
- [ ] Documentation complete with usage examples
- [ ] Test coverage for all components

## Limitations and Future Enhancements
- **Current**: Basic statistical weighting and simple rules
- **Future**: Machine learning model integration, complex opponent-aware logic
- **Current**: Fixed score prediction
- **Future**: Dynamic score calculation based on team matchups

## Next Step
After implementing the YAML strategy builder, proceed to **07-strategy-builder-interactive.md** to create an interactive TUI/web interface for strategy creation.