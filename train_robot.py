from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import os
import wget

# 設定 Chrome 選項
PATH = "D:/program/spider/tos_data/chromedriver.exe"
service = Service(PATH)
driver = webdriver.Chrome(service=service)
driver.get("https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query")
time.sleep(2)

# 身分證號碼
id_num = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".idmember.pid.form-input"))
)
# 出發點
start_station = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "startStation"))
)
# 目的地
end_station = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "endStation")) 
)
# 出發日期
date = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="queryForm"]/div[2]/div[2]/div[1]/div[2]/button'))
)
#車次
train_no = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".form-control.input-small.trainNoList.train1"))
)

id_num.send_keys("A123456789") # 輸入身分證號碼
start_station.send_keys("7000") # 輸入出發站代碼
end_station.send_keys("3300") # 輸入目的地站代碼
date_from_today = 3 # 預計出發日-今天日期
date.click() # 點擊日期選擇器
for day in range(date_from_today):
    date.send_keys(Keys.ARROW_RIGHT) # 按下鍵盤向下鍵
date.send_keys(Keys.ENTER) # 按下鍵盤 Enter 鍵

train_no.send_keys("271") # 輸入車次




# 切換到 iframe
iframe = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src,'recaptcha')]"))
)
driver.switch_to.frame(iframe)

# 點選 checkbox
checkbox = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
)
print("請手動完成驗證（無時間限制）")

# 等待驗證完成（檢查 aria-checked 屬性是否為 true）
while True:
    status = checkbox.get_attribute("aria-checked")
    if status == "true":
        print("驗證已完成")
        break
    time.sleep(1)

# 回到主畫面
driver.switch_to.default_content()

book = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="queryForm"]/div[4]/input[2]'))
)
book.click()
print("已送出訂票")




finish_book = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="order"]/div[4]/button'))
)
driver.execute_script("arguments[0].scrollIntoView(true);", finish_book)
time.sleep(1)  # 給動畫一點時間
finish_book.click()
print("已完成訂票")


# 等待付款方式出現
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "paymentMethod"))
)

# 選擇付款方式
pay_type = Select(driver.find_element(By.ID, "paymentMethod"))
pay_type.select_by_index(1)  # 這裡選第2個，可改成 select_by_value("xxx")

# 點擊付款按鈕
pay_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="order"]/div[4]/button[2]'))
)
pay_button.click()
print("已送出付款")

#time.sleep(1)


