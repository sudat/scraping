import requests
import json
import urllib.request

def main():
    password = 'WjAc PcZF 1qwT HNu2 t63B O8gT'
    user_id  = 'admin'
    end_point_url_post = 'https://douga01.mixh.jp/wp-json/wp/v2/posts'
    end_point_url_media = 'https://douga01.mixh.jp/wp-json/wp/v2/media'

    response = post_image(user_id,password,end_point_url_media)
    data = response.json()
    #print(json.dumps(data,indent=4))
    
    p_title = 'APIからの投稿'
    p_content = '内容のサンプル<br>aaaa'
    p_status = 'draft'
    p_tags = '2'
    p_media = data["id"]
    
    payload = {
                'title':p_title,
                'content':p_content,
                'status':p_status,
                'tags':p_tags,
                'featured_media':p_media #アイキャッチ画像
                }
    headers = {'content-type':'application/json'}
    
    r = requests.post(end_point_url_post,data=json.dumps(payload),headers=headers,auth=(user_id,password))
    print(r)

def post_image(user_id,password,end_point_url):
    url='https://sociorocketnews.files.wordpress.com/2018/04/mokichi004.jpg?w=640&h=480'
    img_data = urllib.request.urlopen(url).read()
    file_name = 'neko.jpg'

    p_headers = {
        'Content-Disposition':'attachment; filename="{}"'.format(file_name),
        'Content-type':'application/octet-stream'
    }
    
    response = requests.post(end_point_url,data=img_data,headers=p_headers,auth=(user_id,password))
    print(response)
    return response

if __name__ == '__main__':
    main()