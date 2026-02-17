#!/usr/bin/env python3
"""
PermissionRequest hook that enforces plain-language explanations.

When Claude Code is about to ask the user for permission to run a tool,
this hook checks whether Claude already provided a [permission_explanation]
tagged explanation. If not, it denies the request and tells Claude to explain first.
"""

import json
import sys


def get_last_assistant_text(transcript_path):
    """Read the transcript and return the text content of the last assistant message."""
    last_text = ""
    try:
        with open(transcript_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg = entry.get("message", {})
                if msg.get("role") != "assistant":
                    continue

                content = msg.get("content", [])
                if isinstance(content, str):
                    last_text = content
                    continue

                # Content is a list of blocks — extract text blocks
                text_parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                if text_parts:
                    last_text = "\n".join(text_parts)
    except (FileNotFoundError, PermissionError):
        # If we can't read the transcript, don't block the action
        return None

    return last_text


def main():
    hook_input = json.loads(sys.stdin.read())
    transcript_path = hook_input.get("transcript_path", "")
    tool_name = hook_input.get("tool_name", "")

    # Only enforce for tools that warrant an explanation
    skip_tools = {"Read", "Glob", "Grep", "TodoRead", "TodoWrite", "TaskCreate",
                  "TaskUpdate", "TaskGet", "TaskList", "AskUserQuestion"}
    if tool_name in skip_tools:
        sys.exit(0)

    last_text = get_last_assistant_text(transcript_path)

    # If we couldn't read the transcript, don't block
    if last_text is None:
        sys.exit(0)

    # Check for the explanation marker
    if "[permission_explanation]" in last_text:
        sys.exit(0)

    # No explanation found — deny and ask Claude to explain
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {
                "behavior": "deny",
                "message": (
                    "You must explain this action to the user in plain language "
                    "before running it. Start with the tag [permission_explanation] "
                    "on its own line, then explain: what you're about to do, what "
                    "data is involved, whether it's reversible, and whether anything "
                    "leaves the machine. Then try again."
                )
            }
        }
    }
    json.dump(result, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()
