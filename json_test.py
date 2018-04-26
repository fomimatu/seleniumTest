import json
import member as mem
from json import JSONEncoder
from collections import namedtuple
import pickle

# シリアライズ
lst = ["東京", "大阪", "図書館", "愛知", "福岡"]
memberList = list(map(lambda x: mem.MemberData(x), lst))
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

