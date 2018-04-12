import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
# options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1024,768')

# driver = webdriver.Chrome(chrome_options=options, executable_path="D:\\Program\\chromedriver_win32\\chromedriver.exe")
driver = webdriver.Chrome(chrome_options=options)

driver.get("http://tokyo-ame.jwa.or.jp/")

time.sleep(3)

driver.save_screenshot("d:/tmp/pythonTest/ame-hc3.png")

# トップ画面を開く。
driver.get('https://www.google.co.jp/')

time.sleep(3)
s = "大阪"
input_element = driver.find_element_by_name('q')
input_element.send_keys(s)
input_element.send_keys(Keys.RETURN)
time.sleep(3)

# output
results = []
[results.append(a.get_attribute('href')) for a in driver.find_elements_by_css_selector('h3 > a')]
print(results)

"""
# 検索メニュークリック
driver.find_element_by_xpath("//span[text()='検索']").click()

time.sleep(3)

# キーワード入力
driver.find_element_by_id("searchKeywordInput").send_keys("めそ子")

time.sleep(3)

# 検索ボタンクリック
driver.find_element_by_id("searchKeywordInputButton").click()

time.sleep(3)

# 検索結果の一覧からリンクのタイトルを取得する
for a in driver.find_elements_by_css_selector('h2 > a'):
    print(a.text)
"""

# 要素の表示待ち
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(By.CLASS_NAME, '_Rm')
)

# リンクをクリック
b = driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[1]/div/div/h3/a')
b.click()

wait = WebDriverWait(driver, 10)
#指定された要素(検索テキストボックス)が表示状態になるまで待機する
element = wait.until(EC.visibility_of_element_located((By.ID, "lst-ib")))
#検索テキストボックスにキー入力する
element.send_keys("要素が表示されるまでキー入力は待機します。")

driver.get("http://somedomain/url_that_delays_loading")
try:
    # 表示されるまで10秒待つ
    element = WebDriverWait(driver, 10).until(
        # IDの出現
        # 「引数に指定した locatorがDOMに現れるまで」待機. ただし待機終了時に, 必ずしもそれが画面に表示されているとは限らない.
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
        # 「引数に指定した locatorがDOMに現れるまで」待機.こちらは画面に表示されたうえで, それが0より大きい幅高さを持って存在している状態になるまで待機する.
        EC.visibility_of_element_located((By.ID, "myDynamicElement")) # こっちみたい
        # タイトルタグに任意のテキスト
        EC.title_contains("Google")
        # クラス表示待ち
        EC.visibility_of_element_located((By.CLASS_NAME, 'entry-title-link'))
    )
finally:
    driver.quit()
# スクリーンショットをとる。
driver.save_screenshot('d:/tmp/pythonTest/search_results.png')
driver.quit()