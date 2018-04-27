import json
import member as mem
from json import JSONEncoder
from collections import namedtuple
import pickle


# 重複削除
def remove_duplicates(x):
    y=[]
    old = ""
    for i in x:
        if old != i.shainNM:
            y.append(i)
        old = i.shainNM
    return y

# シリアライズ
lst = ["東京", "横浜", "大阪", "図書館", "愛知", "福岡", "大阪"]
memberList = list(map(lambda x: mem.MemberData(x), lst))
xxx = remove_duplicates(sorted(memberList, key=lambda x: x.shainNM))
zzz = sorted(xxx, key=lambda x: memberList.index(x))


print(zzz)




"""
json_string = json.dumps([ob.__dict__ for ob in memberList], sort_keys=True, ensure_ascii=False, indent=2)

# デシリアライズ
obj = json.loads(json_string)
print(obj[0]["shainNM"])
print(obj)
#
def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())

obj2 = json.loads(json_string, object_hook=_json_object_hook)
print(obj2[1].shainNM)
print(obj2)


# objectのシリアライズ化
# JSONでの運用は、技術が足らず諦める
# pickleを使用する
with open('d:/tmp/pickle.bin', 'wb') as sw:
    pickle.dump(memberList, sw)

with open('d:/tmp/pickle.bin', 'rb') as sr:
    mem_list = pickle.load(sr)
print(mem_list)

"""