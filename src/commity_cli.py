from .diff_analyzer import GitDiffAnalyzer
from .commit_generator import CommitGenerator

import argparse
import os
import sys
import subprocess


class GitCommitCLI:
    """Main CLI application."""

    def __init__(self):
        self.analyzer = GitDiffAnalyzer()

    def run(self):
        """Run the CLI application."""
        parser = argparse.ArgumentParser(
            description="Generate AI-powered commit messages from git diffs"
        )
        parser.add_argument(
            "--provider",
            choices=["openai"],
            default="openai",
            help="AI provider to use (default: openai)"
        )
        parser.add_argument(
            "--api-key",
            help="API key for the AI provider (or set OPENAI_API_KEY env var)"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Generate message but don't commit"
        )
        parser.add_argument(
            "--interactive",
            "-i",
            action="store_true",
            help="Review and edit the generated message before committing"
        )

        args = parser.parse_args()

        # Get API key
        api_key = args.api_key
        if not api_key:
            env_var = "OPENAI_API_KEY"
            api_key = os.getenv(env_var)

        if not api_key:
            print(f"Error: API key required. Set {env_var} environment variable or use --api-key")
            sys.exit(1)

        try:
            # Check if we're in a git repository
            subprocess.run(['git', 'status'], capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print("Error: Not in a git repository")
            sys.exit(1)

        try:
            # Get diff
            print("Analyzing staged changes...")
            diff = self.analyzer.get_staged_diff()

            if not diff.strip():
                print("No staged changes found. Use 'git add' to stage changes first.")
                sys.exit(1)

            summary = self.analyzer.get_diff_summary(diff)
            print(f"Found {summary['files_changed']} changed file(s)")

            # Generate commit message
            print("Generating commit message...")
            generator = CommitGenerator(api_key)
            message = generator.generate_commit_msg(diff, summary)

            print("\nGenerated commit message:")
            print("-" * 50)
            print(message)
            print("-" * 50)

            if args.dry_run:
                print("\nDry run mode - not committing")
                return

            # Interactive mode
            if args.interactive:
                response = input("\nUse this message? (y/n/e for edit): ").strip().lower()
                if response == 'n':
                    print("Commit cancelled")
                    return
                elif response == 'e':
                    # Open editor for message
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as f:
                        f.write(message)
                        f.flush()

                        editor = os.getenv('EDITOR', 'vi')
                        subprocess.run([editor, f.name])

                        f.seek(0)
                        message = open(f.name, 'r').read().strip()
                        os.unlink(f.name)
            else:
                response = input("\nCommit with this message? (y/n): ").strip().lower()
                if response != 'y':
                    print("Commit cancelled")
                    return

            # Commit with the message
            print("Committing...")
            subprocess.run(['git', 'commit', '-m', message], check=True)
            print("✅ Committed successfully!")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)