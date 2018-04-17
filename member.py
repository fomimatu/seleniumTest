# coding: utf-8

"""
ﾘｻｲﾌﾟｵﾌｨｽより取得した情報を格納
"""
class MemberData:
    def __init__(self):
        self.shainCD = None  # 社員番号
        self.shainNM = None  # 名前
        self.kana = None  # かな
        self.naisen = None  # 内線
        self.userID = None  # ユーザＩＤ
        self.mail = None  # メールアドレス
        self.section = None  # 部署
        self.post = None  # 役職
