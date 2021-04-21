# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import json
from util.youtube import YoutubeModule

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
testClient = "util/client_id.json"
clientPath = "util/client_secret_73593820896-vsttr5tpok1qc29605dt13soc6co6dmh.apps.googleusercontent.com"
check = True
searchData = dict(
    part="snippet",
    q="Hololive中文|烤肉|熟肉",
    maxResults=50,
    relevanceLanguage="zh_hant",
    type="channel"
)


def _checkLog(data, title):
    print("{} =>".format(title), data, '\n')


def main():
    youtube = YoutubeModule()
    response = youtube.youtubeApi(searchData)
    # response = youtubeApi(**searchData)
    PageInfo = response['pageInfo']  # 將 PageInfo 之值存進 PageInfo 此 dictionary 中
    TotalResult = PageInfo['totalResults']
    ResultPerPage = PageInfo['resultsPerPage']
    itemGet = response['items']
    ResultnextPageToken = response['nextPageToken']
    ResultChannelTitle = []
    ResultChannelId = []
    # ResultOutPut = {}

# 測試確認用之輸出
    _checkLog(response, "response")
    _checkLog(itemGet, "itemGet")
    _checkLog(ResultnextPageToken, "ResultnextPageToken")
    _checkLog(len(itemGet), "itemGet Length")
    _checkLog(type(TotalResult), "TotalResult Type")
    _checkLog(type(ResultPerPage), "ResultPerPage Type")

# /測試確認用之輸出

    for i in range(len(itemGet)):  # 將取得的ID與Title儲存進lst
        # add null check when itemGet is null data (not sure)
        if itemGet[i] is None:
            return
        ResultChannelTitle.append(itemGet[i]['snippet']['channelTitle'])
        ResultChannelId.append(itemGet[i]['id']['channelId'])

# 若有複數搜尋頁面
    def loopSearchData(items):
        for i in range(len(items)):  # 將取得的ID與Title儲存進lst
            ResultChannelTitle.append(
                items[i]['snippet']['channelTitle'])
            ResultChannelId.append(items[i]['id']['channelId'])

    def getNextPage(response, nextPageToken):
        if nextPageToken is '':
            return

        if ('nextPageToken' in response) and (nextPageToken != ''):  # 判斷是否還有下一頁
            nextSearchData = dict(  # 第二次開始之呼叫，含 nextPageToken
                part="snippet",
                q="Hololive中文|烤肉|熟肉",
                pageToken="%s" % response['nextPageToken'],
                maxResults=50,
                relevanceLanguage="zh_hant",
                type="channel"
            )
            response = youtube.youtubeApi(nextSearchData)
            if 'nextPageToken' in response:
                nextPageToken = response['nextPageToken']
            else:
                nextPageToken = ''

            itemGet = response['items']
            loopSearchData(itemGet)

        return getNextPage(response, nextPageToken)

    getNextPage(response, ResultnextPageToken)

    # 以 ChannelTitle 為 Key，ChannelID 為 Value 儲存進 ResultOutPut 此 dictionary 進行接下來之跨程式傳遞值
    _checkLog(len(ResultChannelId), "ResultChannelId Length")
    _checkLog(ResultChannelId, "ResultChannelId")
    _checkLog(len(ResultChannelTitle), "ResultChannelTitle Length")

    ResultOutPut = dict(zip(ResultChannelTitle, ResultChannelId))

    _checkLog(ResultOutPut, "ResultOutPut")
    with open("TestStorage2.json", "w", encoding='utf-8') as f:  # 儲存成 .json 檔案
        json.dump(ResultOutPut, f, ensure_ascii=False)
        print("成功創建 json 檔案")


if __name__ == "__main__":
    main()
