# AxLu-ZeSi CP - AI Coding Assistant

A beautiful, LeetCode-style C++ coding platform with AI assistance.

![Platform Preview](https://img.shields.io/badge/Python-3.10+-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## Features

- 🎨 **Beautiful Dark Theme UI** - Modern, sleek interface inspired by VS Code
- 🤖 **AI-Powered Assistance** - Get help from the fine-tuned model
- ✅ **Self-Verification** - AI checks its own solution before presenting
- 💻 **Real C++ Compiler** - Compile and run C++ code directly
- 📝 **Multiple Problems** - Practice with curated problems
- ⚡ **Fast Execution** - Instant feedback on your code

## Screenshots

The platform features:
- Dark theme with gradient accents
- Split-pane layout (Problems | Editor | Output)
- Beautiful code editor with syntax highlighting ready
- Real-time test case results
- AI assistant modal with reasoning

## Quick Start

### Prerequisites

- Python 3.10+
- g++ compiler (MinGW on Windows)
- LM Studio (for AI features)
- Flask

### Installation

```bash
# Navigate to app directory
cd axlu-zesi-cp/app

# Install dependencies
pip install -r requirements.txt

# Install evaluation dependencies
cd ../evaluation
pip install -r requirements.txt
```

### Running the App

```bash
# Make sure LM Studio is running with your model loaded

# Start the web server
cd axlu-zesi-cp/app
python main_app.py
```

Open your browser to: **http://localhost:5000**

## Usage

### 1. Select a Problem
- Click on any problem from the left panel
- Read the description, examples, and constraints

### 2. Write Your Solution
- Type your C++ code in the editor
- Use the template to get started

### 3. Run / Submit
- Click **Run** to test against sample cases
- Click **Submit** when ready

### 4. Get AI Help
- Click **Ask AI** when stuck
- The AI will generate a solution
- The solution is self-verified (tested before showing)
- Click **Use This Solution** to insert it into the editor

## Project Structure

```
axlu-zesi-cp/
├── app/
│   ├── main_app.py          # Main Flask application
│   ├── templates/
│   │   └── main.html       # Beautiful frontend
│   └── requirements.txt
├── evaluation/              # Evaluation engine
│   ├── client.py           # LM Studio API
│   ├── compiler.py         # C++ compiler
│   ├── runner.py           # Test runner
│   ├── harness.py          # Evaluation harness
│   └── prompts.py          # AI prompts
└── dataset/               # Problem datasets
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page |
| `/api/problems` | GET | List all problems |
| `/api/compile` | POST | Compile C++ code |
| `/api/run` | POST | Run code against tests |
| `/api/ask-ai` | POST | Get AI solution |
| `/api/health` | GET | System health check |

## How AI Works

1. User clicks "Ask AI"
2. Problem + prompt sent to model
3. Model generates solution
4. Solution is compiled and tested
5. If tests fail → Model tries to fix (up to 3 attempts)
6. Verified solution + reasoning shown to user

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JS
- **Backend**: Python Flask
- **AI**: Qwen2.5 via LM Studio
- **Compiler**: g++ (MinGW)

## Customization

### Add More Problems

Edit the `SAMPLE_PROBLEMS` list in `main_app.py`:

```python
{
    "id": "new_problem",
    "title": "New Problem",
    "difficulty": "Medium",
    "tags": ["Array", "DP"],
    "statement": "Problem description...",
    "examples": [...]
}
```

### Change AI Model

Edit `config.py` in the evaluation directory:
```python
MODEL_NAME = "your-model-name"
API_URL = "http://localhost:1234/v1"
```

## Troubleshooting

### "Compiler not found"
- Install MinGW/g++ on Windows
- Ensure g++ is in PATH

### "AI not responding"
- Check LM Studio is running
- Ensure model is loaded
- Verify server URL in config

### "Tests not passing"
- Check your code logic
- Verify input/output format matches

## License

MIT License - See LICENSE file

## Credits

- Base Model: [Qwen](https://huggingface.co/Qwen)
- Framework: [LM Studio](https://lmstudio.ai/)
- Icons: Custom SVG icons
