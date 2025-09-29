# CommityAI
An AI CLI tool that takes staged changes to git and creates a commit message from it.

# Installation Instructions:

## Quick Start
1. Install OpenAI SDK: `pip install openai`
2. Get your API key from https://platform.openai.com/api-keys
3. Set your API key: `export OPENAI_API_KEY=sk-your-key-here`
4. `git add` you want the AI to generate a commit message for
5. Run: `python main.py`

## Alternative Installation (as package)
1. Create a directory with both files
2. Run: `pip install -e .`
3. Use anywhere: `commityai`

## Usage Examples:

### Basic usage
export OPENAI_API_KEY=sk-...
git add .
python git_commit_ai.py

### Dry run (don't commit, just show message)
python git_commit_ai.py --dry-run

### Interactive mode (review before commit)
python git_commit_ai.py -i

### Pass API key directly (not recommended)
python git_commit_ai.py --api-key sk-...