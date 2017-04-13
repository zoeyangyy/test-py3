import time
import requests
import json
from bs4 import BeautifulSoup

file = open('./data_date/0403.txt', 'a')

for i in range(1, 662):
    r1 = requests.get('http://club.xywy.com/keshi/2017-04-03/' + str(i) + '.html')
    r1.encoding = 'gbk'
    soup = BeautifulSoup(r1.text, "html.parser")
    table = soup.find("div", attrs={"class": "DiCeng"})

    for div in table.find_all("div", attrs={"class": "club_dic"}, recursive=False):
        dic = {}
        dic['disease'] = div.h4.var.a.text
        dic['title'] = div.h4.em.a.text
        dic['ques'] = div.p.text
        file.write(json.dumps(dic, ensure_ascii=False)+'\n')

    print(time.strftime('%H:%M:%S', time.localtime(time.time())) +"   page "+ str(i) + " is ready")

file.close()
