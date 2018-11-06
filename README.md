## get-latest-novel

#### 功能简介
该模块的功能主要是循环监控小说网站指定小说的更新，如果更新的话将更新的小说信息post到指定的url，另一个微信公众号后台程序会监听该指定url，将更新的小说信息通过微信发送给用户。

#### 流程图
下面是一个简单的流程图描述：

![image](https://img-1252787176.cos.ap-shanghai.myqcloud.com/get-latest-novel.jpg)

#### 配置文件
配置文件其实就是一个json文件，包含了小说名称和在小说网站的url。  
一个典型的模板：
```json
{
  "shengxu": {
    "chineseName": "圣墟",
    "bookUrl": "https://www.biqiuge.com/book/4772/"
  },
  "feijianwendao": {
    "chineseName": "飞剑问道",
    "bookUrl": "https://www.biqiuge.com/book/24277/"
  }
}
```

#### 最终提交的post信息
```json
{
  "bookName" : "圣墟",
  "latestChapter" : "第1291章 阳间风云激荡",
  "updateTime" : "2018-11-06 00:06:26",
  "latestUrl":"https://www.biqiuge.com/book/4772/26795186.html"
}
```
