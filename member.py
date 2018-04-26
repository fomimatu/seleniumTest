# coding: utf-8
import json
from json import JSONEncoder

"""
ﾘｻｲﾌﾟｵﾌｨｽより取得した情報を格納
"""
class MemberData:
    def __init__(self, shain_nm=None, section_cd=None, section_nm=None):  # デフォルト値
        self.sectionCD = section_cd  # 部署番号（ﾘｻｲﾌﾟｵﾝﾘｰ)
        self.shainCD = None  # 社員番号
        self.shainNM = shain_nm  # 名前
        self.kana = None  # かな
        self.naisen = None  # 内線
        self.userID = None  # ユーザＩＤ
        self.mail = None  # メールアドレス
        self.section = section_nm  # 部署
        self.post = None  # 役職
        self.accessTime = None  # 更新時間、ここがNoneなら末巡回とする
