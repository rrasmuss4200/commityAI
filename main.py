import commity_ai

def main():
    an = commity_ai.GitDiffAnalyzer()
    print(an.get_diff_summary(an.get_staged_diff()))

if __name__ == "__main__":
    main()