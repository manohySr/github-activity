from typing import Dict, List
import requests

class GithubActivityService:
    """Service class for handling GitHub activity operations."""
    
    def __init__(self) -> None:
        """Initialize the GitHub activity service"""
        self.base_url = "https://api.github.com"
        
    def get_user_activity(self, username: str) -> List[Dict]:
        """Get user's GitHub activity.
        
        Args:
            username (str): GitHub username
            
        Returns:
            List[Dict]: List of activity events
        """
        # url = f"{self.base_url}/users/{username}/events"
        # response = requests.get(url)
        # response.raise_for_status()
        # return response.json()
        pass
        
    def display_activity(self, activities: List[Dict], title: str) -> None:
        """Display activity data in a formatted table.
        
        Args:
            activities (List[Dict]): List of activity events
            title (str): Title for the activity table
        """
        pass
