import functools

tpl_list = [('1', 'サンコーインダストリー株式会社'),
 ('2', '役員グループ'),
 ('3', '営業部'),
 ('4', '第１営業部'),
 ('5', '営業第１課'),
 ('6', '東大阪営業所'),
 ('7', '北支店'),
 ('8', '第２営業部'),
 ('10', '営業北日本課'),
 ('412', '営業東日本課'),
 ('11', '営業中日本課'),
 ('12', '営業西日本課'),
 ('13', '営業推進課'),
 ('199', '営業東海北陸課'),
 ('357', '営業九州・山口課'),
 ('9', '東京支店'),
 ('981', '東京\u3000営業１課'),
 ('982', '東京\u3000営業２課'),
 ('983', '東京\u3000営業３課'),
 ('984', '東京\u3000総務部'),
 ('14', '商品本部'),
 ('15', '仕入部'),
 ('16', '仕入第１課'),
 ('17', '仕入第２課'),
 ('18', '仕入第３課'),
 ('19', '特殊ファスナー課'),
 ('523', '国際取引課'),
 ('20', '品質保証部'),
 ('21', '経理部'),
 ('22', '総務部'),
 ('23', '経営戦略室'),
 ('24', 'ＩＳＯ推進室'),
 ('25', '物流部'),
 ('26', '本社物流課'),
 ('27', '東大阪物流課'),
 ('1060', '電算課'),
 ('28', '商品企画部'),
 ('29', '電算部'),
 ('33', 'その他'),
 ('-99', '[退職者又は利用停止]')]
removeList = [ '2', '3', '4', '5', '6', '7', '8', '10', '412', '11', '12', '13', '199', '357', '9', '981', '982', '983', '984', '14', '15', '16', '17', '18', '19', '523', '20', '21', '22', '23', '24', '25', '26', '27', '1060', '28', '29', '33', '-99']
# removeList = ['1', '2', '3']

#for key, val in tpl_list:
    # print(key, val)

tpl_list = list(filter(lambda x: x[0] not in removeList, tpl_list))
print(tpl_list)

