from .commity_cli import GitCommitCLI
import warnings

def main():
    warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')
    cli = GitCommitCLI()
    cli.run()

if __name__ == "__main__":
    main()