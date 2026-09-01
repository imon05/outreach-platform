import requests 
from bs4 import BeautifulSoup 
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# -- REDDIT SCRAPER --

def scrape_reddit(keywords, batch_size):
    prospects = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    for keyword in keywords:
        print(f"🔍 Searching Reddit for: {keyword}")
        url = f"https://www.reddit.com/search.json?q={keyword}&sort=new&limit=25"
        resp = requests.get(url, headers=headers)
             
        if resp.status_code != 200:
            print(f"⚠️ Failed to fetch for keyword: {keyword}")
            continue

        try:
            data = resp.json()
            posts = data.get("data", {}).get("children", [])
            count = 0

            for post in posts:
                post_data = post.get("data", {})
                username = post_data.get("author")
                if not username or username == "[deleted]":
                    continue

                title = post_data.get("title", "").strip()
                body = post_data.get("selftext", "").strip()
                body_text = body if body else title  # Fallback to title if body is empty

                permalink = post_data.get("permalink", "")
                profile_link = f"https://reddit.com/u/{username}"
                full_link = f"https://reddit.com{permalink}"

                prospects.append({
                    "platform": "reddit",
                    "username": username,
                    "profile_link": profile_link,
                    "bio": f"Post: {body_text} ({full_link})"
                })

                count += 1
                if count >= batch_size:
                    break
                
        except Exception as e:
            print(f"❌ Error parsing JSON for keyword '{keyword}':", str(e))

        time.sleep(2)  # Respectful scraping

    print(f"🎯 Reddit results: {prospects}")
    return prospects

# -- INDIHACKERS SCRAPER --

def scrape_indiehackers(keywords, batch_size):
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=options)

    prospects = []

    for keyword in keywords:
        print(f"🔍 Searching IndieHackers for: {keyword}")
        search_url = f"https://www.indiehackers.com/search?q={keyword}&type=discussion"
        driver.get(search_url)
        time.sleep(3)  # Let the page fully load

        soup = BeautifulSoup(driver.page_source, "html.parser")
        discussions = soup.select("div.search-result--discussion")

        for discussion in discussions:
            try:
                username_tag = discussion.select_one(".user-link__name--username")
                profile_tag = discussion.select_one("a.user-link__link")
                post_link_tag = discussion.select_one("a.result__text-link")
                post_title_tag = discussion.select_one(".result__title")

                if not (username_tag and profile_tag and post_link_tag and post_title_tag):
                    continue

                username = username_tag.text.strip()
                profile_link = "https://www.indiehackers.com" + profile_tag["href"]
                post_title = post_title_tag.text.strip()
                post_url = "https://www.indiehackers.com" + post_link_tag["href"]

                # Visit post URL to fetch full post content
                driver.get(post_url)

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "post-page__body"))
                    )
                except:
                    print(f"⚠️ Timeout waiting for post body at {post_url}")
                    continue

                post_soup = BeautifulSoup(driver.page_source, "html.parser")
                paragraphs = post_soup.select(".post-page__body p")
                content = " ".join(p.text.strip() for p in paragraphs)

                if not content:
                    content = f"{post_title} (No body found)"

                # Final bio = content from post body
                prospects.append({
                    "platform": "indiehackers",
                    "username": username,
                    "profile_link": profile_link,
                    "bio": f"Post: {content} ({post_url})"
                })

                if len(prospects) >= batch_size:
                    break

            except Exception as e:
                print(f"⚠️ Error parsing a discussion block: {e}")
                continue

        time.sleep(2)

    driver.quit()
    return prospects

# -- X SCRAPER --

import pickle

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def load_cookies(driver, cookie_file="C:/Users/debim/sudohumanx_outreach/core/x_cookies.pkl"):
    with open(cookie_file, "rb") as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        # Selenium requires expiry to be int if present
        if isinstance(cookie.get("expiry"), float):
            cookie["expiry"] = int(cookie["expiry"])
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"⚠️ Could not add cookie {cookie['name']}: {e}")

def scrape_x(keywords, batch_size=10):
    prospects = []
    driver = init_driver()
    driver.get("https://twitter.com/")   # open base URL
    load_cookies(driver)
    driver.refresh()   # now you’re logged in already

    for keyword in keywords:
        print(f"🔍 Searching X for: {keyword}")
        try:
            search_url = f"https://twitter.com/search?q={keyword}&f=live"
            driver.get(search_url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']"))
            )

            tweets = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")[:batch_size]

            for tweet in tweets:
                try:
                    handle_elem = tweet.find_element(By.XPATH, ".//div[@data-testid='User-Name']//span[contains(text(), '@')]")
                    handle = handle_elem.text.strip().lstrip('@')
                    profile_link = f"https://twitter.com/{handle}"

                    
                    content_elem = tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']")
                    content = content_elem.text.strip().replace("\n", " ")

                    tweet_url_elem = tweet.find_element(By.XPATH, ".//a[contains(@href, '/status/')]")
                    tweet_link = tweet_url_elem.get_attribute("href")

                    prospects.append({
                        "platform": "x",
                        "username": handle,
                        "profile_link": profile_link,
                        "bio": f"Tweet: {content} ({tweet_link})"
                    })
                except Exception as e:
                    print(f"⚠️ Failed to extract tweet details: {e}")
                    continue

            time.sleep(2)
        except Exception as e:
            print(f"❌ Error scraping X for keyword '{keyword}': {str(e)}")

    driver.quit()
    return prospects




