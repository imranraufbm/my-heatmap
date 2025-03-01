import os
import subprocess
import sys
import argparse
import random
from datetime import datetime, timedelta
from PIL import Image

try:
    import config
except ImportError:
    config = None

# -------------------------------------------------------
# Utility
# -------------------------------------------------------

def run(cmd, env=None):
    # Quiet the output for a cleaner terminal during many commits
    subprocess.run(cmd, shell=True, check=True, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

COMMIT_MESSAGES = [
    "Fix: Resolved Python data synchronization issue",
    "Feature: Added HTML authentication layer",
    "Docs: Updated README documentation for better clarity",
    "Refactor: Optimized HTML/CSS heatmap rendering",
    "Bug: Fixed Python memory leak in generation loop",
    "Style: Improved HTML terminal output formatting",
    "Test: Added Python unit tests for date distribution",
    "Chore: Updated README dependencies and config",
    "Issue: Resolved HTML rendering bug",
    "Contribution: Private contribution to core engine",
    "Contribution: Solving Python backend issues",
    "Issue: Solved README formatting in March-April",
    "Private: Contribution to private project module",
    "Task: Implemented Python custom range generator",
    "Update: Refined HTML/Python commit weights"
]

def generate_custom_range_pattern(start_date, end_date, total_target=1000, night_only=False):
    """
    Generates commits from start_date to end_date.
    Favors nights (mostly) and weekends.
    If night_only is True, uses the 22:00 - 05:00 window.
    """
    print(f"\nGenerating {total_target} commits from {start_date} to {end_date}...")
    if night_only:
        print("Bias: Late Nights (22:00 - 05:00)\n")
    else:
        print("Bias: Nights and Weekends\n")
    
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    total_days = (end_dt - start_dt).days + 1
    
    commit_data = []
    
    # Generate all potential days
    days = [start_dt + timedelta(days=i) for i in range(total_days)]
    
    # Assign weights to days (Weekends get higher weights)
    day_weights = []
    for d in days:
        weight = 1.0
        if d.weekday() >= 5: # Saturday or Sunday
            weight = 3.0 # Weekends are 3x more likely/busy
        day_weights.append(weight)
        
    # Distribute total_target commits across days based on weights
    total_weight = sum(day_weights)
    commits_per_day = [int(total_target * (w / total_weight)) for w in day_weights]
    
    # Adjust for rounding errors
    diff = total_target - sum(commits_per_day)
    for _ in range(abs(diff)):
        idx = random.randint(0, len(commits_per_day) - 1)
        commits_per_day[idx] += 1 if diff > 0 else -1

    for i, day_obj in enumerate(days):
        day_str = day_obj.strftime("%Y-%m-%d")
        num_commits = commits_per_day[i]
        
        for _ in range(num_commits):
            if night_only:
                # Late night range: 22:00 to 05:00
                # Split between 22-23 and 0-5
                if random.random() < 0.4: # 40% chance of 22-23
                    hour = random.randint(22, 23)
                else: # 60% chance of 0-5
                    hour = random.randint(0, 5)
            else:
                # Default distribution: Mostly nights (after 18:00) and some day
                if random.random() < 0.7:
                    hour = random.randint(18, 23)
                else:
                    hour = random.randint(9, 17)
                
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            message = random.choice(COMMIT_MESSAGES)
            commit_data.append((day_str, hour, minute, second, message))
                
    return commit_data

def make_commit(date_str, hour=10, minute=0, second=0, message="Update", filename="activity_log.txt"):
    timestamp = f"{date_str}T{hour:02d}:{minute:02d}:{second:02d}"

    with open(filename, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = timestamp
    env["GIT_COMMITTER_DATE"] = timestamp

    run(f"git add -f {filename}")
    run(f'git commit -m "{message}"', env=env)

def preview_heatmap(commit_data):
    if not commit_data:
        print("No activity to preview.")
        return

    # Extract dates only
    date_objs = [datetime.strptime(d[0], "%Y-%m-%d").date() for d in commit_data]
    min_date = min(date_objs)
    max_date = max(date_objs)
    
    # Align min_date to Sunday
    start_date = min_date - timedelta(days=(min_date.weekday() + 1) % 7)
    num_weeks = (max_date - start_date).days // 7 + 1
    
    # Track intensity (commits per day)
    intensity_map = {}
    for d in date_objs:
        intensity_map[d] = intensity_map.get(d, 0) + 1
        
    print("\nHeatmap Preview (Intensity based on dots):")
    for y in range(7):
        line = ""
        for x in range(num_weeks):
            d = start_date + timedelta(weeks=x, days=y)
            count = intensity_map.get(d, 0)
            if count == 0:
                line += "· "
            elif count < 5:
                line += "░ "
            elif count < 10:
                line += "▒ "
            elif count < 15:
                line += "▓ "
            else:
                line += "█ "
        print(line)
    print()

# -------------------------------------------------------
# Main App
# -------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="GitHub Heatmap Designer")
    parser.add_argument("--start-date", type=str, default="2025-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, default="2025-07-17", help="End date (YYYY-MM-DD)")
    parser.add_argument("--commits", type=int, default=1000, help="Total target commits")
    parser.add_argument("--username", type=str, help="GitHub Username (overrides config.py)")
    parser.add_argument("--repo", type=str, help="GitHub Repository Name (overrides config.py)")
    parser.add_argument("--branch", type=str, default="main", help="Git Branch (default: main)")
    parser.add_argument("--night-only", action="store_true", help="Only generate commits between 22:00 and 05:00")
    
    args = parser.parse_args()

    # Determine configuration values
    username = args.username or (getattr(config, 'GITHUB_USERNAME', 'username') if config else 'username')
    repo = args.repo or (getattr(config, 'REPO_NAME', 'repo') if config else 'repo')
    start_date = args.start_date
    end_date = args.end_date
    total_commits = args.commits
    branch = args.branch
    night_only = args.night_only

    print("\n==============================")
    print("   GitHub Heatmap Designer")
    print("==============================")
    print(f"Target: {start_date} to {end_date}")
    print(f"Total Commits: {total_commits}")
    print(f"User/Repo: {username}/{repo}")
    if night_only:
        print("Timing: Late Night (22:00 - 05:00)")

    commit_data = generate_custom_range_pattern(start_date, end_date, total_commits, night_only=night_only)
    
    if not commit_data:
        print("No activity generated.")
        return

    preview_heatmap(commit_data)

    print(f"\nTotal days with activity: {len(set(d[0] for d in commit_data))}")
    print(f"Total commits to be created: {len(commit_data)}")

    confirm = input("\nProceed with creating commits? (yes/no): ").lower()
    if confirm != "yes":
        print("Cancelled.")
        return

    print("\nCreating commits... Please wait.")
    
    # Sort by date and time for natural repo history
    commit_data.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    
    total = len(commit_data)
    for idx, (d, h, m, s, msg) in enumerate(commit_data):
        make_commit(d, h, m, s, msg)
        if (idx + 1) % 50 == 0:
            print(f"Progress: {idx + 1}/{total} commits created...", end="\r")

    print(f"\n\nAll {total} commits created successfully.")
    print("\nTo update your GitHub profile (REPLACING current history):")
    print("WARNING: This will overwrite all existing history in the remote repository. Use with extreme caution.")
    print(f"  git remote add origin https://github.com/{username}/{repo}.git")
    print(f"  git push -u origin {branch} --force")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
