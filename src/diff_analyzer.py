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
            raise Exception(f"Error getting git diff: {e}") from e

    def get_diff_summary(self, diff: str) -> Dict[str, Any]:
        if not diff.strip():
            return {"files_changed": 0, "insertions": 0, "deletions": 0, "files": []}

        files = []
        lines = diff.split('\n')

        # Get file names
        for line in lines:
            if line.startswith('diff --git'):
                parts = line.split(' ')
                if len(parts) >= 4:
                    files.append(parts[3][2:])

        line_insertertions = 0
        line_deletions = 0
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--numstat'],
                capture_output=True,
                text=True,
                check=True
            )
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 2 and parts[0] != '-' and parts[1] != '-':
                        try:
                            line_insertertions += int(parts[0]) if parts[0].isdigit() else 0
                            line_deletions += int(parts[1]) if parts[1].isdigit() else 0
                        except (ValueError, IndexError):
                            pass
        except subprocess.CalledProcessError:
            line_insertertions = diff.count('\n+')
            line_deletions = diff.count('\n-')

        return {"files_changed": len(files),
                "insertions": line_insertertions,
                "deletions": line_deletions,
                "files": files}
