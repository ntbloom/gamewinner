# Step 07: Interactive Strategy Builder Interface

## Objective
Create an interactive interface (Terminal UI and/or Web UI) that allows users to build strategies visually without writing YAML or Python code. The interface should guide users through the strategy creation process and provide real-time feedback on their choices.

## Interface Options Analysis

### Option 1: Terminal User Interface (TUI)
**Pros**: 
- Lightweight, no web server required
- Consistent with CLI-based workflow
- Works in any terminal environment

**Cons**:
- Limited visual capabilities
- Less intuitive for complex configurations

### Option 2: Web Interface
**Pros**:
- Rich visual interface with charts/graphs
- Better user experience for complex configurations
- Can include real-time data visualization

**Cons**:
- Requires web server setup
- More complex deployment

### Option 3: Hybrid Approach
- TUI for basic strategy creation
- Web interface for advanced features and visualization
- Both generate same YAML output format

## Implementation Tasks

### Task 7.1: TUI Strategy Builder
**File**: `gamewinner/strategy_builder/tui_builder.py`

**Technology**: Use `textual` library for rich terminal interface

**Core Components**:
```python
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Button, Input, Select, 
    DataTable, Static, Checkbox, Slider
)

class StrategyBuilderTUI(App):
    """Interactive terminal strategy builder"""
    
    CSS_PATH = "strategy_builder.css"
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            Vertical(
                Static("Strategy Metadata", classes="section-title"),
                Input(placeholder="Strategy Name", id="strategy_name"),
                Input(placeholder="Description", id="description"),
                Input(placeholder="Author", id="author"),
                classes="metadata-panel"
            ),
            Vertical(
                Static("Statistical Components", classes="section-title"),
                DataTable(id="components_table"),
                Button("Add Component", id="add_component"),
                classes="components-panel"
            ),
            classes="main-panels"
        )
        yield Horizontal(
            Button("Preview YAML", id="preview"),
            Button("Generate Strategy", id="generate"),
            Button("Save & Exit", id="save"),
            classes="action-buttons"
        )
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the interface"""
        # Setup components table
        table = self.query_one("#components_table", DataTable)
        table.add_columns("Statistic", "Weight", "Transform", "Actions")
        
        # Load available statistics
        self.available_stats = self._load_available_statistics()
        
    def _load_available_statistics(self) -> List[str]:
        """Load available statistics from data files"""
        # Use most recent data to get column names
        sample_data = load_mathstats_data(2024)
        return sorted(sample_data.columns.tolist())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks"""
        if event.button.id == "add_component":
            self._show_add_component_dialog()
        elif event.button.id == "preview":
            self._show_yaml_preview()
        elif event.button.id == "generate":
            self._generate_strategy()

class AddComponentDialog(App):
    """Dialog for adding statistical components"""
    
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Add Statistical Component"),
            Select(
                [(stat, stat) for stat in available_stats],
                prompt="Select Statistic",
                id="stat_select"
            ),
            Slider(0.0, 2.0, 1.0, step=0.1, id="weight_slider"),
            Static("Weight: 1.0", id="weight_display"),
            Select([
                ("percentile", "Percentile"),
                ("inverse_percentile", "Inverse Percentile"), 
                ("raw", "Raw Value"),
                ("log", "Logarithmic")
            ], id="transform_select"),
            Horizontal(
                Button("Add", id="confirm"),
                Button("Cancel", id="cancel")
            )
        )
```

**TUI Features**:
- **Component Management**: Add/remove/edit statistical components
- **Weight Adjustment**: Visual sliders for component weights
- **Transform Selection**: Dropdown for transform types
- **Live Preview**: Show YAML output as user builds strategy
- **Validation**: Real-time validation with error highlighting
- **Template Loading**: Start from existing strategy templates

### Task 7.2: Web Strategy Builder
**File**: `gamewinner/strategy_builder/web_builder.py`

**Technology**: Use FastAPI + React/Vue.js or pure HTML/JS

**FastAPI Backend**:
```python
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="GameWinner Strategy Builder")

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/statistics")
async def get_available_statistics():
    """Get list of available statistics"""
    sample_data = load_mathstats_data(2024)
    stats_info = []
    
    for col in sample_data.columns:
        stats_info.append({
            "name": col,
            "description": get_stat_description(col),
            "type": get_stat_type(col),
            "range": get_stat_range(sample_data[col])
        })
    
    return stats_info

@app.post("/api/preview")
async def preview_strategy(strategy_definition: Dict[str, Any]):
    """Generate YAML preview from strategy definition"""
    try:
        yaml_content = generate_yaml_from_dict(strategy_definition)
        return {"yaml": yaml_content, "valid": True}
    except Exception as e:
        return {"yaml": "", "valid": False, "error": str(e)}

@app.post("/api/generate")
async def generate_strategy(strategy_definition: Dict[str, Any]):
    """Generate Python strategy file"""
    try:
        # Convert to YAML
        yaml_content = generate_yaml_from_dict(strategy_definition)
        
        # Generate Python code
        parser = YAMLStrategyParser()
        definition = parser.parse_from_string(yaml_content)
        generator = CodeGenerator()
        python_code = generator.generate(definition)
        
        return {
            "success": True,
            "yaml": yaml_content,
            "python": python_code,
            "filename": f"{definition.strategy['name'].lower()}.py"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/templates")
async def get_strategy_templates():
    """Get available strategy templates"""
    templates_dir = "examples/strategy_definitions/"
    templates = []
    
    for yaml_file in glob.glob(f"{templates_dir}*.yaml"):
        with open(yaml_file) as f:
            template_data = yaml.safe_load(f)
        
        templates.append({
            "name": template_data["strategy"]["name"],
            "description": template_data["strategy"]["description"],
            "file": os.path.basename(yaml_file),
            "definition": template_data
        })
    
    return templates
```

**Frontend Interface** (HTML/JavaScript):
```html
<!-- gamewinner/strategy_builder/static/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>GameWinner Strategy Builder</title>
    <link rel="stylesheet" href="/static/css/builder.css">
</head>
<body>
    <div id="app">
        <!-- Strategy Metadata Panel -->
        <section class="metadata-panel">
            <h2>Strategy Information</h2>
            <input type="text" id="strategy-name" placeholder="Strategy Name">
            <textarea id="strategy-description" placeholder="Description"></textarea>
            <input type="text" id="strategy-author" placeholder="Author">
        </section>
        
        <!-- Components Panel -->
        <section class="components-panel">
            <h2>Statistical Components</h2>
            <div id="components-list"></div>
            <button id="add-component">Add Component</button>
        </section>
        
        <!-- Randomization Panel -->
        <section class="randomization-panel">
            <h2>Randomization Settings</h2>
            <label>
                <input type="checkbox" id="randomization-enabled"> Enable Randomization
            </label>
            <div id="randomization-settings" class="hidden">
                <label>Base Factor: <input type="range" id="base-factor" min="0" max="1" step="0.05" value="0.1"></label>
            </div>
        </section>
        
        <!-- Rules Panel -->
        <section class="rules-panel">
            <h2>Conditional Rules</h2>
            <div id="rules-list"></div>
            <button id="add-rule">Add Rule</button>
        </section>
        
        <!-- Preview Panel -->
        <section class="preview-panel">
            <h2>Preview</h2>
            <div class="tabs">
                <button class="tab-button active" data-tab="yaml">YAML</button>
                <button class="tab-button" data-tab="python">Python</button>
            </div>
            <div class="tab-content">
                <pre id="yaml-preview" class="tab-panel active"></pre>
                <pre id="python-preview" class="tab-panel hidden"></pre>
            </div>
        </section>
        
        <!-- Actions -->
        <section class="actions">
            <button id="load-template">Load Template</button>
            <button id="validate">Validate</button>
            <button id="generate">Generate Strategy</button>
            <button id="download">Download Files</button>
        </section>
    </div>
    
    <script src="/static/js/builder.js"></script>
</body>
</html>
```

**Frontend JavaScript**:
```javascript
// gamewinner/strategy_builder/static/js/builder.js
class StrategyBuilder {
    constructor() {
        this.strategy = {
            strategy: {
                name: "",
                description: "",
                author: "",
                version: "1.0",
                parent_class: "IMathStatsStrategy"
            },
            scoring: {
                components: [],
                adjustments: []
            },
            randomization: {
                enabled: false,
                base_factor: 0.1,
                components: []
            },
            rules: []
        };
        
        this.availableStats = [];
        this.initialize();
    }
    
    async initialize() {
        await this.loadAvailableStats();
        this.bindEvents();
        this.updatePreview();
    }
    
    async loadAvailableStats() {
        const response = await fetch('/api/statistics');
        this.availableStats = await response.json();
    }
    
    bindEvents() {
        document.getElementById('add-component').addEventListener('click', () => {
            this.showAddComponentModal();
        });
        
        document.getElementById('generate').addEventListener('click', () => {
            this.generateStrategy();
        });
        
        // Auto-update preview when fields change
        ['strategy-name', 'strategy-description', 'strategy-author'].forEach(id => {
            document.getElementById(id).addEventListener('input', (e) => {
                this.updateStrategyMetadata(id, e.target.value);
            });
        });
    }
    
    updateStrategyMetadata(field, value) {
        const fieldMap = {
            'strategy-name': 'name',
            'strategy-description': 'description', 
            'strategy-author': 'author'
        };
        
        this.strategy.strategy[fieldMap[field]] = value;
        this.updatePreview();
    }
    
    async updatePreview() {
        const response = await fetch('/api/preview', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(this.strategy)
        });
        
        const result = await response.json();
        document.getElementById('yaml-preview').textContent = result.yaml;
        
        if (!result.valid) {
            document.getElementById('yaml-preview').classList.add('error');
        } else {
            document.getElementById('yaml-preview').classList.remove('error');
        }
    }
    
    showAddComponentModal() {
        // Create modal for adding statistical components
        const modal = this.createComponentModal();
        document.body.appendChild(modal);
    }
    
    createComponentModal() {
        const modal = document.createElement('div');
        modal.className = 'modal';
        
        const statsOptions = this.availableStats.map(stat => 
            `<option value="${stat.name}">${stat.name} - ${stat.description}</option>`
        ).join('');
        
        modal.innerHTML = `
            <div class="modal-content">
                <h3>Add Statistical Component</h3>
                <div class="form-group">
                    <label>Statistic:</label>
                    <select id="modal-stat-select">${statsOptions}</select>
                </div>
                <div class="form-group">
                    <label>Weight: <span id="weight-display">1.0</span></label>
                    <input type="range" id="modal-weight" min="0" max="2" step="0.1" value="1.0">
                </div>
                <div class="form-group">
                    <label>Transform:</label>
                    <select id="modal-transform">
                        <option value="percentile">Percentile</option>
                        <option value="inverse_percentile">Inverse Percentile</option>
                        <option value="raw">Raw Value</option>
                        <option value="log">Logarithmic</option>
                    </select>
                </div>
                <div class="form-actions">
                    <button id="modal-add">Add</button>
                    <button id="modal-cancel">Cancel</button>
                </div>
            </div>
        `;
        
        // Bind modal events
        modal.querySelector('#modal-add').addEventListener('click', () => {
            this.addComponent({
                stat: modal.querySelector('#modal-stat-select').value,
                weight: parseFloat(modal.querySelector('#modal-weight').value),
                transform: modal.querySelector('#modal-transform').value
            });
            document.body.removeChild(modal);
        });
        
        modal.querySelector('#modal-cancel').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        return modal;
    }
    
    addComponent(component) {
        this.strategy.scoring.components.push(component);
        this.updateComponentsList();
        this.updatePreview();
    }
    
    updateComponentsList() {
        const list = document.getElementById('components-list');
        list.innerHTML = '';
        
        this.strategy.scoring.components.forEach((comp, index) => {
            const item = document.createElement('div');
            item.className = 'component-item';
            item.innerHTML = `
                <span class="stat-name">${comp.stat}</span>
                <span class="weight">Weight: ${comp.weight}</span>
                <span class="transform">${comp.transform}</span>
                <button onclick="builder.removeComponent(${index})">Remove</button>
            `;
            list.appendChild(item);
        });
    }
    
    removeComponent(index) {
        this.strategy.scoring.components.splice(index, 1);
        this.updateComponentsList();
        this.updatePreview();
    }
    
    async generateStrategy() {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(this.strategy)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Show generated code
            document.getElementById('python-preview').textContent = result.python;
            
            // Enable download
            this.enableDownload(result.yaml, result.python, result.filename);
        } else {
            alert('Generation failed: ' + result.error);
        }
    }
    
    enableDownload(yaml, python, filename) {
        const downloadBtn = document.getElementById('download');
        downloadBtn.disabled = false;
        
        downloadBtn.onclick = () => {
            // Download YAML file
            this.downloadFile(yaml, `${filename.replace('.py', '.yaml')}`, 'text/yaml');
            // Download Python file  
            this.downloadFile(python, filename, 'text/python');
        };
    }
    
    downloadFile(content, filename, type) {
        const blob = new Blob([content], {type: type});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
    }
}

// Initialize when page loads
let builder;
document.addEventListener('DOMContentLoaded', () => {
    builder = new StrategyBuilder();
});
```

### Task 7.3: Template System Integration
**File**: `gamewinner/strategy_builder/templates.py`

**Template Management**:
```python
class StrategyTemplateManager:
    def __init__(self):
        self.templates_dir = "examples/strategy_definitions/"
        
    def list_templates(self) -> List[Dict]:
        """Get available strategy templates"""
        templates = []
        
        for yaml_file in glob.glob(f"{self.templates_dir}*.yaml"):
            with open(yaml_file) as f:
                template_data = yaml.safe_load(f)
            
            templates.append({
                "id": os.path.basename(yaml_file).replace('.yaml', ''),
                "name": template_data["strategy"]["name"],
                "description": template_data["strategy"]["description"],
                "category": template_data.get("category", "General"),
                "difficulty": template_data.get("difficulty", "Beginner"),
                "file_path": yaml_file
            })
        
        return templates
    
    def load_template(self, template_id: str) -> Dict:
        """Load a specific template"""
        template_file = f"{self.templates_dir}{template_id}.yaml"
        
        with open(template_file) as f:
            return yaml.safe_load(f)
    
    def create_custom_template(self, name: str, definition: Dict) -> str:
        """Save a strategy as a reusable template"""
        template_file = f"{self.templates_dir}custom_{name.lower()}.yaml"
        
        with open(template_file, 'w') as f:
            yaml.dump(definition, f, default_flow_style=False)
        
        return template_file
```

### Task 7.4: Statistics Visualization
**File**: `gamewinner/strategy_builder/stats_viz.py`

**Data Visualization for Web Interface**:
```python
import plotly.graph_objects as go
import plotly.express as px

class StatisticsVisualizer:
    def __init__(self):
        self.sample_data = load_mathstats_data(2024)
        
    def create_stat_distribution_chart(self, stat_name: str) -> str:
        """Create distribution chart for a statistic"""
        data = self.sample_data[stat_name]
        
        fig = px.histogram(
            x=data,
            title=f"Distribution of {stat_name}",
            labels={'x': stat_name, 'y': 'Number of Teams'}
        )
        
        return fig.to_html(div_id=f"chart_{stat_name}")
    
    def create_correlation_matrix(self, selected_stats: List[str]) -> str:
        """Create correlation matrix for selected statistics"""
        correlation_data = self.sample_data[selected_stats].corr()
        
        fig = px.imshow(
            correlation_data,
            title="Correlation Matrix",
            aspect="auto"
        )
        
        return fig.to_html(div_id="correlation_matrix")
    
    def create_strategy_simulation_chart(self, strategy_def: Dict) -> str:
        """Simulate strategy performance on historical data"""
        # Run strategy on sample teams and visualize results
        # This would show how the strategy would rank teams
        pass
```

### Task 7.5: CLI Integration
**File**: `gamewinner/cli/interactive_builder.py`

**Enhanced CLI Commands**:
```python
@click.group()
def interactive():
    """Interactive strategy builder commands"""
    pass

@interactive.command()
def tui():
    """Launch terminal strategy builder"""
    from gamewinner.strategy_builder.tui_builder import StrategyBuilderTUI
    app = StrategyBuilderTUI()
    app.run()

@interactive.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=8000)
def web(host, port):
    """Launch web strategy builder"""
    import uvicorn
    from gamewinner.strategy_builder.web_builder import app
    
    click.echo(f"Starting web strategy builder at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

@interactive.command()
@click.argument('template_name')
@click.option('--customize', is_flag=True)
def from_template(template_name, customize):
    """Create strategy from template"""
    template_mgr = StrategyTemplateManager()
    
    try:
        template_def = template_mgr.load_template(template_name)
        
        if customize:
            # Launch TUI with template pre-loaded
            app = StrategyBuilderTUI(initial_strategy=template_def)
            app.run()
        else:
            # Generate directly from template
            strategy_name = template_def["strategy"]["name"] + "_Custom"
            template_def["strategy"]["name"] = strategy_name
            
            # Generate and register
            generate_and_register_strategy(template_def)
            
    except FileNotFoundError:
        click.echo(f"Template '{template_name}' not found")
        click.echo("Available templates:")
        for template in template_mgr.list_templates():
            click.echo(f"  - {template['id']}: {template['name']}")
```

### Task 7.6: Advanced Features

#### Real-time Strategy Testing
```python
class StrategyTester:
    def __init__(self):
        self.historical_data = load_all_historical_data()
        
    def test_strategy_on_historical_data(self, strategy_def: Dict) -> Dict:
        """Test strategy performance on past tournaments"""
        results = {}
        
        for year in [2022, 2023, 2024]:
            # Generate strategy for that year
            strategy = create_strategy_from_definition(strategy_def)
            
            # Run on historical bracket
            bracket_result = run_strategy_on_year(strategy, year)
            
            # Calculate performance metrics
            results[year] = calculate_performance_metrics(bracket_result, year)
        
        return results

    def compare_against_existing_strategies(self, new_strategy_def: Dict) -> Dict:
        """Compare new strategy against existing ones"""
        comparisons = {}
        
        for existing_strategy in available_strategies:
            similarity_score = calculate_strategy_similarity(new_strategy_def, existing_strategy)
            performance_diff = calculate_performance_difference(new_strategy_def, existing_strategy)
            
            comparisons[existing_strategy.name] = {
                'similarity': similarity_score,
                'performance_diff': performance_diff
            }
        
        return comparisons
```

#### Strategy Optimization
```python
class StrategyOptimizer:
    def optimize_weights(self, base_strategy_def: Dict, historical_years: List[int]) -> Dict:
        """Use genetic algorithm or grid search to optimize component weights"""
        
    def suggest_improvements(self, strategy_def: Dict) -> List[str]:
        """Analyze strategy and suggest improvements"""
        suggestions = []
        
        # Check for common issues
        if len(strategy_def["scoring"]["components"]) == 1:
            suggestions.append("Consider adding multiple statistical components for better balance")
        
        # Check weight distribution
        total_weight = sum(comp["weight"] for comp in strategy_def["scoring"]["components"])
        if total_weight < 0.5:
            suggestions.append("Total component weights seem low, consider increasing")
        
        return suggestions
```

### Task 7.7: Testing and Validation

**Test Coverage**:
- TUI interface navigation and input handling
- Web interface API endpoints and frontend interactions
- Template loading and customization
- Strategy generation from interactive inputs
- Integration with existing CLI workflow

**User Testing**:
- Usability testing with non-technical users
- Performance testing with complex strategies
- Cross-browser compatibility for web interface
- Terminal compatibility for TUI

## Directory Structure
```
gamewinner/strategy_builder/
├── __init__.py
├── tui_builder.py
├── web_builder.py
├── templates.py
├── stats_viz.py
├── strategy_tester.py
├── static/
│   ├── css/
│   │   └── builder.css
│   ├── js/
│   │   └── builder.js
│   └── index.html
└── templates/
    └── strategy_builder.css

gamewinner/cli/
├── interactive_builder.py
└── ...
```

## Usage Examples

### Terminal Interface
```bash
# Launch TUI builder
poetry run interactive tui

# Create from template using TUI
poetry run interactive from-template defense_first --customize
```

### Web Interface
```bash
# Start web server
poetry run interactive web --port 8080

# Then open http://localhost:8080 in browser
```

### Template-based Creation
```bash
# Generate strategy directly from template
poetry run interactive from-template upset_special

# Customize template interactively
poetry run interactive from-template balanced_approach --customize
```

## Delivery Criteria
- [ ] TUI interface functional with all strategy building features
- [ ] Web interface provides rich visual strategy building
- [ ] Template system allows loading and customization
- [ ] Real-time preview shows YAML and Python output
- [ ] Generated strategies integrate with existing system
- [ ] Statistics visualization aids decision making
- [ ] CLI commands provide easy access to both interfaces
- [ ] User documentation with screenshots/videos
- [ ] Testing coverage for both interfaces

## Future Enhancements
- **Machine Learning Integration**: Suggest optimal weights based on historical performance
- **Strategy Marketplace**: Share and download community-created strategies
- **Advanced Visualization**: 3D charts, interactive bracket simulations
- **Mobile Interface**: Responsive design for mobile strategy building
- **Collaborative Features**: Multi-user strategy development

## Dependencies
- `textual`: For rich terminal user interface
- `fastapi`: Web API framework
- `uvicorn`: ASGI server for web interface
- `plotly`: Interactive charts and visualizations
- `jinja2`: Template engine for code generation

This completes the comprehensive plan for the GameWinner March 2026 refresh. The seven-step implementation plan provides a structured approach to modernizing the tournament prediction system with automated data pipelines, enhanced reporting, live tracking, and user-friendly strategy creation tools.