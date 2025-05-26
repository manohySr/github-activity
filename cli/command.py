import typer
from .core import GithubActivityService, GithubActivityError


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
            try:
                activities = self.service.get_user_activity(username)
                self.service.display_activity(activities, username)
            except GithubActivityError as e:
                typer.echo(f"\tError: {str(e)}")
                typer.Exit(code=1)

    def run(self):
        self.app()

# Create a singleton instance
github_activity = GithubActivity()
app = github_activity.app

if __name__ == "__main__":
    github_activity.run()
