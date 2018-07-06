import requests
from bs4 import BeautifulSoup

# Code by CyouGuang
# date 2018-7-6
session = requests.session()
headers = {
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}


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
    if response.text.find("密码有误") == -1:
        return True
    else:
        return False


def main():
    isquit = False
    islogin = False
    while not isquit:
        while not islogin:
            username = input("请输入学号:")
            password = input("请输入密码:")
            if login(username=username, password=password):
                print("登录成功，本项目已在GitHub开源，欢迎star或fork")
                islogin = True
            else:
                print("登录失败,请检查是否在学校内网，有问题在Github发issue")

        command = input("请输入需要执行的命令(输入序号即可):")
        if command.lower() == "q":
            isquit = True


if __name__ == '__main__':
    main()
