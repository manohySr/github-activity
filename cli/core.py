from typing import Dict, List, Optional
import requests
from requests.exceptions import RequestException
import typer
from rich.console import Console


class GithubActivityError(Exception):
    """Custom exception for GitHub activity errors."""
    pass


class EventFormatter:
    """Helper class to format different types of GitHub events."""
    
    @staticmethod
    def format_push_event(event: Dict) -> str:
        commit_count = event.get("payload", {}).get("size", 0)
        repo_name = event.get("repo", {}).get("name")
        return f"- Pushed [bold blue]{commit_count} commits[/bold blue] to [bold magenta]{repo_name}[/bold magenta]"

    @staticmethod
    def format_create_event(event: Dict) -> str:
        ref_type = event.get("payload", {}).get("ref_type")
        ref = event.get("payload", {}).get("ref")
        repo_name = event.get("repo", {}).get("name")
        
        if ref_type == "repository":
            return f"- Created a new [bold cyan]repository[/bold cyan]: [bold magenta]{repo_name}[/bold magenta]"
        elif ref_type in ["branch", "tag"]:
            return f"- Created {ref_type} [bold yellow]{ref}[/bold yellow] in [bold magenta]{repo_name}[/bold magenta]"
        return ""

    @staticmethod
    def format_issue_event(event: Dict) -> str:
        action = event.get("payload", {}).get("action")
        issue = event.get("payload", {}).get("issue", {})
        repo_name = event.get("repo", {}).get("name")
        return f"- {action.capitalize()} issue [bold green]#{issue.get('number')}[/bold green]: '{issue.get('title')}' in [bold magenta]{repo_name}[/bold magenta]"

    @staticmethod
    def format_pr_event(event: Dict) -> str:
        action = event.get("payload", {}).get("action")
        pr = event.get("payload", {}).get("pull_request", {})
        repo_name = event.get("repo", {}).get("name")
        return f"- {action.capitalize()} pull request [bold purple]#{event.get('payload', {}).get('number')}[/bold purple]: '{pr.get('title')}' in [bold magenta]{repo_name}[/bold magenta]"

    @staticmethod
    def format_fork_event(event: Dict) -> str:
        repo_name = event.get("repo", {}).get("name")
        forkee_name = event.get("payload", {}).get("forkee", {}).get("full_name")
        return f"- Forked [bold magenta]{repo_name}[/bold magenta] to [bold cyan]{forkee_name}[/bold cyan]"

    @staticmethod
    def format_watch_event(event: Dict) -> str:
        action = event.get("payload", {}).get("action")
        repo_name = event.get("repo", {}).get("name")
        return f"- {action.capitalize()} watching [bold magenta]{repo_name}[/bold magenta]"

    @staticmethod
    def format_release_event(event: Dict) -> str:
        action = event.get("payload", {}).get("action")
        release_name = event.get("payload", {}).get("release", {}).get("name")
        repo_name = event.get("repo", {}).get("name")
        return f"- {action.capitalize()} release [bold yellow]'{release_name}'[/bold yellow] in [bold magenta]{repo_name}[/bold magenta]"


class GithubActivityService:
    """Service class for handling GitHub activity operations."""
    
    EVENT_FORMATTERS = {
        "PushEvent": EventFormatter.format_push_event,
        "CreateEvent": EventFormatter.format_create_event,
        "IssuesEvent": EventFormatter.format_issue_event,
        "PullRequestEvent": EventFormatter.format_pr_event,
        "ForkEvent": EventFormatter.format_fork_event,
        "WatchEvent": EventFormatter.format_watch_event,
        "ReleaseEvent": EventFormatter.format_release_event,
    }
    
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
        """Display activity data in a formatted way.
        
        Args:
            activities (List[Dict]): List of activity events
            username (str): User name
        """
        self.console.print(f"\n[bold green]{username}'s recent GitHub Activity:[/bold green]\n")

        for event in activities:
            event_type = event.get("type")
            formatter = self.EVENT_FORMATTERS.get(event_type)
            
            if formatter:
                output_line = formatter(event)
            else:
                repo_name = event.get("repo", {}).get("name")
                output_line = f"- Performed a [bold white]{event_type}[/bold white]" + (
                    f" in [bold magenta]{repo_name}[/bold magenta]" if repo_name else ""
                )

            if output_line:
                self.console.print(f"  {output_line}")
