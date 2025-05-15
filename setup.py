import os
import sys
import subprocess
import requests
from getpass import getpass
from github import Github
from dotenv import load_dotenv

def run_command(command):
    """Run a shell command and return its output"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def create_github_repo(token, repo_name):
    """Create a new GitHub repository"""
    try:
        g = Github(token)
        user = g.get_user()
        repo = user.create_repo(
            repo_name,
            description="LeetCode Progress Tracker",
            homepage="https://github.com/{}/{}".format(user.login, repo_name),
            has_wiki=False,
            has_issues=True,
            auto_init=True
        )
        return repo
    except Exception as e:
        print(f"Error creating GitHub repository: {str(e)}")
        sys.exit(1)

def setup_repository_secrets(token, repo_name, leetcode_username):
    """Set up repository secrets"""
    try:
        # Get the repository
        g = Github(token)
        repo = g.get_repo(f"{g.get_user().login}/{repo_name}")
        
        # Set up the LEETCODE_USERNAME secret
        repo.create_secret("LEETCODE_USERNAME", leetcode_username)
        print("Successfully set up repository secrets!")
    except Exception as e:
        print(f"Error setting up repository secrets: {str(e)}")
        sys.exit(1)

def main():
    print("Welcome to LeetCode Progress Tracker Setup!")
    print("This script will help you set up your LeetCode progress tracking repository.")
    
    # Get GitHub token
    print("\nTo enter your GitHub token:")
    print("1. Copy your token")
    print("2. Right-click in this window to paste")
    print("3. Press Enter when done")
    print("\nEnter your GitHub Personal Access Token:")
    github_token = input().strip()
    
    # Get LeetCode username
    print("\nEnter your LeetCode username:")
    leetcode_username = input().strip()
    
    # Get repository name
    print("\nEnter the name for your repository (default: leetcode-progress):")
    repo_name = input().strip() or "leetcode-progress"
    
    # Create .env file
    with open(".env", "w") as f:
        f.write(f"LEETCODE_USERNAME={leetcode_username}\n")
        f.write(f"GITHUB_TOKEN={github_token}\n")
        f.write(f"GITHUB_REPO={repo_name}\n")
    
    print("\nCreating GitHub repository...")
    repo = create_github_repo(github_token, repo_name)
    
    print("\nSetting up repository secrets...")
    setup_repository_secrets(github_token, repo_name, leetcode_username)
    
    print("\nInitializing local repository...")
    run_command("git init")
    run_command("git add .")
    run_command('git commit -m "Initial commit"')
    
    print("\nSetting up remote and pushing code...")
    run_command(f"git remote add origin https://github.com/{repo.full_name}.git")
    run_command("git branch -M main")
    run_command("git push -u origin main")
    
    print("\nSetup completed successfully!")
    print(f"\nYour LeetCode progress will be tracked at: https://github.com/{repo.full_name}")
    print("The GitHub Action will start running automatically.")
    print("\nYou can view your progress at: https://github.com/{repo.full_name}/blob/main/dsa/leetcode_stats.md")

if __name__ == "__main__":
    main() 