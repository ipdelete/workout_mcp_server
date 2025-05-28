Please analyze and address the review comments in the GitHub PR: $ARGUMENTS.

Follow these steps:

1. Use `gh pr view <PR_NUMBER> --comments` to see general PR comments
2. Use `gh api repos/<owner>/<repo>/pulls/<PR_NUMBER>/comments` for file-specific comments
3. Identify the specific feedback and understand what changes are requested
4. Navigate to the file(s) mentioned in the review
5. Implement the suggested changes following project conventions
6. Run relevant tests or linters after making changes
7. Create a commit that references the review feedback
8. Push the changes to the same PR branch
9. Respond to the reviewer's comment acknowledging the change

Remember to make focused commits that directly address the review feedback.