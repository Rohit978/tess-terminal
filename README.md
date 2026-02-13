# 🤖 TESS Terminal - Configurable Edition

A **standalone, user-configurable** terminal AI agent that puts you in control. No hardcoded secrets, no complex setup—just a clean, interactive configuration experience.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/install-pip-blue.svg)](#installation)

---

## ✨ Features

- **🔧 Interactive Setup Wizard** - Configure everything through a beautiful TUI
- **🔑 Secure API Key Management** - Local storage with proper permissions
- **🔄 Multi-Provider Support** - Groq, OpenAI, DeepSeek, Gemini with automatic failover
- **🛡️ Configurable Security** - Choose your security level (LOW/MEDIUM/HIGH)
- **📊 Settings Menu** - Change configuration anytime without editing files
- **💬 Natural Language** - Control your computer with plain English
- **⚡ Extensible** - Easy to add new capabilities

---

## 🚀 Installation

### Option 1: Install from GitHub (Recommended)

```bash
pip install git+https://github.com/YOUR_USERNAME/tess-terminal.git
```

### Option 2: Clone and Install

```bash
git clone https://github.com/YOUR_USERNAME/tess-terminal.git
cd tess-terminal
pip install -e .
```

### Option 3: Download ZIP

1. Download and extract this repository
2. `cd tess-terminal`
3. `pip install -e .`

---

## 🎯 Quick Start

### 1. Configure

```bash
tess --setup
```

This interactive wizard will:
- Help you get a free API key
- Set your security preferences
- Configure optional features

### 2. Run

```bash
# Interactive mode
tess

# Or execute a single command
tess "open chrome"
tess "list files in downloads"
```

---

## 📖 Usage

### Interactive Mode

```
$ tess

┌─────────────────────────────────┐
│     TESS Terminal               │
│     Configurable Edition        │
├─────────────────────────────────┤
│  Provider: GROQ                 │
│  Model: llama-3.3-70b-versatile │
│  Security: MEDIUM               │
└─────────────────────────────────┘

Type 'help' for commands, 'exit' to quit

You: open notepad
[TESS] Launched notepad

You: take a screenshot
[TESS] Screenshot saved to Desktop

You: search for python tutorials
[TESS] Searching: python tutorials
```

### Special Commands

| Command | Description |
|---------|-------------|
| `help` | Show help message |
| `config` | Open settings menu |
| `history` | Show conversation history |
| `status` | Show system status |
| `clear` | Clear screen |
| `!command` | Execute shell command directly |
| `exit` / `quit` | Exit TESS |

### CLI Options

```bash
tess --setup          # Run configuration wizard
tess --settings       # Open settings menu
tess --reset          # Reset to defaults
tess --version        # Show version
tess "your command"   # Execute single command
```

---

## 🔑 Getting API Keys (FREE)

TESS works with multiple LLM providers. **Groq is recommended** (free & fast):

| Provider | Get Key | Free Tier |
|----------|---------|-----------|
| **Groq** ⭐ | [console.groq.com/keys](https://console.groq.com/keys) | ✅ $200/month |
| **Gemini** | [aistudio.google.com](https://aistudio.google.com/app/apikey) | ✅ Generous |
| **DeepSeek** | [platform.deepseek.com](https://platform.deepseek.com/api_keys) | ✅ Available |
| **OpenAI** | [platform.openai.com](https://platform.openai.com/api-keys) | ❌ Paid |

> 💡 **Tip**: Add multiple keys for automatic failover!

---

## ⚙️ Configuration

Settings are stored in:
- **Windows**: `%USERPROFILE%\.tess\config.json`
- **macOS/Linux**: `~/.tess/config.json`

Change anytime with:
```bash
tess --settings
```

Or in-app:
```
You: config
[Settings Menu opens...]
```

---

## 🏗️ Architecture

```
tess_configurable/
├── config_manager.py      # Settings persistence
├── setup_wizard.py        # First-time setup TUI
├── settings_menu.py       # Configuration menu
├── main.py                # Entry point & CLI
└── core/
    ├── brain.py           # Multi-provider LLM
    ├── orchestrator.py    # Action routing
    └── schemas.py         # Data validation
```

---

## 🛡️ Security Features

- 🔐 API keys stored locally with 0600 permissions
- 🚫 No hardcoded credentials
- ✅ Command validation before execution
- ⚠️ Configurable confirmation prompts
- 🛡️ Blocked dangerous commands: `rm -rf`, `format`, `shutdown`

---

## 🐛 Troubleshooting

### "No API keys configured"
```bash
tess --setup
```

### Import errors
```bash
pip install --upgrade -r requirements.txt
```

### Reset everything
```bash
tess --reset
# Or manually delete ~/.tess/
```

---

## 🤝 Contributing

Contributions welcome! Areas to help:
- 🐛 Bug fixes
- ✨ New actions/skills
- 🌍 Cross-platform improvements
- 📚 Documentation

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file.

---

## 🙏 Credits

Inspired by the original TESS Terminal Pro. This configurable edition focuses on user control, easy setup, and clean architecture.

---

## ⭐ Star History

If you find TESS useful, please consider starring the repo!

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/tess-terminal&type=Date)](https://star-history.com/#YOUR_USERNAME/tess-terminal&Date)
