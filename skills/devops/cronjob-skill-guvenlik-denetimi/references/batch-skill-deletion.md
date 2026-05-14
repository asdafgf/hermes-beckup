# Batch Skill Deletion — 14 May 2026

## The Problem

Garbage skills (John Hammond transcript artifacts) cannot be deleted in batch via the CLI because:

- `hermes skills uninstall <name>` requires interactive confirmation(y/N) — even `--yolo` flag doesn't bypass it
- 465+ skills to delete individually via `skill_manage(action='delete')` would require ~465 tool calls
- Many garbage skills don't exist as physical directories — they're hub-installed/imported artifacts that only exist in the skills list

## What DOES NOT Work

```bash
hermes skills uninstall "skill-name"        # asks for confirmation
hermes --yolo skills uninstall "skill-name" # still asks for confirmation
hermes skill remove "skill-name"            # 'skill' is not a valid command
```

## What DOES Work

`skill_manage(action='delete', name='skill-adi')` — this is the tool-level API that bypasses CLI confirmation.

But it only works one skill at a time. For batch deletion:
1. Write a Python script that reads the skills list and calls the equivalent via subprocess/hermes CLI — BUT this fails because the CLI always confirms
2. The only viable path is sequential `skill_manage` calls — accept that 400+ deletions will take multiple sessions

## Conservative Filtering Lesson

When filtering garbage skills, we initially flagged valid skills like:
- `windows-allow-once-otomatik` — valid Windows automation skill
- `windows-c-junction-fix` — valid path fix skill
- `windows-terminal-hata-cozumu` — valid troubleshooting skill
- `cloudflare-browser-bypass` — valid Cloudflare skill

The original prefix-based filter was too aggressive. Solution: use multi-level filtering:
1. First pass: prefix match (catches obvious transcript artifacts)
2. Second pass: exclude any skill that has a legit category assigned
3. Third pass: exclude any skill whose description is >20 chars and contains meaningful content (not just repeating transcript)
