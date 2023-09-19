import sys
from urllib.parse import urlparse

import indieweb_utils
import requests
from bs4 import BeautifulSoup

ME = "jamesg.blog"


def send_webmention(post_url, target_url):
    print(f"Found a link to {ME} on Reddit!")
    print("Link to post: " + post_url)
    print("Link to my website: " + target_url)

    try:
        indieweb_utils.send_webmention(post_url, target_url)
    except indieweb_utils.webmentions.discovery.WebmentionEndpointNotFound:
        print("Webmention endpoint not found.")
        return

    print("Webmention sent!")


def main():
    try:
        r = requests.get(
            "https://reddit.com/domain/jamesg.blog/.rss",
            headers={"User-Agent": "reddit-webmention-bot"},
        )
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    reddit_posts = BeautifulSoup(r.text, "html.parser").find_all("entry")

    for post in reddit_posts:
        post_content = BeautifulSoup(post.find("content").text, "html.parser")

        # get all urls that start with ME
        post_urls = []

        for link in post_content.find_all("a"):
            if link.get("href") is None:
                continue

            if urlparse(link.get("href")).netloc == ME:
                post_urls.append(link.get("href"))

        reddit_post_url = post.find("link").get("href")

        for post_url in post_urls:
            if post_url is not None and urlparse(post_url).netloc == ME:
                send_webmention(post_url, reddit_post_url)
                continue


main()
