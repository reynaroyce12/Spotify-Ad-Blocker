import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.spotify.com/us/")
driver.maximize_window()

wait = WebDriverWait(driver, 15)
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
on_mute = False


def login():
    login_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/header/div/nav/ul/li[6]/a')
    login_button.click()
    wait.until(expected_conditions.visibility_of_element_located(
        (By.ID, 'login-username')))
    email_button = driver.find_element(By.ID, 'login-username')
    email_button.click()
    type_credentials(email)
    password_button = driver.find_element(By.ID, 'login-password')
    password_button.click()
    type_credentials(password)
    submit_button = driver.find_element(By.XPATH, '//*[@id="login-button"]/div[1]')
    submit_button.click()
    dismiss_alerts()


def type_credentials(credentials):
    actions = ActionChains(driver)
    actions.send_keys(credentials)
    actions.perform()


def dismiss_alerts():
    wait.until(expected_conditions.visibility_of_element_located(
        (By.XPATH, '/html/body/div[16]/div/div/div/div[2]/button[2]')))
    banner = driver.find_element(By.XPATH, '/html/body/div[16]/div/div/div/div[2]/button[2]')
    banner.click()


def mute_unmute():
    volume_button = driver.find_element(By.ID, 'volume-icon')
    volume_button.click()


def now_playing_ad():
    now_playing_element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[1]/div')
    now_playing_title = now_playing_element.get_attribute("aria-label")
    if now_playing_title == 'Advertisement':
        return True
    else:
        return False


login()

while True:
    if now_playing_ad() and on_mute == False:
        mute_unmute()
        on_mute = True
    elif not now_playing_ad() and on_mute == True:
        mute_unmute()
        on_mute = False
