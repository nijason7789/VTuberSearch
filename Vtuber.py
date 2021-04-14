# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

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

    request = youtube.search().list(
        part="snippet",
        q="Hololive中文|烤肉|熟肉",
        maxResults = 50,
        relevanceLanguage="zh_hant",
        type="channel"
    )
    itemGet = {}
    response = request.execute()
    itemGet = response['items']

    print(response,'\n')
    print(itemGet,'\n')
    print(len(itemGet))

    i = 0
    for i in range(len(itemGet)):
        print(itemGet[i]['snippet']['channelTitle'])
        print(itemGet[i]['id']['channelId'],'\n')
    

if __name__ == "__main__":
    main()