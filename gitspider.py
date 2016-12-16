import httplib2
from optparse import OptionParser
import urllib2
import re


class PageClass:
    def get_page(self,url,headers):
        http=httplib2.Http()
        response,content=http.request(url,'GET',headers=headers)
        return content.decode('unicode-escape','ignore').encode('utf-8')   #ignore error decode


def GET_PAGE_DETAIL(url):
    Real_Url = "https://github.com" + url
    #print "Now, Searching: " + Real_Url +"\n"
    Detail_Info = PageClass()
    Detail_Info_Content = Detail_Info.get_page(Real_Url,HEADERS)
    if ACC_KEY_WORD in Detail_Info_Content:
        Key_Word_Number = Detail_Info_Content.count(ACC_KEY_WORD)
        Info_Content_Block = Detail_Info_Content.split(ACC_KEY_WORD)

        if Key_Word_Number == 1:
            if len(Info_Content_Block[0]) > 10 and len(Info_Content_Block[1])>10:
                try:
                    print "KEY WORD CONTEXT: " +Info_Content_Block[0][-100:] + ACC_KEY_WORD + Info_Content_Block[1][:100]
                    ACC_KEY_WORD_URL_LIST.append(Real_Url)
                    print "THESE URL CONTAINS THE KEY WORD: "+ Real_Url
                    print "#################################################################"
                    return
                except:
                    try:
                        print "KEY WORD CONTEXT: " +Info_Content_Block[0][-50:] + ACC_KEY_WORD + Info_Content_Block[1][:50]
                        ACC_KEY_WORD_URL_LIST.append(Real_Url)
                        print "THESE URL CONTAINS THE KEY WORD: "+ Real_Url
                        print "#################################################################"
                        return
                    except:
                        print "Detail_Info length Error,you should see the detail by Browser\n"
                        return
            else:
                print "Detail length Error,you should see the detail by Browser\n"
                return

        for i in range(0,int(Key_Word_Number)):     #block = number+1
            if len(Info_Content_Block[i]) > 10 and len(Info_Content_Block[i+1])>10:
                try:
                    print "KEY WORD CONTEXT: " +Info_Content_Block[i][-100:] + ACC_KEY_WORD + Info_Content_Block[i+1][:100]
                except:
                    try:
                        print "KEY WORD CONTEXT: " +Info_Content_Block[i][-50:] + ACC_KEY_WORD + Info_Content_Block[i+1][:50]
                    except:
                         print "Detail_Info length Error,you should see the detail by Browser\n"
            else:
                print "Detail length Error,you should see the detail by Browser\n"

        ACC_KEY_WORD_URL_LIST.append(Real_Url)
        print "THESE URL CONTAINS THE KEY WORD: "+ Real_Url
        print "#################################################################"



def GET_MAX_PAGE_NUMBER(arrlen, url_regx):
    reg= r'/search\?p=(\d+)&.*'
    reg_re=re.compile(reg)
    try:
        reg_rex=reg_re.search(url_regx[arrlen-1])
        reg_rex2=reg_re.search(url_regx[arrlen-2])

        if int(reg_rex2.group(1)) >= int(reg_rex.group(1)):
            print "A total of "+ str(reg_rex2.group(1)) + " Pages\n"
            return reg_rex2.group(1)
    except:
        print "A total of 1 Pages\n"
        return 1


def GET_EVERY_PAGE_URL(number,headers):
    for i in range(1,int(number)+1):
        Clear_URL_List=[]
        Page_Url ='https://github.com/search?p='+str(i)+'&q='+Search_Key_Word+'&ref=simplesearch&type=Code&utf8=%E2%9C%93'
        print "############### NOW, SEARCHING "+ str(i) + " PAGE ###################\n"
        page_n = PageClass()
        content_n = page_n.get_page(Page_Url,headers)
        c_n = str(content_n)
        c_n = c_n.replace('\n','')

        url_flag = r'<a href="(/.*?)">'
        url_re=re.compile(url_flag)
        url_regx=url_re.findall(c_n)
        arrlen = len(url_regx)

        str_flag = r'.*/blob/.*'
        str_flag2 = r'.*(#.*)'
        str_re=re.compile(str_flag)
        str_re2=re.compile(str_flag2)
        for i in range(0,arrlen-1):
            try:
                str_regx=str_re.search(url_regx[i])  #include /blob/ keyword
                try:
                    Clear_URL=str_re2.search(str_regx.group(0))
                    Clear_URL = Clear_URL.group(0).replace(Clear_URL.group(1),"")  #delete '#1L' get real url
                    Clear_URL_List.append(Clear_URL)

                except:
                    pass

            except:
                pass
        Clear_URL_List=list(set(Clear_URL_List))
        for url in Clear_URL_List:
            GET_PAGE_DETAIL(url)


def GET_PAGE_INFO(content,headers):
    url_flag = r'<a.*?href="(/.*?)">'
    url_re=re.compile(url_flag)
    url_regx=url_re.findall(content)
    arrlen = len(url_regx)

    Max_Page_Number = GET_MAX_PAGE_NUMBER(arrlen, url_regx)
    GET_EVERY_PAGE_URL(Max_Page_Number,headers)


def main():
    global Search_Key_Word
    global ACC_KEY_WORD
    global HEADERS
    global ACC_KEY_WORD_URL_LIST

    HEADERS={"Cookie":'user_session=5dvLN1DbBbVIUjkLC5iwuKFfV_qoO0wTCOHGHKfdk4bgRePF'}
    Search_Key_Word = "api.fraudmetrix"
    ACC_KEY_WORD='secret_key'
    ACC_KEY_WORD_URL_LIST=[]

    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage)
    parser.add_option("-K","--KEY",dest="KEY",help="SET YOUR SEARCH KEY")
    parser.add_option("-k","--key",dest="key",help="SET YOUR ACCURATE KEY")
    (options, args) = parser.parse_args()
    KEY = options.KEY
    key = options.key
    if KEY == None and key == None:
        print parser.print_help()
    if KEY:
        Search_Key_Word = KEY
    if key:
        ACC_KEY_WORD = key

    url = 'https://github.com/search?q='+Search_Key_Word+'&ref=simplesearch&type=Code&utf8=%E2%9C%93'
    page = PageClass()
    print url
    content = page.get_page(url,HEADERS)
    c = str(content)
    c = c.replace('\n','')
    GET_PAGE_INFO(c,HEADERS)
    print "############## THESE URL CONTAINS "+ ACC_KEY_WORD +" ###############\n"
    print ACC_KEY_WORD_URL_LIST


if __name__ == "__main__":

    main()
