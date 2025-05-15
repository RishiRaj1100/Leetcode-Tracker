# LeetCode Stats GitHub Updater

This script automatically updates your LeetCode statistics to a GitHub repository, making it easy for recruiters to track your progress.

## Features

- Fetches your LeetCode statistics using the official GraphQL API
- Creates/updates a markdown file with your current stats
- Automatically pushes updates to your GitHub repository
- Tracks total problems solved, ranking, and problems by difficulty

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` and fill in your details:
   - `LEETCODE_USERNAME`: Your LeetCode username
   - `GITHUB_TOKEN`: A GitHub Personal Access Token with repo scope
   - `GITHUB_REPO`: Your GitHub repository in the format `username/repository`

## Usage

Run the script:
```bash
python leetcode_stats_updater.py
```

The script will:
1. Fetch your current LeetCode statistics
2. Create/update a file at `dsa/leetcode_stats.md` in your repository
3. Push the changes to GitHub

## Automation

To keep your stats updated automatically, you can:

1. Set up a GitHub Action to run this script periodically
2. Use a cron job on your local machine
3. Use a cloud service like AWS Lambda

## Output

The script creates a markdown file with:
- Total problems solved
- Your LeetCode ranking
- Problems solved by difficulty level
- Last update timestamp

## Security

- Never commit your `.env` file
- Keep your GitHub token secure
- Use environment variables for sensitive information 