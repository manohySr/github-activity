import typer
from .core import GithubActivityService


class GithubActivity:
    def __init__(self) -> None:
        self.app = typer.Typer(help="Github activity CLI")
        self.service = GithubActivityService()
        self._setup_commands()

    def _setup_commands(self):
        @self.app.command()
        def hello():
            """Test hello world"""
            typer.echo("Hello world")

        @self.app.command()
        def user(
            username: str = typer.Argument(..., help="GitHub username"),
        ):
            """Get activity for a specific GitHub user."""
            activities = self.service.get_user_activity(username)
            typer.echo(f"Activity for {username}")
            self.service.display_activity(activities, f"Activity for {username}")

    def run(self):
        self.app()

# Create a singleton instance
github_activity = GithubActivity()
app = github_activity.app

if __name__ == "__main__":
    github_activity.run()
