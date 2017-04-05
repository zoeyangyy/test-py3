import requests
from bs4 import BeautifulSoup

r = requests.get('')
soup = BeautifulSoup(r.text)

table = soup.find(id="result_content").find_all('tr',limit=3)

del(table[0])
list1 = []

for row in table:
	dict1={}
	dict1['index']=row.find_all('td')[0].text
	dict1['bookname']=row.find_all('td')[1].a.text
	dict1['author']=row.find_all('td')[2].text
	dict1['publisher']=row.find_all('td')[3].text
	dict1['booknumber']=row.find_all('td')[4].text
	dict1['booktype']=row.find_all('td')[5].text

	link=row.find_all('td')[1].a
	subweb=requests.get('http://opaclibrary.sufe.edu.cn/opac/'+link['href'])
	soup1=BeautifulSoup(subweb.text)
	print(soup1.find(id="book_img"))

	detail=soup1.find(id="item_detail").find_all('dl')
	dict1['edition']=detail[1].dd.text
	dict1['ISBN']=detail[3].dd.text
	dict1['douban']=detail[17].dd.p.text
	dict1['available_number']=len(soup1.find_all(attrs={"color":"green"}))

	storelist=soup1.find(id="item").find_all('tr')
	del(storelist[0])
	list_info=[]

	for row_info in storelist:
		dict_info={}
		dict_info['booknumber']=row_info.find_all('td')[0].text
		dict_info['barcode']=row_info.find_all('td')[1].text
		dict_info['year']=row_info.find_all('td')[2].text
		dict_info['place']=row_info.find_all('td')[3].text
		list_info.append(dict_info)

	dict1['storeinformation']=list_info
	list1.append(dict1)
	j=json.dumps(list1)
	print(j)
