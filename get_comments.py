import re
import requests
import json
import time
import math
import dbhelper
import argparse
from comment import Comment


def fetch_url(url):
    headers = {
        'accept': """text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8""",
        'user-agent': """Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36""",
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        print(r.url)
        return r.text
    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")


def parse_html(html):
    s = json.loads(html)

    reply_list = []
    reply_list = s['data']['replies']
    return reply_list


def form_url(oid, page):
    base_url = 'https://api.bilibili.com/x/v2/reply?type=1&'
    return base_url + 'oid=' + str(oid) + '&pn=' + str(page)


def get_pages(oid):
    base_url = 'https://api.bilibili.com/x/v2/reply?type=1&oid='
    html = fetch_url(base_url + str(oid))
    assert html is not None, 'Html is None.'
    data = json.loads(html)['data']
    pages = math.ceil(data['page']['count'] / data['page']['size'])
    return pages


def check_exist_comment(comm, comms):
    existed = False
    for item in comms:
        if item.rpid == comm.rpid:
            existed = True
    return existed


# 抓取一个视频，或一个番剧其中一集中所有的评论
def get_av_comments(oid):
    url = f'https://api.bilibili.com/x/v2/reply?type=1&oid={oid}'
    fetch_url(url)
    pages = get_pages(oid)
    replies = []
    # print(pages)
    for i in range(pages):
        replies_cur_page = parse_html(fetch_url(form_url(oid=oid, page=i)))
        for reply in replies_cur_page:
            replies.append(reply)

    comments = []
    for reply in replies:
        # mid, username, gender, ctime, content, likes, rcounts, rpid
        comment = Comment(mid=reply['mid'],
                          username=reply['member']['uname'],
                          gender=reply['member']['sex'],
                          ctime=reply['ctime'],
                          content=reply['content']['message'],
                          likes=reply['like'],
                          rcount=reply['rcount'],
                          rpid=reply['rpid'])
        comments.append(comment.values())
        if reply['rcount'] > 0:
            for item in reply['replies']:
                comment = Comment(mid=item['mid'],
                                  username=item['member']['uname'],
                                  gender=item['member']['sex'],
                                  ctime=item['ctime'],
                                  content=item['content']['message'],
                                  likes=item['like'],
                                  rcount=item['rcount'],
                                  rpid=item['rpid'])
                comments.append(comment.values())
    dbhelper.insert_comment(c, conn, comments)


# 根据番剧第一集的url获取所有集的oid
def get_paly_oids(play_url):
    html = fetch_url(play_url)
    oids = re.findall(r'"aid":(\d{8}),', html)
    return list(set([int(oid) for oid in oids]))


# 获取番剧的所有评论
def get_play_comments(play_url):
    oids = get_paly_oids(play_url)
    for oid in oids:
        get_av_comments(oid)


if __name__ == '__main__':
    conn, c = dbhelper.connect_db()
    # 创建数据表
    dbhelper.create_table(c)
    parser = argparse.ArgumentParser()
    parser.add_argument("-type", type=str, help="视频(-video), 番剧(-play)")
    parser.add_argument("-url", type=str, help="the exponent")
    args = parser.parse_args()
    url = args.url
    if args.type == 'video':
        oid = re.findall(r'www.bilibili.com/video/av(\d{8}).*', url)[0]
        get_av_comments(int(oid))
    elif args.type == 'play':
        get_play_comments(url)

    # to csv
    dbhelper.data_table_to_csv(c, conn)
    conn.close()
