import requests
import json

def main():
    password = 'WjAc PcZF 1qwT HNu2 t63B O8gT'
    user_id  = 'admin'
    end_point_url = 'https://douga01.mixh.jp/wp-json/wp/v2/posts'
    
    p_title = 'APIからの投稿'
    p_content = '内容のサンプル<br>aaaa'
    p_status = 'draft'
    
    payload = {
                'title':p_title,
                'content':p_content,
                'status':p_status
                }
    headers = {'content-type':'application/json'}
    
    r = requests.post(end_point_url,data=json.dumps(payload),headers=headers,auth=(user_id,password))
    print(r)

if __name__ == '__main__':
    main()