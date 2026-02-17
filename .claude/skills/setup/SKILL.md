---
name: setup
description: Guided first-time setup for non-technical users. Walks through what Claude Code is, how to stay safe, and configures permissions, model, and output style.
argument-hint: ""
---

Walk a non-technical user through Claude Code setup, step by step. Use `AskUserQuestion` for each decision point. Write all configuration to `.claude/settings.local.json` (personal, not shared).

**Tone:** Friendly, plain language, no jargon. Explain every concept before asking the user to make a choice. Keep explanations short — 2-3 sentences max per concept.

---

## Step 1: Welcome and orientation

Print the following (adapt lightly if needed, but keep the substance):

```
Welcome to Claude Code!

Claude Code is different from the Claude you might use in a browser.
It runs on your machine, which means it can read your files, run commands,
and make changes to your project. That makes it very powerful — and it's
why we'll set up some safety guardrails now.

Here's what Claude Code can do that browser Claude can't:
- See and edit files in your project
- Run commands in your terminal
- Search the web for answers
- Track changes with git
- Remember things about your project across sessions
```

---

## Step 2: Your safety net

Print the following:

```
Before we configure anything, here's the most important thing to know:

You can always undo. Claude Code automatically saves a snapshot of your
code before every change. If something goes wrong, press Esc twice (or
type /rewind) to go back to any previous point.

Think of it like infinite undo — you can restore your code, your
conversation, or both. So don't worry about getting anything wrong
during this setup. You can always change it later.
```

---
## Step 2.5 Pause for user input
Print the following:
```
Any questions before we get started configuring your setup?
```

**STOP HERE. Do not call any tools or produce any further output until the user sends a message.** If they have questions, answer them. If they say they're ready (or anything like "no", "nope", "let's go", etc.), continue to Step 3.


## Step 3: Permissions

Print:

```
Permissions control what Claude can do without asking you first. There
are actions Claude is blocked from entirely (like touching passwords or
force-pushing code), and actions where Claude will ask your permission
each time (like pushing code to GitHub or installing packages).

On top of those safety rules, you can choose how much Claude asks about
everyday work — editing files, running scripts, etc.

This project already has safety rules that can't be overridden. 

Claude is permanently blocked from:
- Accessing passwords, secret keys, and other sensitive files on your machine
- Actions that could cause serious damage, like overwriting code history or publishing your project to the internet

Separately, Claude will always ask your permission before uploading code to GitHub or downloading new software.

These rules apply no matter which option you choose next.

Make sense? If so, we can proceed.
```

**STOP HERE. Do not call any tools or produce any further output until the user sends a message.** If they have questions, answer them. If they say they're ready (or anything like "makes sense", "yes", "got it", etc.), continue with the `AskUserQuestion` below.

Use `AskUserQuestion` with these options:

**Question:** "How much should Claude ask before acting?"
**Options:**
1. **Cautious** — "Claude asks before every action. Best if you're new to this."
2. **Standard (Recommended)** — "Claude edits project files and runs project scripts without asking. Still asks before anything touches the internet. Doesn't touch "
3. **Open** — "Claude also handles local git operations (commit, branch, etc.) without asking. Still asks before pushing code or installing packages."
4. **Custom** — "Describe what you want in your own words and I'll set it up."

**If Cautious, Standard, or Open:** Run the configure script:
```bash
python3 "$CLAUDE_PROJECT_DIR/.claude/skills/configure-permissions/scripts/configure.py" "$CLAUDE_PROJECT_DIR" <profile>
```

**If Custom:** Ask the user to describe what they want in plain language (e.g., "I want Claude to edit files but always ask before running any command" or "Auto-approve everything except network requests"). Then:
1. Translate their description into permission allow rules using the pattern syntax from `PERMISSIONS.md`
2. Show the user what rules you'd write, explained in plain language
3. Ask for confirmation before writing
4. Write the rules to `.claude/settings.local.json` under `permissions.allow`

After setting permissions, briefly confirm what was set.

---

## Step 4: Safety preferences

Print:

```
This project has an extra safety feature: before Claude takes any action
that needs your permission, it's required to explain what it's about to
do in plain language — what it will touch, whether it's reversible, and
whether anything leaves your machine.

This is helpful when you're learning, but can feel repetitive once you're
comfortable.

Next, you can choose whether you want to keep this setting or not. You can disable it at any time by running the /setup command again.

Let me know when you're ready to continue.
```

**STOP HERE. Do not call any tools or produce any further output until the user sends a message.** If they have questions, answer them. If they say they're ready (or anything like "ready", "yes", "continue", etc.), continue with the `AskUserQuestion` below.

Use `AskUserQuestion`:

**Question:** "Do you want Claude to explain each action before asking permission?"
**Options:**
1. **Yes, keep explanations (Recommended)** — "Claude explains every new action in plain language before doing it."
2. **No, skip explanations** — "Claude still asks permission, but without the detailed explanation."

**If Yes:** No changes needed — the hook is already active.

**If No:** Edit `.claude/hooks/require-explanation.py` to disable it. Replace the body of the `main()` function with just `sys.exit(0)`, commenting out the original code. Specifically:
- Read the file
- Comment out lines 52-88 (everything in `main()` after `hook_input = ...` through the `json.dump`)
- Replace with `sys.exit(0)` so the hook runs but does nothing
- Tell the user: "Disabled. Claude will still ask permission for actions not in your allow list, but won't include the detailed explanation. You can re-enable this anytime by running /setup again."

---

## Step 5: Model selection

Print:

```
Claude comes in different versions — think of them as different modes:

You can switch models anytime during a conversation by typing /model.
You can also use faster models for quick subtasks (Claude does this
automatically sometimes).

Before we display and set the available models, do you have any questions?
```

**STOP HERE. Do not call any tools or produce any further output until the user sends a message.** If they have questions, answer them. If they say they're ready (or anything like "no", "nope", "let's go", etc.), continue with the `AskUserQuestion` below.

Use `AskUserQuestion`:

**Question:** "Which model do you want to use by default?"
**Options:**
1. **Sonnet — Balanced (Recommended)** — "Good at most tasks, reasonable speed and cost. Best default for most people."
2. **Opus — Thorough** — "Most capable. Better for complex, multi-step work. Slower and costs more."
3. **Haiku — Fast** — "Quick and cheap. Good for simple questions and small edits. Less thorough."

Write the chosen model to `.claude/settings.local.json` under `model`:
- Sonnet: `"claude-sonnet-4-5-20250929"`
- Opus: `"claude-opus-4-6"`
- Haiku: `"claude-haiku-4-5-20251001"`

Merge this into the existing `settings.local.json` — don't overwrite permissions or other settings already written in earlier steps.

---

## Step 6: Output style

Print:

```
Next, you can adjust how Claude communicates — more detailed explanations or
shorter, to-the-point answers.

You can also work with Claude to create a custom output style, if you'd like. 
I'd recommend doing this after trying one of the pre-baked ones and getting a feel for what you like and wish to change.

Make sense?
```

**STOP HERE. Do not call any tools or produce any further output until the user sends a message.** If they have questions, answer them. If they say they're ready (or anything like "makes sense", "yes", "sure", etc.), continue with the `AskUserQuestion` below.

Use `AskUserQuestion`:

**Question:** "How should Claude communicate with you?"
**Options:**
1. **Explanatory (Recommended)** — "More context, explains reasoning, better for learning."
2. **Concise** — "Shorter answers, less explanation, faster to read."

Write the chosen style to `.claude/settings.local.json` under `outputStyle`:
- Explanatory: `"Explain your reasoning. Use plain language. When introducing a concept, briefly define it."`
- Concise: `"Be concise and direct. Skip explanations unless asked."`

Merge into existing `settings.local.json`.

---

## Step 7: Summary

Print a personalized summary based on their choices. Format:

```
=== You're all set! ===

Here's what we configured:

  Permissions:    <profile name> — <one-line description>
  Explanations:   <On/Off>
  Default model:  <model name> — <one-line description>
  Output style:   <style> — <one-line description>

All saved to .claude/settings.local.json (personal, not shared).
The project's safety rules in settings.json always apply on top.
You can re-run /setup anytime to change these.

Commands worth knowing:
  Esc Esc     Go back — undo code changes, conversation, or both
  /compact    Free up conversation space when things slow down
  /cost       Check how much you've spent this session
  /clear      Start a completely fresh conversation
  /model      Switch between fast/balanced/thorough models mid-conversation
  /help       See all available commands

For more details, see:
  .claude/CHEATSHEET.html  Plain-language guide to all commands and concepts (open in browser)
  .claude/PERMISSIONS.md   How permissions work and what's blocked
```
