# 20260315 Opus46 critique of Sonnet plan

Claude Opus 4.6 was given the following prompt, asked to assess the state of the repo at fe0558fdc7f191ce08b6825ddcef85b3c92d3d39; the plan made by Sonnet 4.

> Hello. Please take a look at the prompt in `llm-context/20260315-refresh-prompt/README.md`. Then peruse the other markdown files in that same directory. These were created by another LLM. Look over these and make any edits that you would like to refine the plan. If you would prefer to delete these files and replace them with a fresh plan, that is also fine. All of this is committed to version control already, so any file can be modified, deleted or renamed as needed.

## Opus 4.6 response 

_After reading a bunch of files..._

Now I have a thorough understanding of the codebase and the proposed plans. Let me summarize my observations and then make edits.

Key findings from the codebase:

1. Column naming changed between 2023→2024: The 2023 CSV has headers like name,Rank,OBPR,DBPR,BPR,...,ResumeRank,HomeRank while the 2024 CSV has rank,team,obpr,dbpr,bpr,opponent_adjust,pace_adjust,...,wins,losses. The 2024 format added opponent_adjust, pace_adjust, wins, losses and dropped ResumeRank.

2. The imathstats.py parser is column-order-based, not header-based — it uses positional unpacking from CSV rows. This is a critical detail the plans miss.

3. The 2023 CSV has 16 columns, 2024 has 20 columns — already a breaking change handled by code updates. The MSProps NamedTuple matches the 2024 format.

4. The existing strategies use MSProps field names (like rank_defense, obj_kills_concede_per_game), not the CSV column headers directly.

5. Team name resolution uses alternate_names.py with get_definitive_name() — this is important and the plans underestimate how central it is.

6. There's no data/2022.yaml — only 2023 and 2024 YAMLs exist, plus a template.

7. The plans contain many factual errors — e.g., claiming columns like runs_per_game when the actual CSV headers are different, inventing non-existent structures, and hallucinating API designs that don't match the codebase's simplicity.

Let me now rewrite the plan files with accurate, grounded content:

... 

_After making a bunch of changes, captured in the next commit..._

Here's a summary of what I did and why:

Summary of Changes
I rewrote all 8 plan files (00-07) to be grounded in the actual codebase rather than speculative/hallucinated. The original plans were ~3,500 lines of mostly fabricated code examples, invented APIs, and incorrect assumptions. The new plans are ~1,100 lines of accurate, actionable guidance.

Key problems fixed across all files:

1. CSV parsing is positional, not header-based — The original plans assumed csv.DictReader/pandas and talked about "column references" as string lookups. In reality, imathstats.py uses tuple unpacking with exact positional destructuring of 20 columns. This is the single most critical architectural detail for Steps 02-03.

2. MSProps NamedTuple is the API boundary — Strategies access data through MSProps field names (like rank_defense, raw_overall), not CSV column names. The original plans confused these layers.

3. 2023→2024 migration already happened — The plans didn't acknowledge that column changes were already handled once. This precedent (e.g., resume_rank kept with default=-1) is the template for handling 2026 changes.

4. Team name system via alternate_names.py — The original plans invented separate "alias systems" when the codebase already has a comprehensive one.

5. CLI uses Typer, not Click — Multiple plan files showed Click-based code. The actual CLI uses Typer.

6. Scope right-sizing — The originals proposed: PDF exporters, Flask/FastAPI web servers, Plotly charts, Slack/Discord notification systems, pydantic schemas, Jinja2 templates, genetic algorithms, strategy marketplaces, mobile interfaces, etc. None of this matches the project's lightweight, single-purpose character. The rewrites propose proportionate solutions.

**Per-file changes:**

| File | Before | After | Key Change |
|------|--------|-------|------------|
| 00-plan | Generic overview | Documents actual architecture (positional CSV parsing, MSProps, etc.) |
| 01-tournament | Invented APIs, validation frameworks | Focuses on exact YAML/CSV format with real examples |
| 02-evan-miya | pandas, DictReader, subscription budgets | Documents exact 20-column format with positional mapping table |
| 03-strategy-updates | Invented AdaptiveTeamProperties, column mapping scripts | Three clear scenarios (columns changed, backward compat, new teams) |
| 04-rendering | Reporting framework, PDF/HTML exporters, Plotly | One new markdown printer + a comparison script |
| 05-tracking | Flask dashboard, notification system, CI pipeline | Simple results YAML file + scoring script |
| 06-yaml-builder | 650-line Jinja2/pydantic/Click framework | 195-line plan for a single-file YAML→Python converter |
| 07-interactive | 812-line React/FastAPI/Textual mega-plan | 100-line suggestion for simple CLI prompts |
