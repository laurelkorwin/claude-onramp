# Claude Code Onramp

A ready-to-use configuration kit that makes [Claude Code](https://docs.anthropic.com/en/docs/claude-code) safe and approachable for people who aren't software engineers.

Claude Code is a powerful tool — it runs on your machine, can read and edit files, run commands, and interact with the internet. That power needs guardrails, especially for people who are still learning what those actions mean. This project provides those guardrails, along with a guided setup experience and a plain-language reference guide.

## What's included

| File | What it does |
|------|-------------|
| `CLAUDE.md` | Instructions Claude follows in this project. Requires plain-language explanations before every action. |
| `.claude/settings.json` | Security rules that can't be overridden — blocks access to secrets, force-pushes, and other dangerous operations. |
| `.claude/CHEATSHEET.html` | A visual, browser-friendly reference guide covering commands, concepts, models, and common situations. |
| `.claude/hooks/require-explanation.py` | An automated check that blocks Claude from acting unless it explains what it's about to do first. |
| `.claude/skills/setup/` | A guided first-time setup wizard (`/setup`) that walks users through permissions, model selection, and preferences. |
| `.claude/skills/configure-permissions/` | A permissions manager (`/configure-permissions`) for viewing and changing what Claude can do without asking. |

## Who this is for

- **Non-technical users** getting started with Claude Code for the first time
- **Teams** onboarding people with varying levels of technical experience
- **Educators** teaching responsible use of AI coding tools
- **Anyone** who wants a safer, more transparent Claude Code experience

## Getting started

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed on your machine
- A Claude API key or an Anthropic account with Claude Code access

### Setup

1. **Clone this repository:**
   ```
   git clone https://github.com/laurelkorwin/claude-onramp.git
   cd claude-onramp
   ```

2. **Open the project in Claude Code:**
   ```
   claude
   ```
   Or open the folder in VS Code with the Claude Code extension installed.

3. **Run the setup wizard:**
   ```
   /setup
   ```
   This walks you through everything step by step — permissions, model selection, and communication preferences. No technical knowledge required.

That's it. The safety rules in `.claude/settings.json` are active immediately. The `/setup` wizard handles everything else.

## How the safety system works

This project uses three layers of protection:

### 1. Blocked actions (can't be overridden)

Some actions are permanently blocked, no matter what. Claude cannot:

- Read or write files containing passwords, API keys, or secrets (`.env`, credentials, SSH keys, etc.)
- Force-push to git (which can erase code history)
- Run destructive commands like `rm -rf /*`
- Publish packages to the internet

These rules live in `.claude/settings.json` and apply to everyone using the project.

### 2. Permission levels (ask before acting)

Actions that aren't blocked fall into two categories:

- **Ask** — Claude requests permission each time (e.g., pushing code to GitHub, installing packages)
- **Allow** — Claude does it automatically (e.g., editing files, running project scripts)

You choose your comfort level during `/setup`. There are three built-in profiles:

| Profile | What Claude does automatically | What Claude still asks about |
|---------|-------------------------------|------------------------------|
| **Cautious** | Nothing — asks about everything | All actions |
| **Standard** | Edits files, runs project scripts | Internet actions, git push, installs |
| **Open** | Above + local git operations (commit, branch) | Pushes, installs |

Your personal permissions are saved in `.claude/settings.local.json`, which is not shared with others.

### 3. Plain-language explanations

Before Claude takes any action that requires your permission, it's required to explain:

- What it's about to do
- What data is involved
- Whether it's reversible
- Whether anything leaves your machine

This is enforced by an automated hook (`.claude/hooks/require-explanation.py`) that blocks the action if no explanation is provided. You can turn this off during `/setup` if you find it repetitive.

## The cheatsheet

Open `.claude/CHEATSHEET.html` in your browser for a visual reference guide that covers:

- **Essential commands** — `/help`, `/clear`, `/compact`, `/cost`, `/model`, and undo (`Esc Esc`)
- **Key concepts** — context window, skills, hooks, persistent memory, checkpoints
- **Models** — when to use Opus (thorough), Sonnet (balanced), or Haiku (fast)
- **Permissions** — how deny, ask, and allow work together
- **Common situations** — what to do when Claude is slow, you want to undo something, or you're unsure if an action is safe

The cheatsheet updates over time as you work with Claude — it will ask before adding new entries.

## Customizing for your team

This project is designed to be forked and adapted:

- **`CLAUDE.md`** — Edit the transparency guidelines to match your team's needs. These are the instructions Claude follows in every conversation.
- **`.claude/settings.json`** — Add or remove deny/ask rules for your organization's security requirements.
- **`.claude/skills/`** — Add new skills (custom commands) for workflows specific to your team.
- **`.claude/hooks/`** — Add automated checks that run when Claude takes certain actions.

Personal settings (`.claude/settings.local.json`) are per-user and should be added to `.gitignore`.

## Commands reference

| Command | What it does |
|---------|-------------|
| `/setup` | Guided first-time setup wizard |
| `/configure-permissions` | View or change permission profiles |
| `/help` | See all available commands |
| `/model` | Switch between Claude models mid-conversation |
| `/compact` | Free up conversation space when things slow down |
| `/clear` | Start a fresh conversation |
| `/cost` | Check token usage and spending for this session |
| `Esc Esc` | Undo — rewind code changes, conversation, or both |

## Project structure

```
claude-onramp/
├── CLAUDE.md                        # Instructions Claude follows
├── README.md                        # This file
└── .claude/
    ├── settings.json                # Security rules (shared, not overridable)
    ├── settings.local.json          # Personal preferences (not shared)
    ├── CHEATSHEET.html              # Visual reference guide
    ├── PERMISSIONS.md               # Permission rules reference
    ├── hooks/
    │   └── require-explanation.py   # Enforces plain-language explanations
    └── skills/
        ├── setup/
        │   └── SKILL.md             # Setup wizard definition
        └── configure-permissions/
            ├── SKILL.md             # Permissions manager definition
            └── scripts/
                └── configure.py     # Permission profile engine
```

## License

MIT — see [LICENSE](LICENSE) for details.
