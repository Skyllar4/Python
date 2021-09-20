import requests
import os
from requests.exceptions import HTTPError
from urllib.parse import urlparse


def shorten_url(bitly_token, url):
    bit_url = "https://api-ssl.bitly.com/v4/shorten"
    params = {"long_url": url}
    headers = {"Authorization": "Bearer {}".format(bitly_token)}
    response = requests.post(bit_url, json=params, headers=headers)
    response.raise_for_status()
    return response.text


def count_clicks(bitly_token, link):
    bit_url = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(
        link)
    params = {"unit": "day", "units": "-1"}
    headers = {"Authorization": "Bearer {}".format(bitly_token)}
    response = requests.get(bit_url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(bitly_token, url):
    bit_url = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(url)
    headers = {"Authorization": "Bearer {}".format(bitly_token)}
    response = requests.get(bit_url, headers=headers)
    return response.ok


def main():
    token = os.environ["BITLY_ACCESS_TOKEN"]
    url = input()
    url_parse = urlparse(url)
    if url_parse.scheme:
        url_with_protocol = url
    else:
        url_with_protocol = f"http://{url}"
    url_without_protocol = f"{url_parse.netloc}{url_parse.path}"

    if is_bitlink(token, url_without_protocol):
        print(count_clicks(token, url_without_protocol))
    else:
        try:
            print(shorten_url(token, url_with_protocol))
        except HTTPError:
            print("Неправильная ссылка: ", url)


if __name__ == "__main__":
    main()
