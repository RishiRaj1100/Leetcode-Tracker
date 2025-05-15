import os
import json
import requests
import sys
from datetime import datetime
from github import Github
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LeetCode GraphQL endpoint
LEETCODE_API_URL = "https://leetcode.com/graphql"

# GraphQL query to fetch user stats
QUERY = """
query getUserProfile($username: String!) {
    matchedUser(username: $username) {
        username
        submitStats: submitStatsGlobal {
            acSubmissionNum {
                difficulty
                count
                submissions
            }
        }
        profile {
            ranking
            reputation
            starRating
            realName
            userAvatar
        }
        recentSubmissionList(limit: 5) {
            title
            timestamp
            statusDisplay
            lang
        }
    }
}
"""

def get_leetcode_stats(username):
    """Fetch LeetCode stats for a given username"""
    try:
        variables = {"username": username}
        response = requests.post(
            LEETCODE_API_URL,
            json={"query": QUERY, "variables": variables},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching LeetCode stats: {str(e)}")
        sys.exit(1)

def create_stats_markdown(data):
    """Create markdown content with LeetCode stats"""
    try:
        user_data = data["data"]["matchedUser"]
        stats = user_data["submitStats"]["acSubmissionNum"]
        profile = user_data["profile"]
        recent_submissions = user_data["recentSubmissionList"]
        
        # Calculate total solved problems
        total_solved = sum(item["count"] for item in stats if item["difficulty"] != "All")
        
        # Create markdown content
        markdown = f"""# LeetCode Progress Tracker

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Profile
- Username: {user_data["username"]}
- Name: {profile.get("realName", "Not provided")}
- Ranking: #{profile["ranking"]}
- Reputation: {profile["reputation"]}
- Star Rating: {profile["starRating"]}

## Overall Stats
- Total Problems Solved: {total_solved}
- Acceptance Rate: {calculate_acceptance_rate(stats)}%

## Problems Solved by Difficulty
"""
        
        # Add difficulty-wise stats
        for stat in stats:
            if stat["difficulty"] != "All":
                markdown += f"- {stat['difficulty']}: {stat['count']} problems\n"
        
        # Add recent submissions
        markdown += "\n## Recent Submissions\n"
        for submission in recent_submissions:
            timestamp = datetime.fromtimestamp(int(submission["timestamp"])).strftime('%Y-%m-%d %H:%M:%S')
            markdown += f"- {submission['title']} ({submission['lang']}) - {submission['statusDisplay']} - {timestamp}\n"
        
        return markdown
    except Exception as e:
        print(f"Error creating markdown: {str(e)}")
        sys.exit(1)

def calculate_acceptance_rate(stats):
    """Calculate acceptance rate from stats"""
    try:
        total_submissions = sum(item["submissions"] for item in stats if item["difficulty"] != "All")
        total_solved = sum(item["count"] for item in stats if item["difficulty"] != "All")
        return round((total_solved / total_submissions * 100), 2) if total_submissions > 0 else 0
    except Exception:
        return 0

def update_github_repo(content):
    """Update the GitHub repository with new stats"""
    try:
        # Initialize GitHub with token
        g = Github(os.getenv("GITHUB_TOKEN"))
        
        # Get the repository
        repo = g.get_repo(os.getenv("GITHUB_REPO"))
        
        # Create dsa directory if it doesn't exist
        try:
            repo.get_contents("dsa")
        except:
            repo.create_file(
                path="dsa/.gitkeep",
                message="Create dsa directory",
                content=""
            )
        
        # Update or create the file
        try:
            # Try to get the file first
            contents = repo.get_contents("dsa/leetcode_stats.md")
            repo.update_file(
                path="dsa/leetcode_stats.md",
                message="Update LeetCode stats",
                content=content,
                sha=contents.sha
            )
        except:
            # If file doesn't exist, create it
            repo.create_file(
                path="dsa/leetcode_stats.md",
                message="Create LeetCode stats",
                content=content
            )
            
        print("Successfully updated GitHub repository!")
    except Exception as e:
        print(f"Error updating GitHub repository: {str(e)}")
        sys.exit(1)

def main():
    # Get LeetCode username from environment variable
    leetcode_username = os.getenv("LEETCODE_USERNAME")
    if not leetcode_username:
        print("Error: LEETCODE_USERNAME not set in environment variables")
        sys.exit(1)
    
    # Fetch LeetCode stats
    print(f"Fetching stats for user: {leetcode_username}")
    stats_data = get_leetcode_stats(leetcode_username)
    
    # Create markdown content
    markdown_content = create_stats_markdown(stats_data)
    
    # Update GitHub repository
    update_github_repo(markdown_content)

if __name__ == "__main__":
    main() 