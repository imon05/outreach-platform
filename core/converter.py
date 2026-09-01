import json
import pickle

# Load cookies from the JSON you exported
with open("twitter_cookies.json", "r", encoding="utf-8") as f:
    cookies = json.load(f)

# Convert into Selenium-friendly format
selenium_cookies = []
for c in cookies:
    cookie = {
        "name": c.get("name"),
        "value": c.get("value"),
        "domain": c.get("domain"),
        "path": c.get("path"),
        "expiry": c.get("expirationDate") if "expirationDate" in c else None,
        "secure": c.get("secure", False),
        "httpOnly": c.get("httpOnly", False)
    }
    selenium_cookies.append(cookie)

# Save as pickle for easy load in your scraping script
with open("x_cookies.pkl", "wb") as f:
    pickle.dump(selenium_cookies, f)

print("✅ Cookies converted and saved to x_cookies.pkl")
