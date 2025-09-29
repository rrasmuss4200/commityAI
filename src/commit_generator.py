from typing import Dict, Any
import requests

class CommitGenerator:
    """Generates commit messages using AI APIs."""

    def __init__(self, api_key: str, provider: str = "openai"):
        self.api_key = api_key
        self.provider = provider.lower()

    def generate_commit_msg(self, diff: str, summary: Dict[str, Any]) -> str:
        """Generate commit message using AI."""
        if self.provider == "openai":
            return self._generate_openai(diff, summary)
        elif self.provider == "anthropic":
            return self._generate_anthropic(diff, summary)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def _generate_openai(self, diff: str, summary: Dict[str, Any]) -> str:
        """Generate commit message using OpenAI API."""
        prompt = self._create_prompt(diff, summary)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that writes concise, clear git commit messages following conventional commit format when appropriate."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 100,
            "temperature": 0.3
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            return result["choices"][0]["message"]["content"].strip()

        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API error: {e}")

    def _generate_anthropic(self, diff: str, summary: Dict[str, Any]) -> str:
        """Generate commit message using Anthropic API."""
        prompt = self._create_prompt(diff, summary)

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }

        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 100,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            return result["content"][0]["text"].strip()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Anthropic API error: {e}")

    def _create_prompt(self, diff: str, summary: Dict[str, Any]) -> str:
        """Create prompt for AI to generate commit message."""
        # Truncate diff if too long
        max_diff_length = 2000
        truncated_diff = diff[:max_diff_length] + "..." if len(diff) > max_diff_length else diff

        prompt = f"""
Analyze this git diff and write a concise commit message. Follow these guidelines:
- Use imperative mood (e.g., "Add", "Fix", "Update")
- Keep the first line under 72 characters
- Be specific about what changed
- Use conventional commit format when appropriate (feat:, fix:, docs:, etc.)

Files changed: {summary['files_changed']}
Files: {', '.join(summary['files'][:5])}{'...' if len(summary['files']) > 5 else ''}

Git diff:
```
{truncated_diff}
```

Commit message:"""

        return prompt