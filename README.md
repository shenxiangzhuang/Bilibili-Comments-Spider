# Bilibili-Comments-Spider
自动爬取B站某个视频及番剧所有剧集的评论.
(改自[Bilibili-Lottery](https://github.com/LSM2016/Bilibili-Lottery))

暂时没有使用多线程或者多进程，测试时候大概10分钟可以抓取50000条数据。

## [改进后]使用方法

#### Step1:
在dbhelper.py内修改你的MySQL相关参数
```
host = "localhost"
user = "username"
passwd = "********"
database = "databaseName"
comment_tablename = "Comments"
```
>注意，我这里用MySQL8连接会报错，参考[stackoverflow](https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported)，设置一个登录选项解决。

>此外，用mysql-connector时使用utf8mb4时会出现一堆错误...直接换pymysql了Orz

>设置自动建表，注意如果已存在要修改下表名；然后插入程序是用的`executemany`，不然太慢了...

#### Step2:

获取单个视频评论
>python get_comments.py -type video -url https://www.bilibili.com/video/av68680509\?spm_id_from\=333.851.b_7265706f7274466972737432.4

获取番剧所有剧集的评论
>python get_comments.py -type play -url https://www.bilibili.com/bangumi/play/ep277026\?spm_id_from\=333.851.b_62696c695f7265706f72745f616e696d65.51



## [拓展]番剧评论的抓取思路
使用python3 get_comments.py来获得B站评论，视频ID在文件内修改。
注意，对于上传的视频来说，一般URL格式为`https://www.bilibili.com/video/avxxxxxxxx`,
后面的视频ID`xxxxxxxx`也就是评论API中的`oid`。

但是，对于番剧来说是其URL结尾格式并不是`avxxxxxxxx`，所以`oid`需要我们手动获取。
在每一部番的首页，如`https://www.bilibili.com/bangumi/play/ep277026`, 我们直接请求该地址，并直接用正则`re.findall(r'"aid":(\d{8}),', s)`获取所有的`oid`即可。



## 更新进程

[Rebuilding](https://github.com/shenxiangzhuang/Bilibili-Lottery/projects/1)
