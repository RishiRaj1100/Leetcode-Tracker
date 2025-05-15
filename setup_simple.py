import os
import sys
import subprocess
import shutil
from github import Github

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def main():
    print("=== LeetCode Progress Tracker Setup ===")
    print("\nStep 1: Enter your GitHub token")
    print("(Right-click to paste in PowerShell)")
    token = input("GitHub Token: ").strip()
    
    print("\nStep 2: Enter your LeetCode username")
    username = input("LeetCode Username: ").strip()
    
    print("\nStep 3: Enter repository name (or press Enter for default)")
    repo_name = input("Repository Name [leetcode-progress]: ").strip() or "leetcode-progress"
    
    # Create .env file
    with open(".env", "w") as f:
        f.write(f"LEETCODE_USERNAME={username}\n")
        f.write(f"GITHUB_TOKEN={token}\n")
        f.write(f"GITHUB_REPO={repo_name}\n")
    
    print("\nSetting up GitHub repository...")
    try:
        g = Github(token)
        user = g.get_user()
        
        # Check if repository exists
        try:
            repo = g.get_repo(f"{user.login}/{repo_name}")
            print(f"Repository {repo_name} already exists. Updating...")
        except:
            print(f"Creating new repository {repo_name}...")
            repo = user.create_repo(
                repo_name,
                description="LeetCode Progress Tracker",
                has_wiki=False,
                has_issues=True,
                auto_init=True
            )
        
        # Set up repository secret
        try:
            repo.create_secret("LEETCODE_USERNAME", username)
        except:
            print("Secret already exists, updating...")
            # Delete existing secret and create new one
            repo.delete_secret("LEETCODE_USERNAME")
            repo.create_secret("LEETCODE_USERNAME", username)
        
        print("\nSetting up local repository...")
        # Remove existing git configuration if any
        if os.path.exists(".git"):
            shutil.rmtree(".git", ignore_errors=True)
        
        run_command("git init")
        run_command("git add .")
        run_command('git commit -m "Initial commit"')
        
        print("\nPushing to GitHub...")
        # Remove existing remote if any
        try:
            run_command("git remote remove origin")
        except:
            pass
        
        run_command(f"git remote add origin https://github.com/{repo.full_name}.git")
        run_command("git branch -M main")
        
        # Force push to overwrite remote content
        run_command("git push -f origin main")
        
        print("\n=== Setup Complete! ===")
        print(f"\nYour LeetCode progress will be tracked at:")
        print(f"https://github.com/{repo.full_name}")
        print("\nYou can view your progress at:")
        print(f"https://github.com/{repo.full_name}/blob/main/dsa/leetcode_stats.md")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 