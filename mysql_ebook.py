import re
import requests
import lxml.html
import MySQLdb

def main():
    conn = MySQLdb.connect(db='scraping',user='scraper',passwd='password',charset='utf8mb4')
    c = conn.cursor()
    
    sql = 'select ISBN from ebook'
    c.execute(sql)
    rs = c.fetchall()

    x = []
    for s in rs:
        x.extend(s)
    y = set(x)

    response = requests.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)
    for url in urls:
        key = extract_key(url)
        if key not in y:
            response = requests.get(url)
            ebook = scrape_detail_page(response)
            print(ebook['url']+ebook['ISBN']+ebook['title'])
            sql = 'INSERT INTO ebook(url,ISBN,title) values(%s,%s,%s)'
            c.execute(sql,(ebook['url'],ebook['ISBN'],ebook['title']))
    conn.commit()
    conn.close()

def scrape_list_page(response):
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)
    for a in root.cssselect('#listBook a[itemprop="url"]'):
        url=a.get('href')
        yield url

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