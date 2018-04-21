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
    members = []
    while len(tpl_busho) != 0:
        print("start", len(tpl_busho))
        for key, val in tpl_busho:
            members_tmp = []
            try:
                # 部署クリック
                locator = (By.XPATH, "//select[@name='org_list']/option[@value='" + key + "']")
                ele = wait_element(driver, locator)
                if ele == None:
                    raise Exception("None error!")
                ele.click()
                time.sleep(0.3)
                locator = (By.XPATH, "//table[@class='layout']/tbody/tr/td/ul/li/a")
                if wait_element(driver, locator) != None:
                    tags = driver.find_elements_by_xpath(locator[1])
                    if len(tags) < 1:
                        raise Exception("None error!")
                    members_tmp = list(map(lambda x: (x.text.replace("◎", "").strip().split('  '))[0], tags))
                    members.extend(members_tmp)
                else:
                    raise Exception("None error!")
                print(val)
                print(val, members)

            except TimeoutException:
                # 商品本部、営業部には今のところ人がいない
                print("not found", val)
            except StaleElementReferenceException:
                # 画面の準備がまだ、再実行
                print("oontinue", val)
                continue
            # except WebDriverException:
            # except Exception as e:
            finally:
                remove_keys.append(key)

        tpl_busho = list(filter(lambda x: x[0] not in remove_keys, tpl_busho))
        print("end", len(tpl_busho))

    return members


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
# 何百回と繰り返し固まるのは確実なので、最初からアクセスする
# <params> list[名前]
# <return> list[ MemberData ]
# ----------------------------------------------------------------------------------------------------------
def shosai_get(members):
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
# Main
# ----------------------------------------------------------------------------------------------------------
def main():
    driver = None
    driver = driver_init(driver)

    # 認証
    logon_to_kairi(driver)
    # 部署一覧取得
    lst_tpl_busho = busho_get(driver)
    # 不要部署（topのサンコー、33その他,-99退職)
    lst_tpl_busho = list(filter(lambda x: x[0] not in ["1", "33", "-99"], lst_tpl_busho))

    members = name_get(driver, lst_tpl_busho)
    # 重複削除、順番変動
    members = list(set(members))
    print("重複削除、順番変動かも", len(members))
    driver.quit()
    time.sleep(1)

    # 何度も固まるから、一つの関数で完結させる
    shosai_get(members)

    # sys.exit()  # 途中終了

    """
    # 部署から名前一覧取得
    # ここから巡回中落ちる場合がある
    member_list = []
    remove_keys = []
    while len(tpl_busho) != 0:
        print("start", len(tpl_busho))
        for key, val in tpl_busho:
            members = []
            try:
                # 部署クリック
                locator = (By.XPATH, "//select[@name='org_list']/option[@value='" + key + "']")
                ele = wait_element(driver, locator)
                if ele == None:
                    raise Exception("None error!")
                ele.click()
                time.sleep(0.3)
                locator = (By.XPATH, "//table[@class='layout']/tbody/tr/td/ul/li/a")
                if wait_element(driver, locator) != None:
                    tags = driver.find_elements_by_xpath(locator[1])
                    if len(tags) < 1:
                        raise Exception("None error!")

                    members = list(map(lambda x: (x.text.replace("◎", "").strip().split('  '))[0], tags))
                    member_list.append({val: members})
                else:
                    raise Exception("None error!")
                print(val)
                print(val, members)

            except TimeoutException:
                # 商品本部、営業部には今のところ人がいない
                print("not found", val)
            except StaleElementReferenceException:
                # 画面の準備がまだ
                print("oontinue", val)
                continue
            # except WebDriverException:
            # except Exception as e:
            finally:
                remove_keys.append(key)

        tpl_busho = list(filter(lambda x: x[0] not in remove_keys, tpl_busho))
        print("end", len(tpl_busho))

    print("member_list", member_list)

    # ここから先は、必ず一度は固まるがこのまま作る
    """

    # スクリーンショットをとる。
    driver.implicitly_wait(2)  # seconds
    driver.save_screenshot('d:/tmp/pythonTest/search_results.png')

    driver.quit()



# ----------------------------------------------------------------------------------------------------------
# スタート
# ----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

