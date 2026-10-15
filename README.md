# MJR Today in History

This repository is the permanent home for MJR's curated Today in History editorial data.

## Current status

- `data/history.json` contains **17 draft entries across October 16 and 17**. They require editorial fact-checking before production use.
- Other calendar dates are **not yet curated**. Do not present this as a complete year-round database.
- The working Prep Now HTML widget remains unchanged and continues to use Wikipedia.

## Editorial guidelines

- Aim for 10–15 strong, recognizable events per date, without padding.
- Prioritize major U.S. and world history, science, technology, sports, and interesting unusual events. Entertainment is welcome when significant; dedicated music history is covered elsewhere in Prep Now.
- Write concise conversational radio copy, with a bold year followed by a hyphen in the display widget.
- Avoid obscure milestones and duplicate events. Fact-check event date and description before changing `status` to `approved`.

## Integration plan

Once enough dates are approved, host the JSON through GitHub Pages and update the Prep Now widget to use approved curated entries with Wikipedia as fallback. Test separately before replacing the working HTML code.
