import requests,time,threading
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import re
import argparse
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class Spider(object):
    keywords = ""
    heads = ""
    counts = 10
    origin_urls = []
    urls = []
    domains = []
    domainsPro = []
    page_urls = []
    threads = []

    def __init__(self,keywords,heads):
        self.keywords = keywords
        self.heads = heads

    # 通过百度搜索引擎爬取
    def GetBaiduUrl(self):
        for i in range(0, self.counts, 10):
            self.page_urls.append('https://www.baidu.com/s?wd=' + self.keywords + '&pn=' + format(i) + '&oq=site%3Abaidu.com&tn=02003390_hao_pg&ie=utf-8&usm=2&rsv_idx=2')

    def BaiduCrawl(self,url):
        r = requests.get(url,headers=self.heads)
        soup = BeautifulSoup(r.content,'html.parser',from_encoding="utf-8")
        raw_url = soup.find_all(name='a',attrs={'data-click':re.compile('.'),'class':None})

        for raw in raw_url:
            try:
                trick_url = raw['href']
                response = requests.get(trick_url, headers=self.heads, timeout=(5), verify=False)
                self.origin_urls.append(response.url)
            except (requests.exceptions.RequestException, ValueError):
                pass

    def Baidu_multi_thread(self):
        self.threads = []
        for url in self.page_urls:
            self.threads.append(
                threading.Thread(target=Spider.BaiduCrawl, args=(self,url,))
            )
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

    # 通过Bing搜索引擎爬取
    def GetBingUrl(self):
        for i in range(1,self.counts,10):
            self.page_urls.append('https://cn.bing.com/search?q='+self.keywords+'&first='+format(i))

    def BingCrawl(self,url):
        r = requests.get(url, headers=self.heads)
        soup = BeautifulSoup(r.content, 'html.parser' ,from_encoding="iso-8859-1")
        raw_url = soup.find_all(name='a', attrs={'target': "_blank", 'class': None, 'id': None})

        for raw in raw_url:
            try:
                trick_url = raw['href']
                response = requests.get(trick_url, headers=self.heads, timeout=(5), verify=False)
                self.origin_urls.append(response.url)
            except (requests.exceptions.RequestException, ValueError):
                pass

    def Bing_multi_thread(self):
        self.threads = []
        for url in self.page_urls:
            self.threads.append(
                threading.Thread(target=Spider.BingCrawl, args=(self,url,))
            )
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

    # 通过Google搜索引擎爬取
    def GetGoogleUrl(self):
        for i in range(0,self.counts,10):
            self.page_urls.append('https://www.google.com.hk/search?q='+self.keywords+'&newwindow=1&start='+format(i)+'&sa=N')

    def GoogleCrawl(self,url):
        r = requests.get(url,headers=self.heads)
        soup = BeautifulSoup(r.content,'html.parser',from_encoding="utf-8")
        raw_url = soup.find_all(name='a',attrs={'target':"_blank",'class':None})


        for raw in raw_url:
            try:
                trick_url = raw['href']
                response = requests.get(trick_url, headers=self.heads, timeout=(10), verify=False)
                self.origin_urls.append(response.url)
            except (requests.exceptions.RequestException, ValueError):
                pass

    def Google_multi_thread(self):
        self.threads = []
        for url in self.page_urls:
            self.threads.append(
                threading.Thread(target=Spider.GoogleCrawl, args=(self,url,))
            )
        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

    # 通过URL形式输出
    def GetUrls(self):
        self.urls = list(set(self.origin_urls))
        for url in self.urls:
            print(url)


    # 通过域名形式输出
    def GetDomain(self):
        origin_domains = []
        for url in self.origin_urls:
            try:
                origin_domains.append(re.sub('^https?://','',re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',url)[0]))
                self.domains = list(set(origin_domains))
            except IndexError:
                pass
        for domain in self.domains:
            print(domain)



    # 通过协议+域名形式输出
    def GetDomainWithProtocol(self):
        origin_domainsPro = []
        for url in self.origin_urls:
            try:
                origin_domainsPro.append(re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',url)[0])
                self.domainsPro = list(set(origin_domainsPro))
            except IndexError:
                pass
        for domainPro in self.domainsPro:
            print(domainPro)

def main():
    global heads
    heads = {
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }

    # 脚本参数列表
    parser = argparse.ArgumentParser()
    parser.add_argument("-E","--engine",help="Use the following search engines to collect: [Baidu], [Bing], [Google] (default:Baidu)", default="Baidu")
    parser.add_argument("-K","--keywords",help="Enter the keywords you want to query",required=True)
    parser.add_argument("-P","--print",choices=["url","domain","domainpro"],help="Print as follows: [url], [domain], [domainpro] (default:domainpro)", default="domainpro")
    parser.add_argument("-C","--counts",help="Number of pages found (default:5)" ,type=int ,default=5)
    parser.add_argument("-O","--output",help="Output file",required=False)
    parser.add_argument("-V", "--version", action='version',version='v1.1')

    args = parser.parse_args()

    if args.keywords:
        keywords = args.keywords
        spider = Spider(keywords,heads)

    if args.counts:
        spider.counts = args.counts*10

    print("\n正在爬取中...\n")
    if "Baidu" in args.engine:
        spider.GetBaiduUrl()
        spider.Baidu_multi_thread()
    if "Bing" in args.engine:
        spider.GetBingUrl()
        spider.Bing_multi_thread()
    if "Google" in args.engine:
        spider.GetGoogleUrl()
        spider.Google_multi_thread()

    print("\n输入结果：\n")
    if args.print == 'url':
        spider.GetUrls()
    if args.print == 'domain':
        spider.GetDomain()
    if args.print == 'domainpro':
        spider.GetDomainWithProtocol()

    if args.output:
        f = open(args.output,"w")
        str = "\n"
        if args.print == 'url':
            f.write(str.join(spider.urls))
        if args.print == 'domain':
            f.writelines(str.join(spider.domains))
        if args.print == 'domainpro':
            f.writelines(str.join(spider.domainsPro))
        f.close()
        print("\n已保存结果为："+args.output)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("\n总共花费时间：", end - start, "s")
