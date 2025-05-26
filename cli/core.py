from typing import Dict, List
import requests
from requests.exceptions import RequestException
import typer
from rich.console import Console

class GithubActivityError(Exception):
    """Custom exception for GitHub activity errors."""
    pass


class GithubActivityService:
    """Service class for handling GitHub activity operations."""
    
    def __init__(self) -> None:
        """Initialize the GitHub activity service"""
        self.base_url = "https://api.github.com"
        self.console = Console()
        
    def get_user_activity(self, username: str) -> List[Dict]:
        """Get user's GitHub activity.
        
        Args:
            username (str): GitHub username
            
        Returns:
            List[Dict]: List of activity events
            
        Raises:
            GithubActivityError: If there's an error fetching the data
        """
        try:
            url = f"{self.base_url}/users/{username}/events"
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            if not data:
                raise GithubActivityError(f"No activity found for user: {username}")
                
            return data
            
        except RequestException as e:
            if response.status_code == 404:
                raise GithubActivityError(f"User not found: {username}")
            raise GithubActivityError(f"Error fetching GitHub data: {str(e)}")
        
    def display_activity(self, activities: List[Dict], username: str) -> None:
        """Display activity data in a formatted table.
        
        Args:
            activities (List[Dict]): List of activity events
            username (str): User name
        """

        self.console.print(f"\n[bold green]{username}'s recent GitHub Activity:[/bold green]\n")

        for event in activities:
            event_type = event.get("type")
            repo_name = event.get("repo", {}).get("name")
            actor_login = event.get("actor", {}).get("login")

            output_line = ""

            match event_type:
                case "PushEvent":
                    commit_count = event.get("payload", {}).get("size", 0)
                    output_line = f"- Pushed [bold blue]{commit_count} commits[/bold blue] to [bold magenta]{repo_name}[/bold magenta]"
                case "CreateEvent":
                    ref_type = event.get("payload", {}).get("ref_type")
                    ref = event.get("payload", {}).get("ref")
                    if ref_type == "repository":
                        output_line = f"- Created a new [bold cyan]repository[/bold cyan]: [bold magenta]{repo_name}[/bold magenta]"
                    elif ref_type == "branch":
                        output_line = f"- Created branch [bold yellow]{ref}[/bold yellow] in [bold magenta]{repo_name}[/bold magenta]"
                    elif ref_type == "tag":
                        output_line = f"- Created tag [bold yellow]{ref}[/bold yellow] in [bold magenta]{repo_name}[/bold magenta]"
                case "IssuesEvent":
                    action = event.get("payload", {}).get("action")
                    issue_title = event.get("payload", {}).get("issue", {}).get("title")
                    issue_number = event.get("payload", {}).get("issue", {}).get("number")
                    output_line = f"- {action.capitalize()} issue [bold green]#{issue_number}[/bold green]: '{issue_title}' in [bold magenta]{repo_name}[/bold magenta]"
                case "IssueCommentEvent":
                    action = event.get("payload", {}).get("action")
                    issue_title = event.get("payload", {}).get("issue", {}).get("title")
                    issue_number = event.get("payload", {}).get("issue", {}).get("number")
                    output_line = f"- {action.capitalize()} a comment on issue [bold green]#{issue_number}[/bold green]: '{issue_title}' in [bold magenta]{repo_name}[/bold magenta]"
                case "PullRequestEvent":
                    action = event.get("payload", {}).get("action")
                    pr_title = event.get("payload", {}).get("pull_request", {}).get("title")
                    pr_number = event.get("payload", {}).get("number")
                    output_line = f"- {action.capitalize()} pull request [bold purple]#{pr_number}[/bold purple]: '{pr_title}' in [bold magenta]{repo_name}[/bold magenta]"
                case "ForkEvent":
                    forkee_name = event.get("payload", {}).get("forkee", {}).get("full_name")
                    output_line = f"- Forked [bold magenta]{repo_name}[/bold magenta] to [bold cyan]{forkee_name}[/bold cyan]"
                case "WatchEvent":
                    action = event.get("payload", {}).get("action")
                    output_line = f"- {action.capitalize()} watching [bold magenta]{repo_name}[/bold magenta]"
                case "ReleaseEvent":
                    action = event.get("payload", {}).get("action")
                    release_name = event.get("payload", {}).get("release", {}).get("name")
                    output_line = f"- {action.capitalize()} release [bold yellow]'{release_name}'[/bold yellow] in [bold magenta]{repo_name}[/bold magenta]"
                case _:
                    # Fallback for unhandled event types
                    if repo_name:
                        output_line = f"- Performed a [bold white]{event_type}[/bold white] in [bold magenta]{repo_name}[/bold magenta]"
                    else:
                        output_line = f"- Performed a [bold white]{event_type}[/bold white]"

            if output_line:
                self.console.print(f"  {output_line}")
