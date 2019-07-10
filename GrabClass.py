#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author:universtar
#time：18/4/12


from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
import time
import re
#响应头信息
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
}
#目标url
url = 'http://sso.jwc.whut.edu.cn/Certification//login.do'

#获取原网页返回的html
def get_html(url,userName,password):
    #添加进入教务处的信息
    data = {
        'systemId':'',
        'xmlmsg':'',
        'userName':userName,
        'password':password,
        'type':'xs'
    }
    #将信息格式编码为html格式
    data = parse.urlencode(data).encode('utf-8')
    #提交请求
    req = request.Request(url=url,headers=headers,data=data)
    response = request.urlopen(req)
    #获取网页html代码
    html =  response.read()
    return html

#
def get_info(htmlresponse):
    #获得soup对象
    soup = BeautifulSoup(htmlresponse, 'html.parser', from_encoding='utf-8')
    #从soup对象中截取到所要的信息
    infos = soup.find_all('div',style="margin-top: 2px; font-size: 10px")
    #定义三个数组用来存放得到的信息
    classname = []
    position = []
    date = []
    #获取信息位置
    for item in infos:
        ele = re.findall('(>.+)',str(item),re.S)
        #获取信息位置
        first_start = 16
        first_end = first_start + ele[-1][16:].find('\r')
        second_start = first_end + 19
        second_end = second_start + 6
        third_start = second_end + 9
        third_end = third_start + 7
        #添加到数组中
        classname.append(ele[-1][first_start:first_end])
        position.append(ele[-1][second_start:second_end])
        date.append(ele[-1][third_start:third_end])
    #返回的参数位三个数组：课程名，地点，时间
    return classname,position,date

if __name__ == '__main__':
    #用户输入
    userName = input('请输入你的用户名：')
    password = input('请输入你的密码:')
    s_time = time.time()
    html = get_html(url,userName,password)
    classname,position,date = get_info(html)
    #开始打印信息
    print('您的课表为:\n')
    for i in range(len(classname)):
        print('课程：'+classname[i]+'\t\t地点:'+position[i]+'\t\t时间:'+date[i])
    e_time = time.time()
    print('用时:' + str(e_time-s_time))