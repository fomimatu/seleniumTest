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
# ページ読取完了


# 認証画面
def login(driver, url):
    driver.get(url)
    try:
        element = WebDriverWait(driver, waitSecond).until(
            lambda x: x.find_element_by_tag_name("html"))
        return driver.execute_script('return document.readyState;') == "complete"
    except:
        return False




options = Options()
# options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1024,768')




# driver = webdriver.Chrome(chrome_options=options, executable_path="D:\\Program\\chromedriver_win32\\chromedriver.exe")
driver = webdriver.Chrome(chrome_options=options)
ele = login(driver, "https://recipeoffice.netcoms.ne.jp/sunco/index.html")
print(ele)

# driver.get("http://tokyo-ame.jwa.or.jp/")

# スクリーンショットをとる。
driver.save_screenshot('d:/tmp/pythonTest/search_results.png')
driver.quit()




