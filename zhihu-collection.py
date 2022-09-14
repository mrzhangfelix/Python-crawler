import datetime
import time
import requests
import re
collections=str(input("请输入收藏夹编码:\n"))
start=str(input("请输入爬取开始篇数:\n"))
end=str(input("请输入爬取结束篇数:\n"))
name_=str(input("请输入保存名字：\n"))
p=20
now_time = int(time.time())
timeArray = time.localtime(now_time)
otherStyleTime = str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))
with open("爬取日志.txt","a+",encoding="utf-8") as c:
    c.write("\n\n在  "+str(otherStyleTime)+"  从ID：  "+str(collections)+"  的收藏夹中爬取了从  "+str(start)+"  到  "+str(end)+"  页的数据\n\n")
for x in range(int(start),int(end),int(p)+1):
    url=f"https://www.zhihu.com/api/v4/collections/{collections}/items?offset={str(int(x)-1)}&limit=20"
    headers={
        "refer":f"https://www.zhihu.com/collection/{collections}",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    s=requests.session()
    res=s.get(url=url,headers=headers).text
    # res_1=re.findall('"content":".*?","title":"","excerpt"',res,re.S)
    res = re.sub(r'\\u003c', "<", res)
    res = re.sub(r'\\u003e', ">", res)
    res = re.sub(r'\\n', "<br/>", res)
    res = re.sub(r'\\u0026', "&", res)  # 乱码替换
    # print(res)
    res_1=re.findall('"id":[0-9]+,"title":".*?","title":"","excerpt"',res,re.S)  #内容分割
    for res_2 in res_1:
        print("==============================这是第" + str(x) + "篇===============================")
        res_3 = re.findall('"title":".*?"', res_2, re.S)[0]   #标题截取
        otherStyleTime_2 = str(time.strftime("%Y年%m月%d日 %H时%M分%S秒", timeArray))
        with open(f"{name_}+{collections}+{otherStyleTime_2}.html","ab+") as f:
            y="<h1>"+"========这是第" + str(x) + "篇=======" + "</h1>"  #分割线赋值
            f.write(y.encode())  #分割线编码写入
            f.write(res_3.encode())  #标题编码写入
            print(res_3)     #标题打印
        res_4 = re.findall('"content":".*?","title":"","excerpt"', res_2, re.S)[0]   #切出主要内容
        res_5 = re.sub(r'"content":"', '<br/>"content":"', res_4)  #内容前空行
        res_5 = re.sub(r'","title":"","excerpt"', "", res_5)  #不必要的符号替换
        res_5 = re.sub(r'src=\\', "src=", res_5) #修改图片储存地址，方便图片显示
        with open(f"{name_}+{collections}+{otherStyleTime_2}.html","ab+") as f:
            f.write(res_5.encode())  #主要内容写入
        x=x+1
        # s='<br/>'+"="*20+"<br/>"+"<br/>"
        # f.write(s.encode())
        # print(res_5)
        # print("<br/>"+"="*50+"<br/>")
num_=x-1
print(f"恭喜你成功爬取了{num_}篇内容，爬取文件与python程序在同一个目录")