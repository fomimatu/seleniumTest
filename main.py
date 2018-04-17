import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import member as m

waitSecond = 5  # 待機秒


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
def wait_element(web_driver, locator):
    try:

        element = WebDriverWait(web_driver, waitSecond).until(
            # lambda x: x.find_element_by_id(elementID)
            # EC.visibility_of_element_located((By.LINK_TEXT, name))
            EC.visibility_of_element_located(locator)
        )
        return element
    except:
        return None


# ----------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------
def main():
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
    # タイムアウトまでの時間
    driver.set_page_load_timeout(waitSecond)

    # 認証
    # try:  # タイムアウト例外が起きる
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
    # 部署一覧取得
    options = driver.find_elements_by_xpath("//select[@name='org_list']/option")
    idx_list = list(map(lambda x: x.get_attribute("value"), options))
    busho_list = list(map(lambda x: x.text.strip(), options))
    dic_busho = dict(zip(idx_list, busho_list))
    member_list = []
    # 名前取得

    for key,val in dic_busho.items():
        # 部署クリック
        locator = (By.XPATH, "//select[@name='org_list']/option[@value='" + key + "']")
        ele = wait_element(driver, locator)
        if ele == None:
            return False
        ele.click()
        driver.implicitly_wait(1)  # seconds

        locator = (By.XPATH, "//table[@class='layout']/tbody/tr/td/ul/li/a")
        if wait_element(driver, locator) != None:
            tags = driver.find_elements_by_xpath(locator[1])
            members = list(map(lambda x: x.text.replace("◎", "").strip(), tags))
            member_list.append({val : members})
        print(len(member_list))








    # ここから先は、必ず一度は固まるがこのまま作る

    # スクリーンショットをとる。
    driver.implicitly_wait(2)  # seconds
    driver.save_screenshot('d:/tmp/pythonTest/search_results.png')
# except:
    # return False
# finally:
    driver.quit()



# ----------------------------------------------------------------------------------------------------------
# スタート
# ----------------------------------------------------------------------------------------------------------

main()

