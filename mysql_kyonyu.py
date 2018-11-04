import re
import requests
import lxml.html
import MySQLdb

def main():
    conn = MySQLdb.connect(db='scraping',user='scraper',passwd='password',charset='utf8mb4')
    c = conn.cursor()
    
    '''
    #ここのブロックいらないかも
    sql = 'select ISBN from T_ORGNL_CONTENTS'
    c.execute(sql)
    rs = c.fetchall()
    
    x = []
    for s in rs:
        x.extend(s)
    y = set(x)
    '''
    
    #巨乳動画ストリームから取得
    url = "https://kyonyudouga.com/"
    
    #最後に取得したカウントNoを取得する
    #M_ORGNL_SITE:url,current_cnt,get_pages
    sql = "select current_cnt,get_pages from M_ORGNL_SITE where url = '{}'".format(url)
    c.execute(sql)
    rs = c.fetchone()
    current_cnt = rs[0]
    
    #1回あたりの取得ページ数を取得する
    get_pages = rs[1]
    
    #最新のカウントNoを取得する
    response = requests.get(url)
    max_cnt = scrape_max_count(response) #リアルタイムの最新カウントNo取得

    #最新のカウントNoに達していない場合のみ処理を実行
    #最後に取得した取得ページ数の次ページから捜索開始
    if int(max_cnt) > int(current_cnt):
        for i in range(current_cnt+1,current_cnt+get_pages):
            posts_url = url + "/archives/{}.html".format(i)                
            res = requests.get(posts_url)
            
            if res.status_code == 200:
                image_url = scrape_image_url(res)
            else:
                image_url = ""
            
            print(posts_url + " " + image_url +" "+ str(res.status_code))
    
    #current_cntは最新のカウントNoを超えさせない
    if i > int(max_cnt):
        current_cnt = max_cnt
    else:
        current_cnt = i
    
    #最後に取得したカウントNoを更新する
    sql = "update M_ORGNL_SITE set current_cnt = {} where url = '{}'".format(current_cnt,url)
    #c.execute(sql)
    conn.commit()
    
    conn.close()

def scrape_max_count(response):
    root = lxml.html.fromstring(response.content)
    url = root.cssselect('.posts')[0].cssselect('a')[0].get('href')
    m = re.search(r'/([^/]+)$',url)
    max_count = m.group(1).replace('.html','') 
    return max_count #intを返す

def scrape_image_url(response):
    root = lxml.html.fromstring(response.content)
    url = root.cssselect('#post_top')[0].cssselect('img')[0].get('src')
    return url #urlのstrを返す

def scrape_detail_page(response):
    root = lxml.html.fromstring(response.content)
    ebook = {
        'url':response.url,
        'ISBN':extract_key(response.url),
        'title':root.cssselect('#bookTitle')[0].text_content(),
        'price':root.cssselect('.buy')[0].text,
        'content':[normalize_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')],
    }
    return ebook #dictを返す

def normalize_spaces(s):
    return re.sub(r'\s+','',s).strip()

def extract_key(url):
    m = re.search(r'/([^/]+)$',url)
    return m.group(1)

if __name__ == '__main__':
    main()