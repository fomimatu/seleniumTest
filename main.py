import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import member as m

waitSecond = 10 # 待機秒


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

    # 認証
    driver.get("https://recipeoffice.netcoms.ne.jp/sunco/index.html")
    # パスワード

    ele = wait_element(driver, (By.NAME, 'password'))
    if ele == None:
        return False
    ele.send_keys("3744")
    # ID
    ele = wait_element(driver, (By.NAME, 'userid'))
    if ele == None:
        return False
    ele.send_keys("TOMIMATSU")
    # 登録ボタン
    ele = wait_element(driver, (By.ID, "login_btn"))
    ele.click()

    # 画面更新待ち
    driver.implicitly_wait(2)  # seconds

    # 管理者画面 (画面操作のみ)
    driver.find_element_by_css_selector("a.open_user_menu").click()
    driver.find_element_by_xpath("//a[text()='管理者設定']").click()
    driver.find_element_by_link_text("管理者システム設定").click()
    driver.find_element_by_link_text("利用者設定").click()
    # 部署一覧取得
    options = driver.find_elements_by_name("org_list")
    for op in options:
        txt = op.get_attribute("option")
        val = op.get_attribute("value")


    # スクリーンショットをとる。
    driver.implicitly_wait(2)  # seconds
    driver.save_screenshot('d:/tmp/pythonTest/search_results.png')
    driver.quit()


# ----------------------------------------------------------------------------------------------------------
# スタート
# ----------------------------------------------------------------------------------------------------------

main()

