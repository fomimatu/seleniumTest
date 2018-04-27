import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import member as m
from datetime import datetime
import pickle
import json
import random

from json import JSONEncoder

waitSecond = 3  # 待機秒 (デバッグモードの時は長めにする）
waitRetry = 3

# ----------------------------------------------------------------------------------------------------------
# ページ読み込み待ち
# ----------------------------------------------------------------------------------------------------------
def page_loaded(web_driver):
   try:
        WebDriverWait(web_driver, waitSecond).until(
            lambda x: x.execute_script('return document.readyState;') == 'complete'
        )
        return True
   except:
        return False


# ----------------------------------------------------------------------------------------------------------
# 要素読み込み待ち
# ----------------------------------------------------------------------------------------------------------
def wait_element2(web_driver, locator):
    element = WebDriverWait(web_driver, waitSecond).until(
        # lambda x: x.find_element_by_id(elementID)
        # EC.presence_of_element_located(locator)
        EC.visibility_of_element_located(locator)
    )
    return element


# ----------------------------------------------------------------------------------------------------------
# 要素読み込み待ち
# ----------------------------------------------------------------------------------------------------------
def wait_element(web_driver, locator):
    element = WebDriverWait(web_driver, waitSecond).until(
        # lambda x: x.find_element_by_id(elementID)
        # EC.presence_of_element_located(locator)
        EC.visibility_of_element_located(locator)
    )
    return element


# ----------------------------------------------------------------------------------------------------------
# 要素読み込み待ち
# ----------------------------------------------------------------------------------------------------------
def element_wait(web_driver, locator):
    ele = None
    i = 0
    while (ele == None):
        try:
            ele = wait_element(web_driver, locator)
        except Exception as ex:
            web_driver.implicitly_wait(1)
            print(type(ex))
            if i > waitRetry:
                return None
            i += 1
    return ele


# ----------------------------------------------------------------------------------------------------------
# webDriver 初期化
# ----------------------------------------------------------------------------------------------------------
def driver_init(driver):
    options = Options()
    # options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1024,768')
    """
    # driver = webdriver.Chrome(
        chrome_options=options, executable_path="D:\\Program\\chromedriver_win32\\chromedriver.exe")
    """
    driver = webdriver.Chrome(chrome_options=options)
    return driver

# ----------------------------------------------------------------------------------------------------------
# ログオンから利用者設定画面まで（ここまでは以下の機能共通）
# ----------------------------------------------------------------------------------------------------------
def logon_to_kairi(driver):
    driver.get("https://recipeoffice.netcoms.ne.jp/sunco/index.html")
    if not page_loaded(driver):
        raise Exception

    # パスワード
    locator = (By.NAME, 'password')
    ele = wait_element(driver, locator)
    if ele == None:
        return False
    ele.send_keys("3744")

    # ID
    locator = (By.NAME, 'userid')
    ele = wait_element(driver, locator)
    if ele == None:
        return False
    ele.send_keys("TOMIMATSU")
    # 登録ボタン
    locator = (By.ID, "login_btn")
    ele = wait_element(driver, locator)
    ele.click()

    # 画面更新待ち
    driver.implicitly_wait(2)  # seconds

    # 管理者画面 (画面操作のみ)
    driver.find_element_by_css_selector("a.open_user_menu").click()
    driver.find_element_by_xpath("//a[text()='管理者設定']").click()
    driver.find_element_by_link_text("管理者システム設定").click()
    driver.find_element_by_link_text("利用者設定").click()


# ----------------------------------------------------------------------------------------------------------
# 部署リスト取得
# <params> webDriver
# <return> list[ tuple(部署idx, 部署名) ]
# ----------------------------------------------------------------------------------------------------------
def busho_get(driver):
    options = driver.find_elements_by_xpath("//select[@name='org_list']/option")
    idx_list = list(map(lambda x: x.get_attribute("value"), options))
    busho_list = list(map(lambda x: x.text.strip(), options))
    return list(zip(idx_list, busho_list))



# ----------------------------------------------------------------------------------------------------------
# 名前リスト取得
# <params> webDriver
# <params> list[ tuple(部署idx, 部署名) ]
# <return> list[ 名前 ]
# ----------------------------------------------------------------------------------------------------------
def name_get(driver, tpl_busho):
    # 部署から名前一覧取得
    remove_keys = []
    memberList = []
    while len(tpl_busho) != 0:
        print("start", len(tpl_busho))
        for key, val in tpl_busho:
            members_tmp = []
            flg = True
            try:
                # 部署クリック
                locator = (By.XPATH, "//select[@name='org_list']/option[@value='" + key + "']")
                ele = wait_element(driver, locator)
                if ele == None:
                    raise Exception("None error!")
                ele.click()
                time.sleep(0.5)
                locator = (By.XPATH, "//table[@class='layout']/tbody/tr/td/ul/li/a")
                if wait_element(driver, locator) != None:
                    tags = driver.find_elements_by_xpath(locator[1])
                    if len(tags) < 1:
                        raise Exception("None error!")
                    # 名前のテキスト検索するので、部署名、リーダーマークはつけたまま
                    # 上はやっぱりやめ。半角、◎をうまく読んでくれないから
                    members = list(map(lambda x: (x.text.replace("◎", "").strip().split('  '))[0], tags))
                    memberList.extend([m.MemberData(x, key, val) for x in members])
                else:
                    raise Exception("None error!")
                    flg = False
                print(val, ":", len(memberList))

            except TimeoutException:
                # 商品本部、営業部には今のところ人がいない.なのでFLG=TRUEのまま
                print("not found", val)
            except StaleElementReferenceException:
                # 画面の準備がまだ、再実行
                print("oontinue", val)
                flg = False
                continue
            except WebDriverException as e:
                flg = False
                print(e.args, val)
            except Exception as e:
                flg = False
                print(e.args, val)
            finally:
                if flg:
                    remove_keys.append(key)
        tpl_busho = list(filter(lambda x: x[0] not in remove_keys, tpl_busho))
        print("member_end")
    return memberList


# ----------------------------------------------------------------------------------------------------------
# 名前リスト詳細取得
# 何百回と繰り返し固まるのは確実なので、最初からアクセスする
# テキスト入力は連続ははねられるようなので不採用
# <params> list[名前]
# <return> list[ MemberData ]
# ----------------------------------------------------------------------------------------------------------
def shosai_get_input(members):
    driver = None
    driver = driver_init(driver)
    # 認証
    logon_to_kairi(driver)
    memberList = []
    while(len(members) > 0):
        try:
            time.sleep(0.5)
            member = members.pop(0)
            ele = driver.find_element_by_name('search_member_text')
            ele.clear()
            ele.send_keys(member)
            driver.find_element_by_link_text("検索").click()
            locator = (By.XPATH, "//th[text()='検索結果']/following-sibling::td/ul/li/a")
            ele = wait_element(driver, locator)
            if ele == None:
                raise Exception("None error!")
            ele.click()
            locator = (By.NAME, 'member_kanri_code')
            ele = wait_element(driver, locator)
            if ele == None:
                raise Exception("None error!")
            #
            o = m.MemberData()
            o.shainCD = driver.find_element_by_name('member_kanri_code').get_attribute('value')
            o.shainNM = driver.find_element_by_name('member_name').get_attribute('value')
            o.kana = driver.find_element_by_name('member_name_kana').get_attribute('value')
            o.mail = driver.find_element_by_name('address_mail').get_attribute('value')
            o.naisen = driver.find_element_by_name('address_ext_tel').get_attribute('value')
            o.userID = driver.find_element_by_name('member_login_user_id').get_attribute('value')
            o.section = Select(driver.find_element_by_id('main_org_id')).first_selected_option.text.strip()
            o.post = Select(driver.find_element_by_id('main_post_id')).first_selected_option.text.strip()
            #
            driver.find_element_by_link_text("閉じる").click()
            #
            memberList.append(o)
            print(len(members), o.shainNM)
        except Exception as ex:
            print(type(ex))
            members.append(member)  # 失敗したらメンバーは戻す
            print(len(memberList))
            driver.implicitly_wait(1)  # seconds
            driver.save_screenshot('d:/tmp/pythonTest/search_results.png')
            driver.quit()

# ----------------------------------------------------------------------------------------------------------
# 名前リスト詳細取得
# 何百回と繰り返し固まるのは確実なので、ここで完結できるように最初からアクセスする
# <params> list[ MemberData ]
# <return> list[ MemberData ]
# ----------------------------------------------------------------------------------------------------------
def shosai_get(member_list):
    driver = None
    driver = driver_init(driver)
    # 認証
    logon_to_kairi(driver)
    # 巡回
    old_sectionCD = ""
    while (any(x.accessTime == None for x in member_list)):
        for mem in member_list:
            if mem.accessTime != None:
                continue
            try:
                # 部署が変わっていたら
                if mem.sectionCD != old_sectionCD:
                    # 部署クリック
                    locator = (By.XPATH, "//select[@name='org_list']/option[@value='" + mem.sectionCD + "']")
                    ele = wait_element(driver, locator)
                    if ele == None:
                        raise Exception("None error!")
                    ele.click()
                    time.sleep(0.3)
                # 名前をクリック
                locator = (By.XPATH, "//table[@class='layout']/tbody/tr/td/ul/li/a[contains(text(),'" + mem.shainNM + "')]")
                ele = wait_element(driver, locator)
                if ele != None:
                    ele.click()
                    time.sleep(0.1)
                    mem.shainCD = driver.find_element_by_name('member_kanri_code').get_attribute('value')
                    # mem.shainNM = driver.find_element_by_name('member_name').get_attribute('value')
                    mem.kana = driver.find_element_by_name('member_name_kana').get_attribute('value')
                    mem.mail = driver.find_element_by_name('address_mail').get_attribute('value')
                    mem.naisen = driver.find_element_by_name('address_ext_tel').get_attribute('value')
                    mem.userID = driver.find_element_by_name('member_login_user_id').get_attribute('value')
                    mem.section = Select(driver.find_element_by_id('main_org_id')).first_selected_option.text.strip()
                    mem.post = Select(driver.find_element_by_id('main_post_id')).first_selected_option.text.strip()
                    mem.accessTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                    #
                    driver.find_element_by_link_text("閉じる").click()
                    print(mem.section, mem.shainNM)
                else:
                    raise Exception("None error!")
                old_sectionCD = mem.sectionCD
            except:
                driver.close()
                return False, member_list
    driver.close()
    return True, member_list

# ----------------------------------------------------------------------------------------------------------
# リスト重複削除
# KEYは社員名
# <params> list[ MemberData ]
# <return> list[ MemberData ]
# ----------------------------------------------------------------------------------------------------------
# 重複削除
def remove_duplicates(x):
    y=[]
    old = ""
    for i in x:
        if old != i.shainNM:
            y.append(i)
        old = i.shainNM
    return y
# ----------------------------------------------------------------------------------------------------------
# TEST
# ----------------------------------------------------------------------------------------------------------
def test_sort():
    with open('d:/tmp/pcl_receipe.bin', 'rb') as sr:
        member_list = pickle.load(sr)
    tmp_member_list = remove_duplicates(sorted(member_list, key=lambda x: x.shainNM))
    member_list2 = sorted(tmp_member_list, key=lambda x: member_list.index(x))


    # xxx = remove_duplicates(sorted(memberList, key=lambda x: x.shainNM))
    # zzz = sorted(xxx, key=lambda x: memberList.index(x))

    print(member_list2)


# ----------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------
def main():
    start = time.time()

    driver = None
    driver = driver_init(driver)

    # 認証
    logon_to_kairi(driver)
    # 部署一覧取得
    lst_tpl_busho = busho_get(driver)
    # 不要部署（topのサンコー、33その他,-99退職)
    lst_tpl_busho = list(filter(lambda x: x[0] not in ["1", "33", "-99"], lst_tpl_busho))

    member_list = name_get(driver, lst_tpl_busho)

    print("メンバー取得数：", len(member_list))
    driver.quit()
    time.sleep(1)

    # pickle保存
    with open('d:/tmp/pcl_receipe0.bin', 'wb') as sw:
        pickle.dump(member_list, sw)

    # 何度も固まるから、一つの関数で完結させる
    flg = False
    rCount = 0
    while flg == False:
        result = shosai_get(member_list)
        flg = result[0]
        member_list = result[1]
        print("retry", rCount)
        rCount += 1
        time.sleep(1)

    # 名前重複削除（部署またがり分削除）
    tmp_member_list = remove_duplicates(sorted(member_list, key=lambda x: x.shainNM))
    member_list = sorted(tmp_member_list, key=lambda x: member_list.index(x))

    # pickle保存
    with open('d:/tmp/pcl_receipe.bin', 'wb') as sw:
        pickle.dump(member_list, sw)

    # JSON保存
    with open('d:/tmp/receipe.json', 'w') as sw:
        json_string = json.dumps([ob.__dict__ for ob in member_list], sort_keys=True, ensure_ascii=False, indent=2)
        sw.write(json_string)

    # 処理時間
    print(time.time() - start)

    # sys.exit()  # 途中終了
    # スクリーンショットをとる。
    # driver.implicitly_wait(2)  # seconds
    # driver.save_screenshot('d:/tmp/pythonTest/search_results.png')

# ----------------------------------------------------------------------------------------------------------
# スタート
# ----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

