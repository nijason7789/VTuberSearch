# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_73593820896-vsttr5tpok1qc29605dt13soc6co6dmh.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.search().list(    #第一次呼叫，不含 nextPageToken
        part="snippet",
        q="Hololive中文|烤肉|熟肉",
        maxResults = 50,
        relevanceLanguage="zh_hant",
        type="channel"
    )
    response = request.execute() #執行
    PageInfo = response['pageInfo']
    TotalResult = PageInfo['totalResults']
    ResultPerPage = PageInfo['resultsPerPage']
    itemGet = response['items']
    ResultnextPageToken = response['nextPageToken']
    ResultChannelTitle = []
    ResultChannelId = []
    ResultOutPut = {}

#測試確認用之輸出

    print(response,'\n')
    print(itemGet,'\n')
    print(ResultnextPageToken,'\n')
    print(len(itemGet))
    print(type(request))
    print(type(TotalResult))
    print(type(ResultPerPage))

#/測試確認用之輸出

    i = 0 

    for i in range(len(itemGet)):   #將取得的ID與Title儲存進lst
        ResultChannelTitle.append(itemGet[i]['snippet']['channelTitle'])
        ResultChannelId.append(itemGet[i]['id']['channelId'])
        print(ResultChannelTitle[i])
        print(ResultChannelId[i],'\n')

#若有複數搜尋頁面
    n = 0

    if ResultnextPageToken != "":   #判斷是否還有下一頁
        if TotalResult%ResultPerPage == 0:  #判斷有幾來，要執行幾次
            for n in range(TotalResult/ResultPerPage):  
                request = youtube.search().list(    #第二次開始之呼叫，含 nextPageToken
                    part="snippet",
                    q="Hololive中文|烤肉|熟肉",
                    pageToken = "%s"%ResultnextPageToken,
                    maxResults = 50,
                    relevanceLanguage="zh_hant",
                    type="channel"
                )
                response = request.execute() #執行
                if 'nextPageToken' in response: #判斷是否還有下一頁
                    ResultnextPageToken = response['nextPageToken']
                itemGet = response['items']
                print(ResultnextPageToken)
                i = 0 

                for i in range(len(itemGet)):   #將取得的ID與Title儲存進lst
                    ResultChannelTitle.append(itemGet[i]['snippet']['channelTitle'])
                    ResultChannelId.append(itemGet[i]['id']['channelId'])
                    #print(ResultChannelTitle[i])
                    #print(ResultChannelId[i],'\n')
        else:
            for n in range(TotalResult//ResultPerPage+1):
                request = youtube.search().list(    #第二次開始之呼叫，含 nextPageToken
                    part="snippet",
                    q="Hololive中文|烤肉|熟肉",
                    pageToken = "%s"%ResultnextPageToken,
                    maxResults = 50,
                    relevanceLanguage="zh_hant",
                    type="channel"
                )
                response = request.execute() #執行
                if 'nextPageToken' in response: #判斷是否還有下一頁
                    ResultnextPageToken = response['nextPageToken']
                itemGet = response['items']
                print(ResultnextPageToken)
                i = 0 

                for i in range(len(itemGet)):   #將取得的ID與Title儲存進lst
                    ResultChannelTitle.append(itemGet[i]['snippet']['channelTitle'])
                    ResultChannelId.append(itemGet[i]['id']['channelId'])
                    #print(ResultChannelTitle[i])
                    #print(ResultChannelId[i],'\n')
   
                print(ResultChannelTitle,'\n')
                print(ResultChannelId,'\n')
    i = 0

    for i in range(len(ResultChannelId)):
        ResultOutPut[ResultChannelTitle[i]] = ResultChannelId[i]

    print(ResultOutPut)
    SearchChannelMethod = json.dumps(ResultOutPut, separators=(',\n',': '),ensure_ascii=False)
    print(SearchChannelMethod)

    with open("TestStorage.json","w", encoding='utf-8') as f:   #儲存成 .json 檔案
        json.dump(SearchChannelMethod,f, ensure_ascii=False)
        print("載入入檔案完成...")
    



    

if __name__ == "__main__":
    main()