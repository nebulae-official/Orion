import csv
import subprocess
import json
from typing import Dict, List, Optional, Any
import os.path


def load_milestones(repo_path: str) -> Dict[str, int]:
    """Load milestones from GitHub repository.

    Args:
        repo_path: Repository path in format 'owner/repo'

    Returns:
        Dictionary mapping milestone titles to their IDs

    """
    result = subprocess.run(
        ["gh", "api", f"repos/{repo_path}/milestones"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print(f"Error loading milestones: {result.stderr}")
        return {}

    milestones = json.loads(result.stdout)
    return {m["title"]: m["number"] for m in milestones}


def create_issues_from_csv(
    csv_path: str,
    repo_path: str,
    dry_run: bool = False,
) -> None:
    """Create GitHub issues from a CSV file.

    Args:
        csv_path: Path to the CSV file containing issue data
        repo_path: Repository path in format 'owner/repo'
        dry_run: If True, only print commands without executing them

    """
    # Validate CSV file exists
    if not os.path.isfile(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    # Load milestones
    milestone_map = load_milestones(repo_path)
    if not milestone_map:
        print("Warning: No milestones found or error occurred")

    # Process each task
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Find milestone number
            milestone_id = None
            for title, number in milestone_map.items():
                if row["Phase"] in title:
                    milestone_id = title
                    break

            # Prepare issue creation command
            cmd = [
                "gh",
                "issue",
                "create",
                "--repo",
                repo_path,
                "--title",
                f"[BETELGEUSE] {row['Title']}",
                "--body",
                prepare_issue_body(row),
            ]

            if milestone_id:
                cmd.extend(["--milestone", str(milestone_id)])

            if row["Labels"]:
                cmd.extend(["--label", row["Labels"]])

            # Print issue details
            print(f"\nIssue Details: Title: {row['Title']}")
            print(f"Description: {row['Description'][:50]}...")
            print(f"Labels: {row['Labels']}")
            print(f"Milestone ID: {milestone_id}")

            if dry_run:
                print(f"[DRY RUN] Command: {' '.join(cmd)}")
            else:
                print(f"Running command: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Created issue: {row['Title']}")
                else:
                    print(f"❌ Failed to create issue: {row['Title']}")
                    print(f"Error: {result.stderr}")


def prepare_issue_body(row: Dict[str, str]) -> str:
    """
    Format the issue body using the row data.

    Args:
        row: Dictionary containing issue data from CSV

    Returns:
        Formatted issue body text
    """
    body = f"""## Description
{row["Description"]}

## Implementation Details
<!-- Add implementation details here -->

## Acceptance Criteria
- [ ] Implementation completed
- [ ] Tests added
- [ ] Documentation updated

## Phase
{row["Phase"]}

## Additional Notes
<!-- Add any additional notes here -->
"""
    return body


if __name__ == "__main__":
    create_issues_from_csv(
        csv_path="/mnt/d/Production/Projects/nebulae/Orion/scripts/betelgeuse_issues.csv",
        repo_path="nebulae-official/Orion",
        dry_run=False,  # Set to True for testing
    )
