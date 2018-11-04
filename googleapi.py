import json
import requests
from oauth2client.client import OAuth2WebServerFlow
import webbrowser
from oauth2client.file import Storage

def main():
    
    ACCESS_TOKEN = get_token()

    flow = OAuth2WebServerFlow(
        client_id = "368365107470-ajh4j02qe867kdft1ligb9qepq8jdtut.apps.googleusercontent.com",
        client_sercret = "1AapNjX55YoQFEfv0N_Z8BHq",
        scope='https://picasaweb.google.com/data/',
        redirect_uri="urn:ietf:wg:oauth:2.0:oob"
    )

    auth_uri = flow.step1_get_authorize_url()
    webbrowser.open(auth_uri)

    token = input("Input your code > ")

    credentials = flow.step2_exchange(token)

    # file.Storage
    storage = Storage('secret/credentials')
    storage.put(credentials)
    # with文を使用するように変更 1.
    with open("secret/credentials") as json_file:
        load = json.load(json_file)

    access_token = load["access_token"]
    user_id = 'default'
    # エンドポイントを変更 2.
    url = 'https://picasaweb.google.com/data/feed/api/user/{}'.format(user_id)
    # headerを変更 3.
    head = {'Authorization': 'OAuth {}'.format(access_token)}
    print(response)


    '''
    #空のアルバムを作成
    headers = {
        'Authorization': "Bearer " + ACCESS_TOKEN,
        'Content-type': 'application/json'
    }
    data = '{ "album": { "title":"kyonyu_doga" } }'
    response = requests.post('https://photoslibrary.googleapis.com/v1/albums', headers=headers, data=data)
    print(response.status_code)
    
    data = response.json()
    print(json.dumps(data,indent=4))
    

    #アルバム一覧を取得
    headers = {'Authorization': "Bearer " + ACCESS_TOKEN}
    response = requests.get('https://photoslibrary.googleapis.com/v1/albums', headers=headers)    
    print(response.status_code)
    
    data = response.json()
    #print(json.dumps(data,indent=4))
    
    #Uploadトークンを取得
    headers = {
        'Authorization': "Bearer " + ACCESS_TOKEN ,
        'Content-type': 'application/octet-stream',
        'X-Goog-Upload-File-Name': '123.jpg',
        'X-Goog-Upload-Protocol': 'raw'
    }

    data = open('mokichi004.jpg', 'rb').read()
    response = requests.post('https://photoslibrary.googleapis.com/v1/uploads', headers=headers, data=data)
    #print(response.status_code)
    UPLOAD_TOKEN = response.text
    ALBUM_ID = "AO7aam3jvKrwXxagmtITMeUVJnIO9gfCHxagXCVEcdGx_93nsnrq3gcTS-R6mETYKIaQ8fxyMPgg"
    #print(UPLOAD_TOKEN)
    
    #メディアのアップロード
    headers = {
        'Authorization': "Bearer " + ACCESS_TOKEN ,
        'Content-type': 'application/json',
    }
    data = '{"albumId":"%s","newMediaItems":[{"simpleMediaItem":{"uploadToken":"%s"}}]}' % (ALBUM_ID,UPLOAD_TOKEN)
    print(data)

    response = requests.post('https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate', headers=headers, data=data)
    print(response.status_code)
    print(response.text)

    '''
    
    
    
    
    
def get_token():
    REFRESH_TOKEN = "1/Iq0MsG585P0u2ATBaodAAbHr6dP2Fz3N2zaUVMgQjxc"
    CLIENT_ID = "368365107470-ajh4j02qe867kdft1ligb9qepq8jdtut.apps.googleusercontent.com"
    CLIENT_SERCRET = "1AapNjX55YoQFEfv0N_Z8BHq"
    # "expires_in": 3600,
    # "scope": "https://www.googleapis.com/auth/photoslibrary",
    # "token_type": "Bearer"
    
    data = {
      'refresh_token': REFRESH_TOKEN,
      'client_id': CLIENT_ID,
      'client_secret': CLIENT_SERCRET,
      'grant_type': 'refresh_token'
    }

    response = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
    data = response.json()
    return data["access_token"]
    
    #print(json.dumps(data,indent=4))

if __name__ == '__main__':
    main()