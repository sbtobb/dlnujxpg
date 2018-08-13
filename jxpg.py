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


def main():
    isValuate = True
    islogin = False
    print(path)
    with open(path+'/banner.txt', 'r',encoding="utf-8") as f:
        print(f.read())
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


if __name__ == '__main__':
    main()
