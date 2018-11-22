
import time
import random
import re

import pymysql
import requests
from lxml import etree

url_list = []


def index(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    }
    time.sleep(random.random())
    try:
        response = requests.get(url=url, headers=headers)
    except:
        return index(url)

    if response.status_code == 200:
        return response.content.decode('utf-8')
    return


def url_xpath(html):
    etree_html = etree.HTML(html)

    url_a = etree_html.xpath('/html/body/div[3]/div/div/div[2]/a/@href')
    url_name = etree_html.xpath('/html/body/div[3]/div/div/div[2]/a/text()')
    sexual = []
    for sexual_isolated in url_name:
        sexual.append(re.match(r"(.+)姓名字大全", sexual_isolated).group(1))

    url = ['http:' + i for i in url_a]

    url_list = []
    for url_isolated in url:
        for i in range(10):
            url_list.append(url_isolated[:-5] + '_' + str(i + 1) + url_isolated[-5:])

    url_dict = {'url': [], 'sexual': []}

    for i in range(len(sexual)):
        url_dict['sexual'].append(sexual[i])

    for i in range(len(url_list)):
        url_dict['url'].append(url_list[i])

    return url_dict


def url2_xpath(html):
    etree_html = etree.HTML(html)

    name = etree_html.xpath('//*[@id="head_"]/div/div/div[1]/a/@href')[0]
    url_a = etree_html.xpath('/html/body/div[3]/div[2]/div[1]/div/a/@href')

    url = [name + i for i in url_a]

    return url


sexual_dict = {}
count1 = 1


def add_data(sexual):
    global sexual_dict
    global count1
    con = pymysql.connect(host='localhost',
                          port=3306,
                          db='resgain',
                          user='root',
                          passwd='123456',
                          charset='utf8')
    try:
        with con.cursor() as cursor:
            result = cursor.execute('insert into sexual(sexual) values ("%s")' % (sexual))
            if result == 1:
                sexual_dict[sexual] = count1
                count1 += 1
                print('数据库添加成功')
            con.commit()
    except pymysql.MySQLError as e:
        print('错误信息%s' % e)
        con.rollback()


count2 = 1


def add_data2(i, cursor, con):
    global count2
    try:
        result = cursor.execute('insert into complete_information(`name`, man, girl, details, five_lines, three_talents, five_cases_tian, five_cases_ren, five_cases_di, five_cases_zong, five_cases_wai, five_grid_analysis_tian, five_grid_analysis_ren, five_grid_analysis_di, five_grid_analysis_wai, five_grid_analysis_zong, verse, sexual_id) ' \
                                'values ("%s", "%s", "%s", "%s", "%s", "%s", %s, %s, %s, %s, %s, "%s", "%s", "%s", "%s", "%s", "%s", %s)' % (i['name'], i['man'], i['girl'], i['details'], i['five_lines'], i['three_talents'], i['five_cases'][0], i['five_cases'][1], i['five_cases'][2], i['five_cases'][3], i['five_cases'][4], i['five_grid_analysis'][0], i['five_grid_analysis'][1], i['five_grid_analysis'][2], i['five_grid_analysis'][3], i['five_grid_analysis'][4], i['verse'], sexual_dict[i['sexual']]))
        if result == 1:
            print('数据库添加%d成功' % (count2))
            count2 += 1
        con.commit()
    except pymysql.MySQLError as e:
        print('错误信息%s' % e)
    cursor.close()


def url3_xpath(html):
    etree_html = etree.HTML(html)
    try:
        title = etree_html.xpath('/html/body/div[2]/div/div[4]/div[2]/div[1]/div[1]/h3/text()')[0][5:]
        man = etree_html.xpath('/html/body/div[2]/div/div[2]/div/div/div[1]/@style')[0]
        man = re.match(r"width: (.+);", man).group(1)
        girl = etree_html.xpath('/html/body/div[2]/div/div[2]/div/div/div[2]/@style')[0]
        girl = re.match(r"width: (.+);", girl).group(1)

        sexual = etree_html.xpath('//*[@id="head_"]/div/div/div[1]/a/div[1]/text()')[0]
        sexual = re.match(r"(.+)姓之家", sexual).group(1)
        details = etree_html.xpath('/html/body/div[2]/div/div[4]/div[1]/div[1]/div[2]/strong/text()')[0]
        five_lines = etree_html.xpath('/html/body/div[2]/div/div[4]/div[2]/div[1]/div[2]/div[1]/blockquote/text()')[0].split()[0]
        three_talents = etree_html.xpath('/html/body/div[2]/div/div[4]/div[2]/div[1]/div[2]/div[2]/blockquote/text()')[0].split()[0]
        five_cases = etree_html.xpath('/html/body/div[2]/div/div[4]/div[2]/div[1]/div[2]/div[3]/blockquote/text()')
        five_cases_list = []
        for i in five_cases:
            a = i.split()
            if a:
                five_cases_list.append(a[0][1:])
        five_grid_analysis = etree_html.xpath('/html/body/div[2]/div/div[4]/div[2]/div[1]/div[2]/div[4]/blockquote/div/text()')
        five_grid_analysis_list = []
        for i in five_grid_analysis:
            five_grid_analysis_list.append(i[1:])
        verse = etree_html.xpath('/html/body/div[2]/div/div[4]/div[1]/div[3]/h4/text()')
        verse_str = ''
        for i in verse:
            if verse_str:
                verse_str += '\n' + i
            else:
                verse_str += i

        _dict = {}
        _dict['name'] = title
        _dict['man'] = man
        _dict['girl'] = girl
        _dict['details'] = details
        _dict['five_lines'] = five_lines
        _dict['three_talents'] = three_talents
        _dict['five_cases'] = five_cases_list
        _dict['five_grid_analysis'] = five_grid_analysis_list
        _dict['verse'] = verse_str
        _dict['sexual'] = sexual
        return _dict
    except:
        return {}


def main():
    url = 'http://www.resgain.net/xmdq.html'
    url_dict = url_xpath(index(url))
    
    for sexual in url_dict['sexual']:
        add_data(sexual)

    con = pymysql.connect(host='localhost',
                          port=3306,
                          db='resgain',
                          user='root',
                          passwd='123456',
                          charset='utf8')

    for url in url_dict['url']:
        url_list = url2_xpath(index(url))

        for url in url_list:
            dict1 = url3_xpath(index(url))
            if dict1:
                add_data2(dict1, con.cursor(), con)
    con.close()


if __name__ == '__main__':
    main()
