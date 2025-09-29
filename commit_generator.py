from typing import Dict, Any

class CommitGenerator:

    def __init__(self, key: str, provider: str = "openai"):
        self._key = key
        self._provider = provider

    def generate_commit_msg(self, diff: str, summary: Dict[str, Any]) -> str:
        match self._provider:
            # Add models if needed
            case "openai":
                return self._openai_gen(diff, summary)

    def _openai_gen(self, diff: str, summary: Dict[str, Any]) -> str:
        prompt = self._create_prompt(diff, summary)

        


    def _create_prompt(self, diff: str, summary: Dict[str, Any]) -> str:
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