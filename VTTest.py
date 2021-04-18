# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
from util.youtube import youtubeApi
# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# import googleapiclient.errors


def main():
    searchData = dict(
        part="snippet",
        maxResults=25,
        q="surfing"
    )
    response = youtubeApi(searchData)
    print(response)


if __name__ == "__main__":
    main()
