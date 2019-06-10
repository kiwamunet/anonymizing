import math
import os
import sys

# 年齢を年代にする


def age_range(obj):
    objs = math.nan
    try:
        objs = int(obj / 10) * 10
    except ValueError:
        print("error")
        # TODO: error ハンドリング
    except TypeError:
        print("error TypeError")
    return objs


def locale(obj):
    # この辺の処理どうしよう。。。。。
    # 一旦適当でいいか
    result = ""
    path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)),
        '../../../samples/KEN_ALL.CSV')

    fp = open(path, "rt", encoding="shift_jis")
    for line in fp:
        line = line.replace(' ', '')
        line = line.replace('"', '')
        cells = line.split(",")
        zipno = cells[2]  # 郵便番号
        ken = cells[6]  # 都道府県
        shi = cells[7]  # 市区
        cho = cells[8]  # 市区以下
        title = ken + shi + cho
        print(str(obj))
        if title.find(str(obj)) >= 0:
            print(zipno + ":" + title)
            result = ken
            break
        if (str(obj).find(ken)) >= 0:
            print(zipno + ":" + title)
            result = ken
            break
    fp.close()
    return result
