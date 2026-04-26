import csv
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

REGISTER_URL = "https://helpcoder.cc/register"
OUTPUT_FILE = "accounts.csv"

def rand_str(n=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

def generate_account():
    username = f"user_{rand_str(6)}"
    password = f"Pwd@{rand_str(8)}"
    email = f"{username}@test.local"
    return username, password, email

def save_account(username, password, email, filename=OUTPUT_FILE):
    write_header = False
    try:
        with open(filename, "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        write_header = True

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["username", "password", "email"])
        writer.writerow([username, password, email])

def main():
    username, password, email = generate_account()
    print("准备注册账号：")
    print("username =", username)
    print("password =", password)
    print("email    =", email)

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # 如果你已把 chromedriver 加入 PATH，可直接这样启动
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(REGISTER_URL)

        wait = WebDriverWait(driver, 15)

        # ===== 下面这些选择器需要你根据页面实际情况微调 =====
        # 优先尝试 name 属性
        username_input = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_input = driver.find_element(By.NAME, "password")

        # 邮箱字段如果存在就填
        email_input = None
        try:
            email_input = driver.find_element(By.NAME, "email")
        except:
            pass

        username_input.clear()
        username_input.send_keys(username)

        password_input.clear()
        password_input.send_keys(password)

        if email_input:
            email_input.clear()
            email_input.send_keys(email)

        # 提交按钮：按按钮文本、type=submit、或 class 去找
        submit_button = None

        possible_submit_selectors = [
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.XPATH, "//button[contains(., '注册')]"),
            (By.XPATH, "//button[contains(., 'Register')]"),
            (By.XPATH, "//span[contains(., '注册')]/ancestor::button"),
        ]

        for by, selector in possible_submit_selectors:
            try:
                submit_button = driver.find_element(by, selector)
                if submit_button:
                    break
            except:
                continue

        if not submit_button:
            raise Exception("未找到注册按钮，请检查页面按钮选择器")

        submit_button.click()

        # 等待页面变化，简单等几秒
        time.sleep(5)

        # 这里根据你的站点特征自行判断成功逻辑
        current_url = driver.current_url
        page_source = driver.page_source

        success_keywords = ["注册成功", "success", "登录", "dashboard", "welcome"]

        if any(k.lower() in page_source.lower() for k in success_keywords) or current_url != REGISTER_URL:
            print("[+] 可能注册成功")
            save_account(username, password, email)
            print(f"[+] 账号已保存到 {OUTPUT_FILE}")
        else:
            print("[-] 未确认注册成功，请手动检查页面反馈")
            print("当前URL：", current_url)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()