{
  "permissions": {
    "deny": [
      "Read(.env*)",
      "Read(**/.env*)",
      "Write(.env*)",
      "Write(**/.env*)",
      "Edit(.env*)",
      "Edit(**/.env*)",
      "Read(**/*secret*)",
      "Read(**/*credential*)",
      "Read(**/*password*)",
      "Write(**/*secret*)",
      "Write(**/*credential*)",
      "Write(**/*password*)",
      "Edit(**/*secret*)",
      "Edit(**/*credential*)",
      "Edit(**/*password*)",
      "Read(~/.ssh/**)",
      "Write(~/.ssh/**)",
      "Edit(~/.ssh/**)",
      "Read(~/.aws/**)",
      "Write(~/.aws/**)",
      "Edit(~/.aws/**)",
      "Read(~/.config/gh/**)",
      "Write(~/.config/gh/**)",
      "Edit(~/.config/gh/**)",
      "Read(**/*.pem)",
      "Read(**/*.key)",
      "Write(**/*.pem)",
      "Write(**/*.key)",
      "Edit(**/*.pem)",
      "Edit(**/*.key)",
      "Bash(git push --force*)",
      "Bash(git push * --force*)",
      "Bash(rm -rf /*)",
      "Bash(npm publish*)"
    ],
    "ask": [
      "Bash(git push*)",
      "Bash(npm install*)",
      "Bash(pip install*)",
      "Bash(pip3 install*)",
      "Bash(brew install*)"
    ]
  },
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/require-explanation.py\""
          }
        ]
      }
    ]
  }
}
