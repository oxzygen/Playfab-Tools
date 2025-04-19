import requests
import json
import time

# Load config
with open("config.json") as f:
    config = json.load(f)

TITLE_ID = config["title_id"]
SECRET_KEY = config["secret_key"]

# Load PlayFab IDs from file
with open("ids.txt", "r") as f:
    ids = [line.strip() for line in f if line.strip()]

def ban_user(playfab_id):
    url = f"https://{TITLE_ID}.playfabapi.com/Admin/BanUsers"
    headers = {
        "X-SecretKey": SECRET_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "Bans": [
            {
                "PlayFabId": playfab_id,
                "Reason": "Mass ban",
                "DurationInSeconds": 0  # if 0 it will be permanent
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, headers=headers)
        data = res.json()
        if res.status_code == 200 and "error" not in data:
            print(f"Banned: {playfab_id}")
        else:
            print(f"Failed to ban {playfab_id}: {data.get('errorMessage', data)}")
    except Exception as e:
        print(f"Error banning {playfab_id}: {str(e)}")

def main():
    print(f"Starting ban of {len(ids)} users...")
    for pid in ids:
        ban_user(pid)
        time.sleep(0.2)  # prevent rate limiting
    print("Done banning all users.")

if __name__ == "__main__":
    main()
