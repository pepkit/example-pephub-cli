import logging
import typer
import webbrowser
from dotenv import load_dotenv

from cli.utils import build_login_url
from cli.auth import login_to_github

load_dotenv()

# from cli.auth import logout, login

logging.basicConfig(level=logging.INFO)

app = typer.Typer()


@app.command()
def login():
    """
    Open browser to log in to the system
    """
    login_to_github()


def main():
    app()


if __name__ == "__main__":
    main()
