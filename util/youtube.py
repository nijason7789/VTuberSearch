import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


class YoutubeModule:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.credentials = None
        self.getCredentials()

    def getCredentials(self):
        client_secrets_file = "util/client_secret_73593820896-vsttr5tpok1qc29605dt13soc6co6dmh.apps.googleusercontent.com.json"
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        self.credentials = flow.run_local_server(port=0)

    def youtubeApi(self, searchData):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"

        # credentials = flow.run_local_server(port=0)
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=self.credentials)
        request = youtube.search().list(
            **searchData
        )
        response = request.execute()
        return response
