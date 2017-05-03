import time
import requests
import json
from bs4 import BeautifulSoup

file = open('./data_date/2016-04.txt', 'a')
file_error = open('./data_date/error4.txt', 'a')

for date in range(1, 31):
    if date < 10:
        date = '0' + str(date)
    else:
        date = str(date)
    for i in range(1, 501):
        try:
            r1 = requests.get('http://club.xywy.com/keshi/2016-04-' + date + '/' + str(i) + '.html')
            r1.encoding = 'gbk'
            soup = BeautifulSoup(r1.text, "html.parser")
            table = soup.find("div", attrs={"class": "DiCeng"})

            for div in table.find_all("div", attrs={"class": "club_dic"}, recursive=False):
                try:
                    dic = {}
                    url = div.h4.em.a['href']

                    # 问答页面
                    r2 = requests.get(url, timeout=60)
                    r2.encoding = 'gbk'
                    soup2 = BeautifulSoup(r2.text, "html.parser")
                    disease = soup2.find("p", attrs={"class": "znblue"}).find_all("a")
                    if len(disease) == 4:
                        dic['depart'] = disease[2].text
                        dic['disease'] = disease[3].text
                    else:
                        dic['depart'] = ""
                        dic['disease'] = ""

                    askcon = soup2.find("div", attrs={"class": "Userinfo"})
                    userinfo = askcon.find_all("span")
                    dic['patient'] = userinfo[0].text
                    print(dic['patient'])
                    dic['gender'] = userinfo[2].text.strip()
                    dic['age'] = userinfo[4].text
                    dic['time'] = userinfo[6].text
                    dic['title'] = div.h4.em.a.text
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

                    file.write(json.dumps(dic, ensure_ascii=False)+'\n')

                except Exception as e:
                    print(e)
                    file_error.write(time.strftime('%H:%M:%S', time.localtime(time.time())) + " " + date + "  page " + str(i) + " " + str(e) + '\n')
                    continue

            print(time.strftime('%H:%M:%S', time.localtime(time.time())) + "   page " + str(i) + " is ready")

        except Exception as e:
            print(e)
            file_error.write(time.strftime('%H:%M:%S', time.localtime(time.time())) + " date " + date + "   page " + str(i) + " " + str(e) + '\n')
            continue

file_error.close()
file.close()
