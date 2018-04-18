import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
def element_wait(web_driver, locator):
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
    ele = None
    i = 0
    while (ele == None):
        try:
            ele = element_wait(web_driver, locator)
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
# 部署一覧取得
# <param>   webDriver
# <return>  Dictionary{ IDX : 部署名 }
# ----------------------------------------------------------------------------------------------------------
def busho_get(driver):
    options = driver.find_elements_by_xpath("//select[@name='org_list']/option")
    idx_list = list(map(lambda x: x.get_attribute("value"), options))
    busho_list = list(map(lambda x: x.text.strip(), options))
    return list(zip(idx_list, busho_list))


# ----------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------
def main():
    driver = None
    driver = driver_init(driver)

    # 認証
    logon_to_kairi(driver)
    # 部署一覧取得
    tpl_busho = busho_get(driver)

    # sys.exit()  # 途中終了

    # 部署から名前一覧取得
    # ここから巡回中落ちる場合がある
    member_list = []
    remove_keys = []
    while len(tpl_busho) != 0:
        print("start", len(tpl_busho))
        for key, val in tpl_busho:
            try:
                # 部署クリック
                locator = (By.XPATH, "//select[@name='org_list']/option[@value='" + key + "']")
                ele = wait_element(driver, locator)
                if ele == None:
                    raise Exception("None error!")
                driver.implicitly_wait(1)  # seconds
                ele.click()
                print(val)
                """
                locator = (By.XPATH, "//table[@class='layout']/tbody/tr/td/ul/li/a")
                if wait_element(driver, locator) != None:
                    tags = driver.find_elements_by_xpath(locator[1])
                    members = list(map(lambda x: x.text.replace("◎", "").strip(), tags))
                    member_list.append({val : members})
                print(val, len(member_list))
                """
                remove_keys.append(key)
            except Exception as e:
                print(type(e))

        tpl_busho = list(filter(lambda x: x[0] not in remove_keys, tpl_busho))
        print("end", len(tpl_busho))

    # ここから先は、必ず一度は固まるがこのまま作る

    # スクリーンショットをとる。
    driver.implicitly_wait(2)  # seconds
    driver.save_screenshot('d:/tmp/pythonTest/search_results.png')

    driver.quit()



# ----------------------------------------------------------------------------------------------------------
# スタート
# ----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

