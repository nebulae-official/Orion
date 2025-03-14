# List all issues with the betelgeuse label
ISSUES=$(gh issue list --repo nebulae-official/Orion --label betelgeuse --json number --jq '.[].number')

# Add each issue to the project
for ISSUE in $ISSUES; do
  gh project item-add 2 --owner nebulae-official --url "https://github.com/nebulae-official/Orion/issues/$ISSUE"
  echo "Added issue #$ISSUE to the project."
done
