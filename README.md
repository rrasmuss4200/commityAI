# CommityAI
An AI CLI tool that takes staged changes to git and creates a commit message from it.

# Installation Instructions:

## Quick Start
1. Install OpenAI SDK: `pip install openai`
2. Get your API key from https://platform.openai.com/api-keys
3. Set your API key: `export OPENAI_API_KEY=sk-your-key-here`
4. `git add` you want the AI to generate a commit message for
5. Run: `python main.py`

## Usage Examples:

### Basic usage
export OPENAI_API_KEY=sk-...
git add .
python src/main.py

### Dry run (don't commit, just show message)
python src/main.py --dry-run

### Interactive mode (review before commit)
python src/main.py -i

### Pass API key directly (not recommended)
python src/main.py --api-key sk-...