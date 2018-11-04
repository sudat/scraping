import re
import requests
import lxml.html

def main():
    session = requests.Session()
    response = session.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)
    for url in urls:
        response = session.get(url)
        ebook = scrape_detail_page(response)
        print(ebook)
        break

def scrape_list_page(response):
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)
    for a in root.cssselect('#listBook a[itemprop="url"]'):
        url=a.get('href')
        yield url

def scrape_detail_page(response):
    root = lxml.html.fromstring(response.content)
    
    #print([headmeta.get('content') for headmeta in root.cssselect('head > meta')]) 
    #実験。headタグ→metaタグのcontent属性を取得。
    
    ebook = {
        'url':response.url,
        'title':root.cssselect('#bookTitle')[0].text_content(),
        'price':root.cssselect('.buy')[0].text,
        'content':[normalize_spaces(h3.text_content()) for h3 in root.cssselect('#content > h3')],
    }
    return ebook #dictを返す

def normalize_spaces(s):
    return re.sub(r'\s+','',s).strip()

if __name__ == '__main__':
    main()