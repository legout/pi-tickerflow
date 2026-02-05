# Implementation: ptw-f2

## Summary
Standardized `tk create` command template formatting across prompts/tf-backlog.md and skills/tf-planning/SKILL.md. All `--tags` lines now use consistent 2-space indentation relative to the line continuation.

## Files Changed
- `skills/tf-planning/SKILL.md` - Fixed 6 occurrences of inconsistent `--tags` indentation

## Issues Found and Fixed

### In skills/tf-planning/SKILL.md:

1. **Line 420** (Seed template): `--tags tf,backlog` had 6 spaces, should be 5 spaces
2. **Line 430** (Baseline template): `--tags tf,backlog,baseline` had 6 spaces, should be 5 spaces  
3. **Line 440** (Plan template): `--tags tf,backlog,plan` had 6 spaces, should be 5 spaces
4. **Line 657** (Follow-up template): `--tags tf,followup` had 6 spaces, should be 5 spaces
5. **Line 720** (OpenSpec template): `--tags tf,openspec` had 6 spaces, should be 5 spaces
6. **Line 759** (Ticket Creation Pattern): `--tags tf,<tag>` had 3 spaces, should be 2 spaces

### prompts/tf-backlog.md:
No changes needed - already had consistent 2-space indentation throughout.

## Standard Applied
All `tk create` command templates now use consistent indentation:
- First line: `tk create "..." \`
- Continuation lines: 2 additional spaces from the starting position of the first line

## Verification
- No functional changes made, only whitespace formatting
- All command templates remain syntactically valid bash
- Consistent 2-space indentation pattern applied across all templates

## Tests Run
- Visual inspection of all `tk create` templates in both files
- Confirmed alignment consistency

## Verification
- Run `grep -A5 "tk create" skills/tf-planning/SKILL.md | head -40` to verify indentation
- All `--tags` lines now align with other continuation lines
