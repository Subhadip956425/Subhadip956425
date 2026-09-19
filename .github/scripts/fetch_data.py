import json
import urllib.request
import os

USERNAME = "Subhadip956425"
URL = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=5"

def fetch_latest_projects():
    # Use a standard user-agent to prevent API blocking
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            projects = []
            for repo in data:
                # Skip forked repositories to only show your original work
                if repo.get("fork"):
                    continue
                    
                projects.append({
                    "name": repo.get("name", "Unknown").replace("-", " ").title(),
                    "description": repo.get("description") or "View repository for details.",
                    "tech": [repo.get("language", "Code")] if repo.get("language") else ["Code"],
                    "link": repo.get("html_url", "")
                })
                
                # Stop once we have exactly 3 original projects
                if len(projects) == 3:
                    break
                
            # Overwrite projects.json in the root directory
            project_file = os.path.join(os.path.dirname(__file__), '..', '..', 'projects.json')
            with open(project_file, "w", encoding="utf-8") as f:
                json.dump(projects, f, indent=2)
            
            print("Successfully updated projects.json with latest repositories.")
            
    except Exception as e:
        print(f"Error fetching GitHub data: {e}")

if __name__ == "__main__":
    fetch_latest_projects()
