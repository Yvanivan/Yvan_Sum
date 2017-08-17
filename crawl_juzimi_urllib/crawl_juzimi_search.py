#-*- coding:utf-8 _*-
import sys,urllib,urllib2,os,json
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')
""" 
@author:Yesus 
@file: crawl_juzimi_search.py 
@time: 2017/08/15 
"""

# 句子迷网站，搜索关键词（书名）
def postUrl(title):
    name = './html/' + title + '_' + 'SearchResultPage' + '.html'
    if  os.path.exists('./html/'+title.decode('utf-8')+'_SearchResultPage.html'):
        filew = open(name.decode('utf-8'), 'a')
        print name+' 搜索结果页已存在，无须请求'
        return filew.name,title
    else:
        print ' 数据不存在，重新获取'
        params = urllib.quote(title)
        url = "http://www.juzimi.com/search/node/%s" % (params)+'%20type:sentence'
        req = urllib2.Request(url)
        req.add_header('User-agent', 'Mozilla 5.10')
        response = urllib2.urlopen(req)
        the_page = response.read()

        filew = open(name.decode('utf-8'),'a')
        filew.write(the_page)
        print filew.name
        return filew.name,title

def requestUrlbyGet(url,savepath):
    if os.path.exists(savepath):
        print savepath+' 页面已存在，无需请求'
        pass
    else:
        req = urllib2.Request(url)
        print url
        req.add_header('User-agent', 'Mozilla 5.10')
        response = urllib2.urlopen(req)
        the_page = response.read()
        print response.getcode()
        filew = open(savepath, 'a')
        filew.write(the_page)

def sent_requestUrlbyGet(url,savepath,num):
    if os.path.exists(savepath.replace('.html','1.html')):
        print savepath+' 页面已存在，无需请求'
        pass
    else:
        num = num / 10 + 1
        for i in range(0,num):
            real_url = url+'?page='+str(i)
            real_savepath = savepath.replace('.html',str(i)+'.html')
            print real_savepath
            print real_url
            i += 1

            req = urllib2.Request(real_url)
            req.add_header('User-agent', 'Mozilla 5.10')
            response = urllib2.urlopen(req)
            the_page = response.read()
            print response.getcode()
            filew = open(real_savepath, 'a')
            filew.write(the_page)



def readhtml_SearchResult(path):
    savepath = path.split('_')[0].replace('html','data').decode('utf-8')+'_SearchResult.txt'
    data = {}
    file = open(path, 'r')
    html = etree.HTML(file.read())
    result = html.xpath("//div[@class='wridesccon']/text()")[0]
    print '---读取搜索结果html'
    data['title'] = path.split('_')[0].split('./html')[0]
    data['description'] = result
    result_url = html.xpath("//div[@class='searchrightinfotop']/a/@href")[0]
    url = 'http://www.juzimi.com' + result_url

    data['url'] = url


    if os.path.exists(savepath):
        print savepath+' 文件已存在'
        return data
        pass
    else:
        print '写文件 ' + savepath
        filew = open(savepath,'a')
        filew.write(json.dumps(data, ensure_ascii=False, indent=4))
        return data

def readhtml_Description(path):
    savepath = path.split('_')[0].replace('html','data').decode('utf-8') + '_Book_description.txt'
    file = open(path, 'r')
    html = etree.HTML(file.read())
    data = {}
    result = html.xpath("//div[@class='jianjiecontext']//text()")
    authorurl = html.xpath("//div[@class='jianjiezuopinswriterdesc']//a//@href")[0]
    all_sentence_url = html.xpath("//div[@class='jianjieyulu']//ol//span//a//@href")[0]
    sentence_num = html.xpath("//div[@class='jianjieyulu']//h2//text()")[1].split('(')[1].split(')')[0]
    print sentence_num
    desc = ''
    for res in result:
        desc = desc + res.replace('\r','<br>')
    data['book_description'] = desc
    data['author_url'] = 'http://www.juzimi.com'+authorurl
    data['all_sentence_url'] = 'http://www.juzimi.com'+all_sentence_url
    data['sentence_num'] = sentence_num

    if os.path.exists(savepath):
        print savepath+' 文件已存在，直接读取'
        return data
        pass
    else:
        print '写文件 '+savepath
        filew = open(savepath,'a')
        filew.write(json.dumps(data, ensure_ascii=False, indent=4))
        return data

def readhtml_Author_Description(path):
    file = open(path, 'r')
    html = etree.HTML(file.read())
    data = {}
    savepath = path.split('_')[0].replace('html','data').decode('utf-8') + '_Author_description.txt'
    result = html.xpath("//div[@class='jianjiecontent']//text()")
    desc = ''
    for res in result:
        desc = desc + res.replace('\r','<br>')
    data['author_description'] = desc
    if os.path.exists(savepath):
        print savepath+' 文件已存在，直接读取'
        return data
        pass
    else:
        print '写文件 '+savepath
        filew = open(savepath,'a')
        filew.write(json.dumps(data, ensure_ascii=False, indent=4))
        return data

def readhtml_SentenceResult(path):
    file = open(path,'r')
    html = etree.HTML(file.read())
    sentence_savepath = path.split('_')[0].replace('html','data').decode('utf-8')+'_Sentences.txt'
    sentenceurl_savepath =  path.split('_')[0].replace('html','data').decode('utf-8')+'_SentencesUrl.txt'
    num_url = html.xpath("//div[@class='wridesccon']//a//@href")[0]
    num_url = 'http://www.juzimi.com' + num_url
    print num_url
    result = html.xpath("//div[@class='view-content']//div[@class='views-field-phpcode']/div/a[@class='xlistju']/@href")
    data = {}
    urldata = {}
    i = 1
    j = 1
    for res in result:
        xpath_str = "//div[@class='view-content']//div[@class='views-field-phpcode']/div/a[@href='"+res+"']/text()"
        urldata['url_'+str(j)] = res
        j += 1
        sents = html.xpath(xpath_str)
        sentstr = ''
        for sent in sents:
            sentstr = sentstr + sent.replace('\r','<br>')
        data[str(i)] = sentstr
        i += 1

    if os.path.exists(sentenceurl_savepath) and os.path.exists(sentence_savepath):
        print sentenceurl_savepath+' and '+sentence_savepath+' 文件已存在，直接读取'
        return data
        pass
    else:
        if os.path.exists(sentenceurl_savepath):
            os.remove(sentenceurl_savepath)
        if os.path.exists(sentence_savepath):
            os.remove(sentence_savepath)

        print '写文件 '+sentence_savepath+' and '+sentenceurl_savepath
        filew = open(sentence_savepath, 'a')
        filewurl = open(sentenceurl_savepath, 'a')
        filew.write(json.dumps(data, ensure_ascii=False, indent=4))
        filewurl.write(json.dumps(urldata, ensure_ascii=False, indent=4))
        # return data
        return num_url

    # print '---读取句子结果html'
    # filew.write(json.dumps(data,ensure_ascii=False,indent=4))
    # filewurl.write(json.dumps(urldata, ensure_ascii=False, indent=4))
    # result_url = html.xpath("//div[@class='searchrightinfotop']/a/@href")[0]
    # url = 'http://www.juzimi.com'+result_url
    # return url


def readhtml_All_SentenceResult(path,PageNum):
    path = path.replace('Sentence','AllSentence')
    num = PageNum/10 + 1
    sentence_savepath = path.split('_')[0].replace('html', 'data').decode('utf-8') + '_ALL_Sentences.txt'
    sentenceurl_savepath = path.split('_')[0].replace('html', 'data').decode('utf-8') + '_ALL_SentencesUrl.txt'

    data = {}
    urldata = {}
    k = 1
    j = 1
    for i in range(0,num):
        realpath = path.replace('Page','Page'+str(i))
        i += 1
        file = open(realpath, 'r')
        html = etree.HTML(file.read())
        result = html.xpath("//div[@class='view-content']//div[@class='views-field-phpcode']/div/a[@class='xlistju']/@href")

        for res in result:
            xpath_str = "//div[@class='view-content']//div[@class='views-field-phpcode']/div/a[@href='" + res + "']/text()"
            urldata['url_' + str(j)] = res
            j += 1
            sents = html.xpath(xpath_str)
            sentstr = ''
            for sent in sents:
                sentstr = sentstr + sent.replace('\r', '<br>')
            data[str(k)] = sentstr
            k += 1

    if os.path.exists(sentenceurl_savepath) and os.path.exists(sentence_savepath):
        print sentenceurl_savepath + ' and ' + sentence_savepath + ' 文件已存在，直接读取'
        return data
        pass
    else:
        if os.path.exists(sentenceurl_savepath):
            os.remove(sentenceurl_savepath)
        if os.path.exists(sentence_savepath):
            os.remove(sentence_savepath)

        print '写文件 ' + sentence_savepath + ' and ' + sentenceurl_savepath
        filew = open(sentence_savepath, 'a')
        filewurl = open(sentenceurl_savepath, 'a')
        filew.write(json.dumps(data, ensure_ascii=False, indent=4))
        filewurl.write(json.dumps(urldata, ensure_ascii=False, indent=4))
        # return data
        return 0


if __name__ == '__main__':
    name,params = postUrl('鲁滨逊漂流记')



    # 读取搜索结果页html，获取url
    ResultData = readhtml_SearchResult(name)
    url = ResultData['url']
    # desc_url = ResultData['num_url']
    #desc_url = url.replace('article','jianjiejieshao')

    # 配置保存路径
    sentspath = './html/'+params.decode('utf-8')+'_SentencesPage.html'
    desc_savepath = './html/'+params.decode('utf-8')+'_description.html'
    author_savepath = './html/' + params.decode('utf-8') + '_author_description.html'
    all_sentence_savepath = './html/'+params.decode('utf-8')+'_AllSentencesPage.html'

    # 请求 句子集页面
    requestUrlbyGet(url,sentspath)
    # 读取html，保存 句子集信息
    desc_url = readhtml_SentenceResult(sentspath)

    # 请求 作品简介页面
    requestUrlbyGet(desc_url, desc_savepath)
    # 读取html，保存 作品简介信息
    desc_data = readhtml_Description(desc_savepath)

    # 从作品信息中获取作者简介url
    author_url = desc_data['author_url']
    # 请求 作者简介页面
    requestUrlbyGet(author_url, author_savepath)
    # 读取html，保存 作者简介信息
    readhtml_Author_Description(author_savepath)

    # 从作品信息中获取全部句子页面的url
    all_sentence_url = desc_data['all_sentence_url']
    sentence_num = int(desc_data['sentence_num'])
    sent_requestUrlbyGet(all_sentence_url,all_sentence_savepath,sentence_num)
    readhtml_All_SentenceResult(sentspath, sentence_num)

