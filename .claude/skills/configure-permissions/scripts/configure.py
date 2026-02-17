#!/usr/bin/env python3
"""
View and configure personal Claude Code permission profiles.

Reads the team settings from settings.json (deny/ask rules) and manages
personal settings in settings.local.json (allow rules). Never modifies
settings.json.

Usage:
  python3 configure.py <project_dir>              # Show help
  python3 configure.py <project_dir> show          # Show current permissions
  python3 configure.py <project_dir> cautious      # Apply cautious profile
  python3 configure.py <project_dir> standard      # Apply standard profile
  python3 configure.py <project_dir> open           # Apply open profile
"""

import argparse
import json
import os
import sys


# ---------------------------------------------------------------------------
# Profile definitions
# ---------------------------------------------------------------------------

PROFILES = {
    "cautious": {
        "description": "Ask me about everything",
        "detail": (
            "Claude asks before every non-read action. "
            "Best for first-time users, unfamiliar projects, or high-security work."
        ),
        "allow": [],
    },
    "standard": {
        "description": "Auto-approve routine local work",
        "detail": (
            "Claude can edit project files and run project scripts without asking. "
            "Still asks for network requests, git operations, and package installs. "
            "Best for day-to-day project work."
        ),
        "allow": [
            "Edit(**)",
            "Write(**)",
            "Bash(npm run *)",
            "Bash(npx *)",
            "Bash(node *)",
            "Bash(python3 *)",
            "Bash(python *)",
        ],
    },
    "open": {
        "description": "Auto-approve most project work, ask before leaving my machine",
        "detail": (
            "Everything in Standard, plus local git operations (add, commit, branch, checkout, status, log, diff). "
            "Still asks before git push, package installs, and all network requests. "
            "Nothing crosses the machine boundary without asking. "
            "Best for experienced users who want flow."
        ),
        "allow": [
            "Edit(**)",
            "Write(**)",
            "Bash(npm run *)",
            "Bash(npx *)",
            "Bash(node *)",
            "Bash(python3 *)",
            "Bash(python *)",
            "Bash(git add *)",
            "Bash(git commit *)",
            "Bash(git status*)",
            "Bash(git log*)",
            "Bash(git diff*)",
            "Bash(git checkout *)",
            "Bash(git branch *)",
        ],
    },
}


# ---------------------------------------------------------------------------
# Plain-language translation tables
# ---------------------------------------------------------------------------

DENY_TRANSLATIONS = [
    # (pattern_substring, plain_language)
    # Order matters — first match wins and deduplicates, so Bash patterns
    # (which are unique per rule) come before path patterns (which repeat
    # across Read/Write/Edit and should collapse into one line).
    ("git push --force", "Force-push to git (can destroy remote history)"),
    ("git push * --force", "Force-push to git with branch (can destroy remote history)"),
    ("rm -rf /*", "Catastrophic deletion (rm -rf /*)"),
    ("npm publish", "Publish packages (npm publish)"),
    (".env", "Read or write .env files (protects API keys and secrets)"),
    ("*secret*", 'Read or write files with "secret" in the name'),
    ("*credential*", 'Read or write files with "credential" in the name'),
    ("*password*", 'Read or write files with "password" in the name'),
    ("~/.ssh/", "Access SSH keys (~/.ssh/)"),
    ("~/.aws/", "Access cloud credentials (~/.aws/)"),
    ("~/.config/gh/", "Access GitHub tokens (~/.config/gh/)"),
    ("*.pem", "Read or write certificate files (*.pem)"),
    ("*.key", "Read or write key files (*.key)"),
]

ASK_TRANSLATIONS = [
    ("git push", "Push code to GitHub (git push)"),
    ("npm install", "Install npm packages (npm install)"),
    ("pip install", "Install Python packages (pip install)"),
    ("pip3 install", "Install Python packages (pip3 install)"),
    ("brew install", "Install Homebrew packages (brew install)"),
]

ALLOW_TRANSLATIONS = [
    ("Edit(**)", "Edit any file in the project"),
    ("Write(**)", "Create or overwrite any file in the project"),
    ("Bash(npm run *)", "Run npm scripts (npm run)"),
    ("Bash(npx *)", "Run npx commands"),
    ("Bash(node *)", "Run Node.js scripts"),
    ("Bash(python3 *)", "Run Python 3 scripts"),
    ("Bash(python *)", "Run Python scripts"),
    ("Bash(git add *)", "Stage files for commit (git add)"),
    ("Bash(git commit *)", "Save code snapshots locally (git commit)"),
    ("Bash(git status*)", "Check git status"),
    ("Bash(git log*)", "View git history"),
    ("Bash(git diff*)", "View code changes (git diff)"),
    ("Bash(git checkout *)", "Switch branches (git checkout)"),
    ("Bash(git branch *)", "Manage branches (git branch)"),
]


def translate_rules(rules, translation_table):
    """Translate permission rules to plain English using the lookup table."""
    seen = set()
    translated = []
    for rule in rules:
        matched = False
        for pattern, description in translation_table:
            if pattern in rule:
                matched = True
                if description not in seen:
                    seen.add(description)
                    translated.append(description)
                break
        if not matched:
            # No translation found — show the raw rule
            if rule not in seen:
                seen.add(rule)
                translated.append(rule)
    return translated


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def read_settings(project_dir, filename):
    """Read a settings JSON file, returning empty dict if missing."""
    path = os.path.join(project_dir, ".claude", filename)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_local_settings(project_dir, data):
    """Write settings.local.json with 2-space indent."""
    path = os.path.join(project_dir, ".claude", "settings.local.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_help():
    """Show help with profile descriptions."""
    print("=== Configure Permissions ===")
    print()
    print("Choose a profile to control how much Claude asks before acting.")
    print("Profiles set your personal settings (settings.local.json).")
    print("The project's security rules (settings.json) always apply on top.")
    print()
    print("Usage:")
    print("  /configure-permissions show       Show your current permissions")
    print("  /configure-permissions cautious    Apply the Cautious profile")
    print("  /configure-permissions standard    Apply the Standard profile")
    print("  /configure-permissions open         Apply the Open profile")
    print()
    print("Profiles:")
    print()
    for name, profile in PROFILES.items():
        label = f"  {name.upper()} — \"{profile['description']}\""
        print(label)
        print(f"    {profile['detail']}")
        print()
    print("For a full explanation of permissions, see .claude/PERMISSIONS.md")


def cmd_show(project_dir):
    """Show current team and personal permissions in plain language."""
    team = read_settings(project_dir, "settings.json")
    personal = read_settings(project_dir, "settings.local.json")

    team_perms = team.get("permissions", {})
    personal_perms = personal.get("permissions", {})

    deny_rules = team_perms.get("deny", [])
    ask_rules = team_perms.get("ask", [])
    allow_rules = personal_perms.get("allow", [])

    print("=== Your Current Permissions ===")
    print()
    print("PROJECT DEFAULTS (shared in settings.json)")
    print("These are the recommended security baseline for this project.")
    print("They can be changed by editing .claude/settings.json directly,")
    print("but you should understand what each rule protects before removing it.")
    print()

    if deny_rules:
        print("  Blocked:")
        for desc in translate_rules(deny_rules, DENY_TRANSLATIONS):
            print(f"  - {desc}")
    else:
        print("  Blocked: (none)")

    print()

    if ask_rules:
        print("  Requires your approval each time:")
        for desc in translate_rules(ask_rules, ASK_TRANSLATIONS):
            print(f"  - {desc}")
    else:
        print("  Requires your approval each time: (none)")

    print()
    print("YOUR PERSONAL SETTINGS (in settings.local.json — just for you)")
    print()

    if allow_rules:
        print("  Auto-approved:")
        for desc in translate_rules(allow_rules, ALLOW_TRANSLATIONS):
            print(f"  - {desc}")
    else:
        print("  Auto-approved: (none)")

    print()
    print("To change your personal settings: /configure-permissions cautious | standard | open")
    print("To understand the project defaults: see .claude/PERMISSIONS.md")


def cmd_apply_profile(project_dir, profile_name):
    """Apply a permission profile to settings.local.json."""
    profile = PROFILES[profile_name]

    # Read current personal settings to show diff
    current = read_settings(project_dir, "settings.local.json")
    current_allow = current.get("permissions", {}).get("allow", [])
    new_allow = profile["allow"]

    # Build the new settings.local.json
    new_settings = {}
    if new_allow:
        new_settings["permissions"] = {"allow": new_allow}
    else:
        new_settings["permissions"] = {"allow": []}

    # Show what's changing
    print(f"=== Applying {profile_name.upper()} profile ===")
    print(f'"{profile["description"]}"')
    print()

    if current_allow == new_allow:
        print("No changes needed — you're already using this profile.")
        print()
    else:
        # Show removals
        removed = [r for r in current_allow if r not in new_allow]
        added = [r for r in new_allow if r not in current_allow]

        if removed:
            print("Removing auto-approvals:")
            for desc in translate_rules(removed, ALLOW_TRANSLATIONS):
                print(f"  - {desc}")
            print()

        if added:
            print("Adding auto-approvals:")
            for desc in translate_rules(added, ALLOW_TRANSLATIONS):
                print(f"  + {desc}")
            print()

        write_local_settings(project_dir, new_settings)
        print("Saved to .claude/settings.local.json")
        print()

    if new_allow:
        print("Your auto-approved actions:")
        for desc in translate_rules(new_allow, ALLOW_TRANSLATIONS):
            print(f"  - {desc}")
    else:
        print("Auto-approved actions: (none)")
        print("Claude will ask before every non-read action.")

    print()
    print("Project deny rules still apply — see /configure-permissions show for full details.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="View and configure Claude Code permission profiles."
    )
    parser.add_argument("project_dir", help="Path to the project directory")
    parser.add_argument(
        "action",
        nargs="?",
        default="help",
        choices=["help", "show", "cautious", "standard", "open"],
        help="Command to run (default: help)",
    )
    args = parser.parse_args()

    if args.action == "help":
        cmd_help()
    elif args.action == "show":
        cmd_show(args.project_dir)
    elif args.action in PROFILES:
        cmd_apply_profile(args.project_dir, args.action)


if __name__ == "__main__":
    main()
