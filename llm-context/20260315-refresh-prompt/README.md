# gamewinner - March 2026 Refresh

This is the gamewinner repo. The top-level README will orient you to the project. It is the time of year when the basketball tournament starts, so we are aiming to implement a few improvements. The top priorities are:

1. Refreshing some key data, from the open internet, and ideally building a pipeline to do so semi-automated in future years. For all of these, we will need code that adds a new file, named for the current year, which matches (as closely as possible) the format of the corresponding files from previous years.
  * The tournament and team information, in YAML and CSV files, under `data/`. You can find this on public websites like ESPN.com or cbssports.com. You may even be able to get it via API from something like ESPN. 
  * The team statistics and metrics, in CSV files, under `gamewinner/strategies/mathstats/data`. This originally came from the blog of Evan Miya, at `https://evanmiya.com/?team_ratings`. This may require a subscription to access, but we can pay for that if needed. This may or may not have an API access option. 
    * Note that some of the categories and statistics on Evan Miya's current website may not exactly match the stats from previous years. You will probably need to make judgment calls as to what are the closest corresponding statistics. 
    * After doing this, we will need to update all of the relevant stategy files, so that they reference the correct statistics in the Evan Miya file for the current year.
2. Making it easier to render the strategies, particularly the ones in `gamewinner/strategies/mathstats/derived/`. 
    * Most simply, to be able to easily run a program like in `gamewinner/strategies/mathstats/derived/slotfire_steady.py`, on the updated data from the current year.
    * Be able to render a "report" of sorts, for a given strategy, similar to the ones posted at `https://github.com/ntbloom/gamewinner/issues/14` and `https://github.com/ntbloom/gamewinner/issues/9`
3. Some way to easily run the bracket results, as the tournament advances, to create simple "standings" like the ones in `https://github.com/ntbloom/gamewinner/issues/19`.
    * Ideally, be able to easily compare these against standings in manually-submitted brackets on various tournament sites like ESPN.com and Yahoo.
    * It would be awesome if this could run automatically in CI, pulling the results of the games each morning and refreshing the standings.
4. Some simple interface for building new strategies.
    * Ultimately, this will define an interface for humans to build a strategy (like those in `gamewinner/strategies/mathstats/derived/`), which can then be parsed and used to code-gen the actual `.py` file that defines the strategy.
    * This could be a simple data definition spec (in something like YAML), so that the human creates a new YAML, and feeds that to a program that parses it into code for the new strategy.
    * It could also be some kind of TUI or simple web-style app, that allows the human user to interactively build rules that get translated into code for the new strategy.
    * This functionality will also need to modify `gamewinner/strategies/__init__.py` (and maybe other files) to register the new strategies that are added.

I would like to address these in that order, though I'm open to doing it slightly differently, if that makes implementation easier or better in some way.

## Create plan `.md` files

Please look at the full list of priorities above, and make plans for how to implement them. You will save these plans to several markdown documents, under `llm-context/20260315-refresh-prompt/`. Each of these files should serve as a good starting point for an LLM to begin with implementing the described plan. Indicate the order that these files should be addressed by starting the filename with two digits, which will increment. 

Start with an overall, high-level plan, saved in `llm-context/20260315-refresh-prompt/00-plan.md`. Then begin adding files for each discrete step of the plan. For example, the next step would be saved in `llm-context/20260315-refresh-prompt/01-<name-of-step>.md`, where `<name-of-step>` is replaced by a short sensible name, the first two digits are incremented each time.
