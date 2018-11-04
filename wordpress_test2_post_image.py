
import requests
import urllib.request
import json

def main():
    password = 'WjAc PcZF 1qwT HNu2 t63B O8gT'
    user_id  = 'admin'
    end_point_url = 'https://douga01.mixh.jp/wp-json/wp/v2/media'
    
    url='https://sociorocketnews.files.wordpress.com/2018/04/mokichi004.jpg?w=640&h=480'
    img_data = urllib.request.urlopen(url).read()
    file_name = 'neko.jpg'
    
    p_headers = {
        'Content-Disposition':'attachment; filename="{}"'.format(file_name),
        'Content-type':'application/octet-stream'
    }
    
    response = requests.post(end_point_url,data=img_data,headers=p_headers,auth=(user_id,password))
    print(response)
    
if __name__ == '__main__':
    main()