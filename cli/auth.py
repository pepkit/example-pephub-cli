import logging
import os
import httpx
from helium import start_firefox, wait_until
from urllib.parse import urlparse, parse_qs

from .const import TOKEN_STORE
from .utils import build_login_url, build_token_exchange_url


def logout_from_github():
    """
    Removes the token file
    """
    logging.info("Logging out")
    try:
        os.rmdir(TOKEN_STORE)
        logging.info("Successfully logged out.")
    except FileNotFoundError:
        logging.info("You are not logged in.")


def exchange_auth_code_for_token(code: str) -> str:
    """
    Exchange auth code for access token
    """
    token_exchange_url = build_token_exchange_url()
    params = {"code": code}
    response = httpx.post(token_exchange_url, json=params)
    return response.json()["token"]


def login_to_github():
    """
    Open browser to log in to the system
    """
    login_url = build_login_url()
    driver = start_firefox(login_url)

    # wait for user to login, they get five minutes
    wait_until(
        lambda: "code" in driver.current_url,
        timeout_secs=5 * 60,
    )

    # extract auth_code
    url_with_code = driver.current_url
    q_params = parse_qs(urlparse(url_with_code).query)
    driver.close()
    auth_code = q_params.get("code")[0]
    access_token = exchange_auth_code_for_token(auth_code)

    # write to config file
    if not os.path.exists(TOKEN_STORE):
        os.makedirs(TOKEN_STORE)
    with open(TOKEN_STORE, "w") as f:
        f.write(access_token)
