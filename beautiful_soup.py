# encoding='utf-8'
# 修改: 1. 文件名 2. 网站 3. 病名

import time
import requests
import json
from bs4 import BeautifulSoup

file = open('./data/nephritis.txt', 'a')

for i in range(82, 201):
    r1 = requests.get('http://club.xywy.com/list_746_all_'+str(i)+'.htm')
    soup = BeautifulSoup(r1.text, "html.parser")

    for tr in soup.table.find_all("tr"):
        dic = {}
        dic['depart'] = '内科'
        dic['disease'] = '肾炎'
        a = tr.td.find_all("a")[1]
        dic['url'] = a['href']

        # 问答页面
        r2 = requests.get(a['href'], timeout=60)
        r2.encoding = 'gbk'
        soup2 = BeautifulSoup(r2.text, "html.parser")
        askcon = soup2.find("div", attrs={"class": "Userinfo"})
        if not askcon:
            continue
        userinfo = askcon.find_all("span")
        dic['patient'] = userinfo[0].text
        print(dic['patient'])
        dic['gender'] = userinfo[2].text.strip()
        dic['age'] = userinfo[4].text
        dic['time'] = userinfo[6].text
        dic['ques'] = soup2.find(attrs={"class": "User_quecol"}).text.strip()

        # 医生相关信息
        if soup2.find(attrs={"class": "Doc_dochf"}):
            doccon = soup2.find(attrs={'class': "docCon"})
            doc_a = doccon.find_all('div', recursive=False)[1].a
            dic['dt_name'] = doc_a.text
            dic['dt_url'] = doc_a['href']
            dic['answer'] = soup2.find(attrs={"class": "Doc_dochf"}).div.text
        else:
            dic['dt_name'] = ''
            dic['dt_url'] = ''
            dic['answer'] = ''

        j = json.dumps(dic, ensure_ascii=False)
        file.write(j+'\n')
    print(time.strftime('%H:%M:%S', time.localtime(time.time())) +"   page "+ str(i) + " is ready")

file.close()
