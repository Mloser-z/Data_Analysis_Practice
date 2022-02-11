import re
from bs4 import BeautifulSoup
import json
import login


def get_user_name(sp):
    name = sp.find(class_="username")
    label = sp.find(class_="label")
    if name is not None:
        return name.string
    elif label is not None:
        return label.string
    else:
        return None


def get_time(sp):
    time = sp.find(class_="lastplay-t")
    return time.string


def get_video_title(sp):
    title = sp.find(class_="title")
    subtitle = sp.find(class_="subtitle")
    if subtitle.string is None:
        return title.string.replace("\n", "").replace(" ", "")
    else:
        return title.string.replace("\n", " ").replace(" ", "") + ':' + subtitle.string.replace("\n", " ").replace(" ", "")


def get_video_type(sp):
    video_type = sp.find(class_="name")
    label = sp.find(class_="label")
    if video_type is not None:
        return video_type.string
    elif label is not None:
        return label.string
    else:
        return None


def get_device_type(sp):
    wrap_i = sp.find(class_="time-wrap").i.get('class')
    device_type = wrap_i[2][5:]
    return device_type


def is_repeat(infor_dic, infor_ed_dic):
    if infor_dic.get("title") == infor_ed_dic.get("title") and infor_dic.get("up_name") == infor_ed_dic.get("up_name"):
        return True
    else:
        return False


if __name__ == "__main__":
    login.start()
    file_name = "history.html"
    soup = BeautifulSoup(open(file_name, encoding="utf-8"), "lxml")
    lis = soup.find_all(class_="history-record")
    infor_lists = []
    infor_ed_lists = []
    file_name = "history.json"
    
    # 读取文件，导出已储存信息，用来判断是否重复
    try:
        with open(file_name, "r", encoding="utf-8") as rp:
            infor_ed_lists = json.load(rp)
    except Exception:
        print("No File")

    with open(file_name, "w", encoding="utf-8") as fp:
        n = 0
        try:
            for li in lis:
                sp = BeautifulSoup(str(li), "lxml")
                infor = {"title": get_video_title(sp), "up_name": get_user_name(sp), "video_type": get_video_type(sp), "device": get_device_type(sp), "time": get_time(sp)}
                # 只爬取两天前的数据
                if re.match(re.compile(r'\d\d:\d\d'), infor.get("time")) is not None:
                    continue
                if infor in infor_ed_lists:
                    break
                else:
                    infor_lists.append(infor)
                    n += 1
        except Exception:
            print("解析失败")
        infor_lists.extend(infor_ed_lists)
        json.dump(infor_lists, fp, ensure_ascii=False)
        print("新增数据: ", n)
        print("数据总数：", len(infor_lists))
