# List all issues with the betelgeuse label
ISSUES=$(gh issue list --repo nebulae-official/Orion --label betelgeuse --json number --jq '.[].number')

# Add each issue to the project
for ISSUE in $ISSUES; do
  gh project item-add 2 --owner nebulae-official --url "https://github.com/nebulae-official/Orion/issues/$ISSUE"
  echo "Added issue #$ISSUE to the project."
done

# Remove all issues from the project
for ISSUE in $ISSUES; do
  gh project item-remove 2 --owner nebulae-official --url "https://github.com/nebulae-official/Orion/issues/$ISSUE"
  echo "Removed issue #$ISSUE from the project."
done

# Remove projects
gh project delete 2 --owner nebulae-official

# Remove all issues from Repository
gh issue list --repo nebulae-official/Orion --label betelgeuse --json number --jq '.[].number' | while read -r ISSUE; do
  gh issue close "$ISSUE" --repo nebulae-official/Orion
  echo "Closed issue #$ISSUE."
done
