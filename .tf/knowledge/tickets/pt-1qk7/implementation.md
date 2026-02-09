# Implementation: pt-1qk7

## Summary
Added `tf-followups-scan` prompt to the install manifest. The settings.json registry entry was already present.

## Files Changed
- `config/install-manifest.txt` - Added `prompts/tf-followups-scan.md` entry

## Key Decisions
- Inserted the entry in alphabetical order alongside other `tf-followups*` entries
- No formatting tools needed (plain text manifest)

## Verification
```bash
$ grep tf-followups config/install-manifest.txt
prompts/tf-followups.md
prompts/tf-followups-scan.md
```

## Acceptance Criteria Status
- [x] Add `"tf-followups-scan": "planning"` to `.tf/config/settings.json` under `prompts` - **Already present**
- [x] Ensure prompt file is included in `config/install-manifest.txt` - **Added**
- [x] Run formatting on edited files - **Not applicable (text file)**
