import httplib2
import json
import requests
from optparse import OptionParser
import re

class PageClass:
    def get_page(self,url,headers):
        http=httplib2.Http()
        response,content=http.request(url,'GET',headers=headers)
        return content.decode('unicode-escape','ignore').encode('utf-8')

def Get_Token(content):
    flag = r'<input id="csrf_token" name="csrf_token" type="hidden" value="(.*?)">'
    flag_re = re.compile(flag)
    result = flag_re.search(content)
    return result.group(1)

def Get_Header(content):
    flag = r'(.*?);'
    flag_re = re.compile(flag)
    result = flag_re.search(content)
    return result.group(1)

def Get_Auto_Get_Session():
    url = 'https://themis.tongdun.cn:8443/login/'
    r = requests.get(url)
    header = Get_Header(r.headers['Set-Cookie'])
    LoginHeader = {'Cookie': header,'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    token = Get_Token(r.text)
    payload = {'csrf_token':token,'name':'123',
            'password':'123'}

    LoginResult = requests.post(url,data=payload,headers=LoginHeader)
    return LoginResult.headers['Set-Cookie']

def GetIp(url):
    page = PageClass()
    content = page.get_page(url,HEADERS)
    cjson = json.loads(content)
    for i in range(0,len(cjson['data'])):
        print cjson['data'][i]['lan_ip']

def GetOsUrl(url):
    hFile = open("OS_IP.txt","w")
    page = PageClass()
    print url
    content = page.get_page(url,HEADERS)
    cjson = json.loads(content)
    for i in range(0,len(cjson['data'])):
        name = cjson['data'][i]['name']
        hFile.write("############"+name+"##############\n")
        name = str(name).replace(" ","%20")
        url = 'https://themis.tongdun.cn:8443/api/software/os?name='+name
        page2 = PageClass()
        content2 = page.get_page(url,HEADERS)
        cjson2 = json.loads(content2)
        for i in range(0,len(cjson2['data'])):
            hFile.write(cjson2['data'][i]['lan_ip']+'\n')
    hFile.close()

def GetMwUrl(url):
    hFile = open("MW_IP.txt","w")
    page = PageClass()
    print url
    content = page.get_page(url,HEADERS)
    cjson = json.loads(content)
    for i in range(0,len(cjson['data'])):
        name = cjson['data'][i]['name']
        version = cjson['data'][i]['version']
        hFile.write("############"+name+": "+version+"##############\n")
        for ii in range(0,len(cjson['data'][i]['hosts'])):
            hFile.write(cjson['data'][i]['hosts'][ii]['lan_ip']+'\n')
    hFile.close()

def GetDomainIP(url):
    value = []
    hFile = open("Domain_IP.txt","w")
    page = PageClass()
    print url
    content = page.get_page(url,HEADERS)
    cjson = json.loads(content)
    for i in range(0,len(cjson['data'])):
        value.append(cjson['data'][i]['value'])
    value = list(set(value))
    for i in range(0, len(value)):
        hFile.write(value[i]+'\n')
    hFile.close()

def main():
    global HEADERS
    session = Get_Auto_Get_Session()
    HEADERS={"Cookie": session}

    url_os = 'https://themis.tongdun.cn:8443/api/software/os'
    #GetOsUrl(url_os)
    #url_db = 'https://themis.tongdun.cn:8443/api/software/database'
    #GetDbUrl('database',url_db)
    url_mw = 'https://themis.tongdun.cn:8443/api/software/middleware'
    #GetMwUrl(url_mw)
    url_domain_out = 'https://themis.tongdun.cn:8443/api/dns/?domainType=out&query_name='
    GetDomainIP(url_domain_out)


if __name__ == "__main__":

    main()
