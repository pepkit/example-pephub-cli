import os
from argparse import ArgumentParser

from .const import LOGIN_ENDPOINT, TOKEN_EXCHAGE_ENDPOINT


def build_argparser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("login", type=bool, help="Login to the system")
    parser.add_argument("logout", type=bool, help="Logout from the system")
    parser.add_argument("--namespace", type=str, help="Namespace to fetch")

    return parser


def build_login_url() -> str:
    """
    Build login url using the environment variables
    """
    BASE_URL = os.getenv("BASE_URL")
    if BASE_URL is None:
        raise ValueError("Missing environment variables. Please set BASE_URL.")
    return f"{BASE_URL}{LOGIN_ENDPOINT}"


def build_token_exchange_url() -> str:
    """
    Build URL to get access token from the auth code
    """
    BASE_URL = os.getenv("BASE_URL")
    if BASE_URL is None:
        raise ValueError("Missing environment variables. Please set BASE_URL.")
    return f"{BASE_URL}{TOKEN_EXCHAGE_ENDPOINT}"
