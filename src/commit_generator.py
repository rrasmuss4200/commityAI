from typing import Dict, Any
from openai import OpenAI

class CommitGenerator:
    """Generates commit messages using AI APIs."""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_commit_msg(self, diff: str, summary: Dict[str, Any]) -> str:
        """Generate commit message using OpenAI API."""
        prompt = self._create_prompt(diff, summary)

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that writes concise, clear git commit messages. Follow conventional commit format (feat:, fix:, docs:, etc.) when appropriate. Keep messages under 72 characters on the first line."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=100,
                temperature=0.3,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )

            # Extract the message from the response
            message = completion.choices[0].message.content.strip()

            # Clean up common issues
            message = message.replace('"', '').replace("'", '').strip()

            # If it's too long, take just the first line
            lines = message.split('\n')
            commit_msg = lines[0].strip()

            return commit_msg

        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")

    def _create_prompt(self, diff: str, summary: Dict[str, Any]) -> str:
        """Create prompt for OpenAI to generate commit message."""
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