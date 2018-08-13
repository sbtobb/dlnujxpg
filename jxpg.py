import requests,os,sys,random
from bs4 import BeautifulSoup

# Code by CyouGuang
# date 2018-7-6

session = requests.session()
headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
path = os.path.split( os.path.realpath(sys.argv[0]))[0]

def evaluation(data):
    subDatas = data.split("#@")
    payloadData = {"wjbm":subDatas[0],"bpr":subDatas[1],"bprm":subDatas[2],"wjmc":subDatas[3],
               "pgnrm":subDatas[4],"pgnr":subDatas[5],"oper":"wjShow","pageSize":"20",
               "page":"1","currentPage":"1","pageNo":""}
    response = session.post("http://zhjw.dlnu.edu.cn/jxpgXsAction.do",data=payloadData,headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    payloadData = {"wjbm":subDatas[0],"bpr":subDatas[1],"pgnr":subDatas[5]}
    for inputTag in soup.find_all("input",type="radio"):
        if inputTag['value'].find("_1") != -1:
            payloadData[inputTag['name']]=inputTag['value']
    with open(path+'/saysomething.txt','r',encoding="utf-8") as something:
        zgpjs = something.readlines()
        randomNum = random.randint(0,len(zgpjs))
        payloadData["zgpj"]=zgpjs[randomNum-1].encode('gb2312')
    print(payloadData)
    if len(payloadData) > 4:
        response = session.post("http://zhjw.dlnu.edu.cn/jxpgXsAction.do?oper=wjpg",data=payloadData,headers=headers)
        response.encoding = response.apparent_encoding
        if response.text.find("评估成功") != -1:
            print(subDatas[4]+"：评估完成")
    else:
        print(subDatas[4]+"：读取试卷列表失败！")

def getEvaluationList():
    response = session.get("http://zhjw.dlnu.edu.cn/jxpgXsAction.do?oper=listWj", headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    evaluationList = []
    print("你未完成评估的有:")
    for trTag in soup.find_all(name="tr",class_="odd"):
        tdTags = trTag.find_all(name="td")
        if len(tdTags) < 5:
            print("无法正确获取待评估列表")
            return evaluationList
        if tdTags[3].string == "否":
            evaluationList.append(tdTags[4].img['name'])
            print(tdTags[2].string)

    return evaluationList




def login(username, password):
    response = session.get("http://zhjw.dlnu.edu.cn/", headers=headers)
    if response.status_code != 200:
        print("访问  http://zhjw.dlnu.edu.cn/  失败")
        return False
    response = session.get(
        "http://authserver.dlnu.edu.cn/authserver/login?service=http%3A%2F%2Fzhjw.dlnu.edu.cn%2Flogin.jsp",
        headers=headers)
    if response.status_code != 200:
        print("访问  http://authserver.dlnu.edu.cn/  失败")
        return False
    response.encoding = response.apparent_encoding

    data = {"username": username, "password": password}
    # 煲汤
    soup = BeautifulSoup(response.text, "html.parser")

    for inputTag in soup.find_all(name="input", type="hidden"):
        data[inputTag['name']] = inputTag['value']

    response = session.post(
        url="http://authserver.dlnu.edu.cn/authserver/login?service=http%3A%2F%2Fzhjw.dlnu.edu.cn%2Flogin.jsp",
        data=data, headers=headers)
    response.encoding = response.apparent_encoding
    if response.text.find("密码有误") == -1:
        return True
    else:
        return False


def startValuate():
    isValuate = True
    islogin = False
    while isValuate:
        #开始登陆流程
        username = input("请输入学号:")
        password = input("请输入密码:")
        if login(username=username, password=password):
            print("登录成功，本项目已在GitHub开源，欢迎star或fork")
            islogin = True
        else:
            print("登录失败,请检查是否在学校内网，有问题在Github发issue")
            islogin = False
        
        if islogin:
        #登陆成功，准备评价
            commandHelp = ("---------------------------------------------\n"
                        '1.一键完成全部(默认非常满意) r.重新登录 q.退出程序\n'
                        '----------------------------------------------')
            print(commandHelp)
            command = input("请输入需要执行的命令(输入序号即可):")
            if command.lower() == 'q':
                isValuate = False
            elif command.lower() == 'r':
                continue
            elif command == "1":
                for evalData in getEvaluationList():
                    evaluation(evalData)
                print("已经完成所有教学评估，感谢使用快速教学评估小工具")
                isValuate = False
        else:
        #未登录
            command = input("请输入功能序号(r.重新登陆 q.退出程序):")
            if command.lower() == 'r':
                continue
            elif command.lower() == 'q':
                isValuate = False

def editSamesomething():
    with open(path+"/saysomething.txt", 'r',encoding="utf-8") as f:
        commentsList = f.read().split('\n')
    isEdit = True
    while isEdit:
        #打印当前评论
        print("---------------------------------------------")
        print("当前评论：")
        for commentIndex in range( len(commentsList) ):
            print("{}.{}".format(commentIndex, commentsList[commentIndex]))
        print("---------------------------------------------")
        #开始修改
        print("1.增 2.删 3.改 4.保存退出 5.退出")
        userSelect = input("输入功能对应序号：")
        if userSelect == '1':
            itemStr = input("请输入要增加的评论(回车结束)：\n")
            if input("确定要增加条目 “{}” 到评论吗？(y/n)".format(itemStr)).lower() == 'y':
                commentsList.append(itemStr)
            else:
                print("您放弃了修改")
        elif userSelect == '2':
            try:
                selectIndex = int(input("请输入要删除评论的序号："))
                if input("确定要删除条目 “{}” 吗？(y/n)".format(commentsList[selectIndex])).lower() == 'y':
                    del commentsList[selectIndex]
                else:
                    print("您放弃了删除")
            except IndexError:
                print("输入的序号不在有效范围内！")
            except ValueError:
                print("你输入了错误的序号！")
            except:
                raise
        elif userSelect == '3':
            try:
                selectIndex = int(input("请输入要修改评论的序号："))
                commentStrToReplace = input("要将评论修改为(回车结束)：")
                if input( "原条目 “{}” \n新条目 “{}”\n确定要修改吗？(y/n)".format( commentsList[selectIndex], commentStrToReplace ) ).lower() == 'y':
                    commentsList[selectIndex] = commentStrToReplace
                else:
                    print("您放弃了修改")
            except IndexError:
                print("输入的序号不在有效范围内！")
            except ValueError:
                print("你输入了错误的序号！")
            except:
                raise
        elif userSelect == '4':
            try:
                f = open(path+"/saysomething.txt", 'w',encoding="utf-8")
                f.write( '\n'.join( commentsList ) )
                print("操作成功结束！")
            except:
                print("在打开并写入的过程中绝逼出了些问题，有问题在Github发issue")
                raise
            finally:
                f.close()
                isEdit = False
        elif userSelect == '5':
            isEdit = False
        else:
            print("输入的序号无法判断，请重试~")

def mainMenu():
    print("当前工作目录:", path)
    with open(path+'/banner.txt', 'r',encoding="utf-8") as f:
        print(f.read())
    menuText = ("--------------------主菜单-------------------\n"
                "1.开始评价\n"
                "2.修改评语\n"
                "q.退出程序\n"
                "---------------------------------------------\n")
    while True:
        userSlect = input(menuText + "请选择菜单序号：")
        if userSlect == '1':
            startValuate()
            break
        elif userSlect == '2':
            editSamesomething()
        elif userSlect.lower() == 'q':
            quit()
        else:
            print("输入出错~ 请检查!")
    

if __name__ == '__main__':
    mainMenu()
