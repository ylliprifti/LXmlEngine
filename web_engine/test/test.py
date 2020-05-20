import requests
from lxml import html

xpath = "//div[contains(@class, 'ReviewsPage__Content')]//div[contains(@class, 'ReviewsItem__Wrapper')]"

with requests.get("https://www.checkatrade.com/trades/ShineYourHome/reviews") as web_request:
    html_element = html.fromstring(web_request.content)
    elements = html_element.xpath(xpath)
    for div in elements:
        print(div)

if __name__ == "__main__":
    pass
