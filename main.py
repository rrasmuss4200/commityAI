import diff_analyzer

def main():
    an = diff_analyzer.GitDiffAnalyzer()
    print(an.get_diff_summary(an.get_staged_diff()))

if __name__ == "__main__":
    main()