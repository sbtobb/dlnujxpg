
# 大连民族大学快速教学评估小工具
## The tools of dlnu evaluate
---
### 如果你电脑中没有安装python，也不想安装python的话，这里提供了使用pyInstall打包好的windows版本  
> 还是建议安装一下python比较好  
> 时间充裕的话，还是手动评价一下比较好(吐槽一下，两分钟提交限制)  
> 请确认电脑连上学校内网  

[jxpg-windows(单击这里下载)](https://github.com/sbtobb/dlnujxpg/releases/download/0.2/jxpg-windows-0.2.zip)
## 请解压后再点击jxpg.exe运行！！
---
## 使用说明
### 功能说明
+ 快速完成教学评估,仅需要十几秒钟
+ 默认选择 非常满意
+ 程序仅完成对老师的评价，后面还有个对学校的评价自己做吧(那个没有提交时间限制)
### 使用步骤
1. 将程序下载下来   
[jxpg.py(单击这里下载)](https://github.com/sbtobb/dlnujxpg/archive/master.zip)  
2. saysomething.txt 中存放了主观评价，每行一条，将随机选取一条
> ⚠️注意:本文件使用utf-8编码,使用windows默认记事本打开可能会显示乱码,请使用支持utf-8编码的编辑器来打开此文件，请确保文件使用utf-8保存  
3. 
```  
python3  jxpg.py  
```

4. 根据命令行完成即可

---
## 更新日志

- 2019/1/10 修复登录模块，添加人性化提示
---
## 开发环境
+ OS: macOS Sierra 10.12.6
+ IDE: PyCharm 2018.1
+ Programming Language: python 3.6.1
+ third-party library:
> beautifulsoup4 (4.5.3)  
  requests (2.13.0)  

---
## 使用协议
+ 本工具具有时效性，即某一时刻教务系统更新了就无法使用
+ 使用本工具造成的后果，与作者无关
+ 当你下载此软件，代表你同意了本协议  
---
## License

Copyright 2018 CyouGuang

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.