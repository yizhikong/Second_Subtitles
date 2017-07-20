# -*- coding: utf-8 -*-
import urllib2
import os
import re

symbol = ['、。，“”？']
pats = {'colon':re.compile('(.*?)：(.*)'), '':re.compile('')}

def getContent(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
    html = urllib2.urlopen(request).read()
    return html

def extract(text):
    liPattern = re.compile('<li>(.*?)</li>')
    lis = liPattern.findall(text)
    lis = map(lambda li:re.sub('<.*?>', '', li), lis)
    liResults = map(lambda li:pats['colon'].findall(li), lis)
    liResults = filter(lambda result:len(result)!=0, liResults)
    results = []
    for result in liResults:
        for item in result:
        	results.append((item[0].strip(), item[1].strip()))
    return results

if __name__ == '__main__':
    url = 'https://zh.moegirl.org/index.php?title=RWBY'
    html = getContent(url)
    #html = ''.join(open('html.txt', 'r').readlines()) # develop only
    results = extract(html)
    with open('document.txt', 'w') as f:
        for item in results:
            f.write(item[0].replace('\t', ' '))
            f.write('\t')
            f.write(item[1].replace('\t', ' '))
            f.write('\n')