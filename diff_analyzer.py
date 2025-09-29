import subprocess
from typing import Dict, Any

class GitDiffAnalyzer:

    def get_staged_diff(self) -> str:
        try:
            res = subprocess.run(
                ['git', 'diff', '--cached', '--no-color'],
                capture_output=True,
                text=True,
                check=True
            )
            return res.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error getting git diff: {e}")

    def get_diff_summary(self, diff: str) -> Dict[str, Any]:
        if not diff.strip():
            return {"files_changed": 0, "insertions": 0, "deletions": 0, "files": []}

        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--stat', '--no-color'],
                capture_output=True,
                text=True,
                check=True
            )
            stat_output = result.stdout
        except subprocess.CalledProcessError:
            stat_output = ""

        files = []
        lines = diff.split('\n')

        # Get file names
        for line in lines:
            if line.startswith('diff --git'):
                parts = line.split(' ')
                if len(parts) >= 4:
                    files.append(parts[3][2:])

        line_insertertions = stat_output.count('+') if '+' in stat_output else 0
        line_deletions = stat_output.count('-') if '-' in stat_output else 0

        return {"Files Changed": len(files),
                "insertions": line_insertertions,
                "deletions": line_deletions,
                "files": files}
