import os
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
    client.send("HTTP/1.1 200 OK\r\n\r\n{}".format(message).encode("utf-8"))
    client.close()


def authenticate():
    comma_scopes = "all"
    redirect_uri = "http://localhost:8080"

    if comma_scopes.lower() == "all":
        scopes = ["*"]
    else:
        scopes = comma_scopes.strip().split(",")

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


def get_reddit_instance(read_only=True):
    """Obtains reddit instance using refresh token."""
    # TODO: Using the pickle package might be easier here
    mode = 'r+' if os.path.exists("userdata.txt") else 'w+'
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    if not read_only:
        with open("userdata.txt", mode) as f:
            if len(f.read()) == 0:
                user_data = authenticate()
                refresh_token = user_data["refresh_token"]
                reddit = user_data["reddit"]
                f.write(refresh_token)
            else:
                f.seek(0)
                refresh_token = f.readline()
                reddit = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    refresh_token=refresh_token,
                    user_agent=user_agent,
                )
    return reddit

if __name__ == '__main__':
    authenticate()
