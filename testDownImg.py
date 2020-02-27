import requests
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def DownloadImg(url, urlOfFileName):
    retry_count = 5
    while True:
        proxy = get_proxy().get("proxy")
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Referer': 'https://www.mzitu.com'
        }
        while retry_count > 0:
            try:
                myResponse = requests.get(url, headers=headers,proxies= {"http": "http://{}".format(proxy)})
                break
            except Exception:
                print(myResponse.status_code)
                retry_count -= 1
        if retry_count > 0:
            break

    filename = urlToFileName(urlOfFileName)
    with open(filename, 'wb') as fin:
        fin.write(myResponse.content)
if __name__ == "__main__":
    # DownloadImg('https://i5.mmzztt.com/2019/09/22b01.jpg','https://www.mzitu.com/204278')
    proxy=get_proxy()
    print(proxy)
    print({"http://{}".format(proxy.get('proxy'))})