"""Fetch live Hack The Box stats and write htb.json for the website.

Needs two GitHub repo secrets:
  HTB_TOKEN    - App Token from https://app.hackthebox.com/account-settings (App Tokens)
  HTB_USER_ID  - number in your profile URL: app.hackthebox.com/profile/<ID>
"""
import json, os, sys, urllib.request


TOKEN = os.environ.get("HTB_TOKEN")
USER_ID = os.environ.get("HTB_USER_ID")
if not TOKEN or not USER_ID:
    sys.exit("HTB_TOKEN and HTB_USER_ID must be set")

API = "https://labs.hackthebox.com/api/v4"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (portfolio-stats)",
}


def get(path):
    req = urllib.request.Request(API + path, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


profile = get(f"/user/profile/basic/{USER_ID}").get("profile", {})

data = {
    "name": profile.get("name"),
    "rank": profile.get("rank"),                 # e.g. "Hacker", "Pro Hacker"
    "global_rank": profile.get("ranking"),       # global ranking position
    "points": profile.get("points"),
    "user_owns": profile.get("user_owns"),
    "system_owns": profile.get("system_owns"),
    "country": profile.get("country_name"),
    "country_rank": None,
    "profile_url": f"https://app.hackthebox.com/profile/{USER_ID}",
}

with open("htb.json", "w") as f:
    json.dump(data, f, indent=2)

# Print only non-sensitive fields so the workflow log is useful for debugging.
print(json.dumps({k: data[k] for k in ("rank", "global_rank", "points", "country")}))
