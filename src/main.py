import commity_cli
import warnings

def main():
    warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')
    cli = commity_cli.GitCommitCLI()
    cli.run()

if __name__ == "__main__":
    main()