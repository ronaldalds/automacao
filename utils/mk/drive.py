from time import sleep
from .coin.coin import Coin
from .aside.aside import Aside
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.expected_conditions import (
    frame_to_be_available_and_switch_to_it,
    element_to_be_clickable,
    alert_is_present
)


class Mk:
    def __init__(self, username: str, password: str, url: str):
        self._username: str = username
        self._password: str = password
        largura = 1280
        altura = 960
        options = Options()
        options.add_argument("--port=4444")
        options.add_argument('--no-sandbox')
        options.add_argument(f"--window-size={largura},{altura}")
        # options.add_argument('--headless')
        webdriver_service = Service(ChromeDriverManager().install())
        self._driver = webdriver.Chrome(
            service=webdriver_service,
            options=options
            )
        self._wdw = WebDriverWait(self._driver, 300)
        self._mouse = ActionChains(self._driver)
        self._driver.get(url)

    def click(self, xpath: str):
        sleep(3)
        self._mouse.move_to_element(
            self._driver.find_element(
                By.XPATH, xpath
            )
        ).click().perform()
        sleep(3)

    def dbclick(self, xpath: str):
        sleep(3)
        self._mouse.move_to_element(
            self._driver.find_element(
                By.XPATH, xpath
            )
        ).double_click().perform()
        sleep(3)

    def text(self, xpath: str) -> str:
        value = self._driver.find_element(
            By.XPATH,
            xpath
        ).get_attribute("value")
        return value

    def write(self, xpath: str, text: str):
        sleep(3)
        self._mouse.move_to_element(self._driver.find_element(
            By.XPATH, xpath
        )).click().send_keys(text).perform()
        sleep(3)

    def login(self):
        self.write('//*[@name="user"]', self._username)
        self.write('//*[@name="password"]', self._password)
        self.click('//button[@name="user"]')

    def minimizeChat(self):
        self._driver.switch_to.default_content()
        self.iframeMain()
        self._wdw.until(element_to_be_clickable(
            (By.XPATH, '//*[@id="jsxc_toggleRoster"]')))
        self._driver.find_element(
            By.XPATH, '//*[@id="jsxc_toggleRoster"]').click()

    def close(self):
        sleep(5)
        self._driver.quit()

    def include(self):
        self._wdw.until(alert_is_present())
        self._driver.switch_to.alert.accept()
        sleep(5)

    def iframeMain(self):
        self._driver.switch_to.default_content()
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (By.XPATH, '//frame[@name="mainsystem"]')))
        return self

    def iframeForm(self):
        self._driver.switch_to.default_content()
        self.iframeMain()
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (By.XPATH, '//*[@class="FormIframe"]/iframe')))
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (By.XPATH, '//iframe[@name="mainform"]')))
        return self

    def iframeFormRes(self):
        self._driver.switch_to.default_content()
        self.iframeMain()
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (
                By.XPATH,
                '//div[@class="WFRIframeForm WFRIframeForm-Active"]/div[2]/iframe'
            )
        ))
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (By.XPATH, '//iframe[@name="mainform"]')))
        return self

    def iframeCoin(self):
        self._driver.switch_to.default_content()
        self.iframeMain()
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (By.XPATH, '//iframe[@name="mainform"]')))
        return self

    def iframeAsideCoin(self, coin: Coin):
        self._driver.switch_to.default_content()
        self.iframeCoin()
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (
                By.XPATH,
                f'//iframe[@componenteaba="{coin.title()} - PainelCloseAbaPrincipal"]'
            )
        ))
        self._wdw.until(
            frame_to_be_available_and_switch_to_it(
                (By.XPATH, '//iframe[@name="mainform"]')
            )
        )
        return self

    def iframePainel(self, coin: Coin, aside: Aside):
        self._driver.switch_to.default_content()
        self.iframeAsideCoin(coin)
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (
                By.XPATH,
                f'//iframe[@componenteaba="{aside.painel()}ClosePainelAba"]'
            )
        ))
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (By.XPATH, '//iframe[@name="mainform"]')))
        return self

    def iframeGrid(self, coin: Coin, aside: Aside):
        self._driver.switch_to.default_content()
        self.iframePainel(coin, aside)
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (By.XPATH, '//div[@id="lay"]/div[2]/div[2]/div[1]/div/iframe')))
        return self

    def iframeGridFaturamento(self, coin: Coin, aside: Aside):
        self._driver.switch_to.default_content()
        self.iframePainel(coin, aside)
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (By.XPATH, '//div[@id="lay"]/div[2]/div[2]/div[2]/div/iframe')))
        return self

    def iframeGridResFaturamento(self, coin: Coin, aside: Aside):
        self._driver.switch_to.default_content()
        self.iframePainel(coin, aside)
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (By.XPATH, '//div[@id="lay"]/div[2]/div[3]/div[1]/div/iframe')))
        return self

    def iframeGridRes(self, coin: Coin, aside: Aside):
        self._driver.switch_to.default_content()
        self.iframePainel(coin, aside)
        self._wdw.until(frame_to_be_available_and_switch_to_it(
            (By.XPATH, '//div[@id="lay"]/div[2]/div[3]/div[1]/div/iframe')))
        return self
