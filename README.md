# Bilibili-Comments-Spider
自动爬取B站某个视频的评论.
(改自[Bilibili-Lottery](https://github.com/LSM2016/Bilibili-Lottery))

## 使用方法
（暂时，后面会集成进去）
### Step1:
本地数据新建符合要求的`TABLE`.


### Step2:
再dbhelper.py内修改你的MySQL相关参数
```
host = "localhost"
user = "username"
passwd = "********"
database = "databaseName"
```

使用python3 get_comments.py来获得B站评论，视频ID在文件内修改。
注意，对于上传的视频来说，一般URL格式为`https://www.bilibili.com/video/avxxxxxxxx`,
后面的视频ID`xxxxxxxx`也就是评论API中的`oid`。

但是，对于番剧来说是其URL结尾格式并不是`avxxxxxxxx`，所以`oid`需要我们手动获取。
在每一部番的首页，如`https://www.bilibili.com/bangumi/play/ep277026`, 我们直接请求该地址，并直接用正则`re.findall(r'"aid":(\d{8}),', s)`获取所有的`oid`即可。
（暂时，后面会集成进去。）

## 更新进程

[Rebuilding](https://github.com/shenxiangzhuang/Bilibili-Lottery/projects/1)
