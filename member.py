# coding: utf-8

"""
ﾘｻｲﾌﾟｵﾌｨｽより取得した情報を格納
"""
class MemberData:
    def __init__(self):
        self.shainCD = None # 社員番号
        self.shainNM = None # 名前
        self.kana = None # かな
        self.naisen = None # 内線
        self.userID = None # ユーザＩＤ
        self.mail = None # メールアドレス
        self.section = None # 部署
        self.post = None # 役職


"""
DVD情報を格納
"""
class DvdInfo:
    def __init__(self, searchCode):
        self.searchCode = searchCode  # 検索ワードより、パターンマッチ(英字3-5文字 & "-" & 数字3-5文字)により抽出
        self.hinban = None  # 検索サイトでの品番（searchCodeの方が一般的になる）
        self.title = None   # タイトル
        self.director = None    # 監督
        self.series = None    # シリーズ
        self.releaseDate = None    # 発売日
        self.maker = None    # メーカー
        self.label = None    # レーベル
        self.performer = None    # 出演者
        self.junle = None    # ジャンル
        self.recTime = None    # 収録時間
        self.comment = None    # コメント
        self.shosaiUrl = None   # 詳細ページのURL
        self.imageL = None    # 画像L
        self.imageS = None    # 画像S
        self.mode = None    # DVDの種類
        self.searchTime = None  # 検索時間
        self.searchSite = None  # 検索サイト
