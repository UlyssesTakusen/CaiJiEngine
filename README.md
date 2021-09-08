# CaiJiEngine

> CaiJiEngine是一款基于Python3的URL采集工具，支持使用百度，必应，谷歌搜索引擎进行URL采集。
>
> 可打印格式：URL、域名、协议+域名。
>
> 结合Google Hacking语法食用更佳。：）

## 使用

### Usage

```
usage: CaiJi.py [-h] [-E ENGINE] -K KEYWORDS [-P {url,domain,domainpro}] [-C COUNTS] [-d] [-O OUTPUT] [-V]

optional arguments:
  -h, --help            show this help message and exit
  -E ENGINE, --engine ENGINE
                        Use the following search engines to collect: [Baidu], [Bing], [Google] (default:Baidu)
  -K KEYWORDS, --keywords KEYWORDS
                        Enter the keywords you want to query
  -P {url,domain,domainpro}, --print {url,domain,domainpro}
                        Print as follows: [url], [domain], [domainpro] (default:domainpro)
  -C COUNTS, --counts COUNTS
                        Number of pages found (default:5)
  -d, --detail          View crawling details
  -O OUTPUT, --output OUTPUT
                        Output file
  -V, --version         show program's version number and exit

```



### 安装

需要安装Python3.6以上环境

```
git clone git://github.com/UlyssesTakusen/CaiJiEngine
cd CaiJiEngine
pip3 install -r requirements.txt
python3 CaiJi.py -h
```



### 基本使用

```
python3 CaiJi.py -K intitle:后台登录 -P url -d
python3 CaiJi.py -K site:baidu.com -E Bing,Baidu -O baidu.csv
```

