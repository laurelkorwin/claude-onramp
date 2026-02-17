---
name: configure-permissions
description: View and configure your personal Claude Code permission profile. Shows what's blocked, what requires approval, and what's auto-approved. Lets you choose between cautious, standard, and open permission profiles.
disable-model-invocation: true
argument-hint: "[show | cautious | standard | open]"
---

Configure your personal Claude Code permissions.

## Steps

1. Parse `$ARGUMENTS` to determine the command:
   - Empty or missing → show help
   - `show` → display current permissions
   - `cautious` → apply cautious profile
   - `standard` → apply standard profile
   - `open` → apply open profile

2. Run the configure script:
   ```bash
   python3 "$CLAUDE_PROJECT_DIR/.claude/skills/configure-permissions/scripts/configure.py" "$CLAUDE_PROJECT_DIR" $ARGUMENTS
   ```

3. Relay the script's output to the user exactly as printed. Do not summarize or reformat it.

4. If the user ran a profile command (`cautious`, `standard`, or `open`), remind them:
   - Their personal settings are saved in `.claude/settings.local.json` (not shared with the team)
   - The project's deny rules in `settings.json` always apply on top
   - They can run `/configure-permissions show` to review their settings at any time
   - For a full explanation of what each rule means, see `.claude/PERMISSIONS.md`
