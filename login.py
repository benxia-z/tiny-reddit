import random
import socket
import sys
import requests
import webbrowser
import praw

client_id = "9jNQxoJqfiPogA"
client_secret = None
user_agent = "windows/osx/linux:redditterminalclient:v1.0.0 (by /u/Soopzoup and /u/KosherCow)"

def receive_connection():
    """Wait for and then return a connected socket
    Opens a TCP connection on port 8080, and waits for a single client.

    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send("HTTP/1.1 200 OK\r\n\r\n{}".format(message).encode("utf-8"))
    client.close()

def main():

    commaScopes = "all"
    redirect_uri = "http://localhost:8080"

    if commaScopes.lower() == "all":
        scopes = ["*"]
    else:
        scopes = commaScopes.strip().split(",")

    reddit = praw.Reddit(
        client_id=client_id.strip(),
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        user_agent=user_agent,
    )
    state = str(random.randint(0, 65000))
    url = reddit.auth.url(scopes, state, "permanent")
    sys.stdout.flush()
    webbrowser.open(url)

    client = receive_connection()
    data = client.recv(1024).decode("utf-8")
    param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
    params = {
        key: value for (key, value) in [token.split("=") for token in param_tokens]
    }

    if state != params["state"]:
        send_message(
            client,
            "State mismatch. Expected: {} Received: {}".format(state, params["state"]),
        )
        raise Exception("State mismatch error")
    elif "error" in params:
        send_message(client, params["error"])
        raise Exception("Client error")

    refresh_token = reddit.auth.authorize(params["code"])
    send_message(client, "Authentication successful, you can close the tab now.")

    user_data = {"reddit": reddit,
                 "refresh_token": refresh_token}

    return user_data
