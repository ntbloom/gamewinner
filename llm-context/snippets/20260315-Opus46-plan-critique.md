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