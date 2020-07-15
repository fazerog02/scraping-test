import requests
from requests_toolbelt import MultipartEncoder
from bs4 import BeautifulSoup as BS
import chromedriver_binary
from selenium import webdriver
import time


POST_URL = "https://www.google.co.jp/searchbyimage/upload"
IMAGE_NAME = "samples/tanpopo.jpg"


class ResultData():
    def __init__(self, title, url, description):
        self.title = title
        self.url = url
        self.description = description


def getSearchResultUrl(image):
    data = MultipartEncoder(
        fields={
            "encoded_image": (IMAGE_NAME, image, 'image/'+IMAGE_NAME.split('.')[1]),
        }
    )
    res = requests.post(url=POST_URL, data=data, headers={"Content-Type": data.content_type})
    res.encoding = res.apparent_encoding
    return res.url.replace("webhp", "search")


def getResultHtml(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    result_html = driver.page_source
    driver.quit()
    return result_html


def parseResultHtml(html_str):
    bs = BS(html_str, 'html.parser')

    search_div = bs.find(id="search")
    result_divs = search_div.find_all(class_="rc")

    result_data_list = []
    for result_div in result_divs:
        result_data_div = result_div.find(class_="r")
        result_title = result_data_div.find(class_="LC20lb DKV0Md").text
        result_url = result_data_div.find("a").get("href")
        result_description = result_div.find(class_="st").text
        result_data_list.append(
            ResultData(
                title=result_title,
                url=result_url,
                description=result_description
            )
        )

    return result_data_list


def main():
    with open(IMAGE_NAME, 'rb') as image:
        res_url = getSearchResultUrl(image)

    res_html = getResultHtml(res_url)
    res_data_list = parseResultHtml(res_html)

    print("検索結果")
    for res_data in res_data_list:
        print("- "+res_data.title)
        print("  - " + res_data.url)
        print("  - " + res_data.description+"\n\n")


if __name__ == '__main__':
    main()

