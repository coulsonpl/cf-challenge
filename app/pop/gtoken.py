import os
import undetected_chromedriver as uc
from pyvirtualdisplay import Display
import logging
from app.config import get_proxies, configure_logging

POPAI_BASE_URL = "https://www.popai.pro/"

configure_logging()

class GTokenManager:
    def __init__(self):
        self.driver = None
        self.display = None
        self.user_agent = None

    def setup_browser(self):
        self.display = Display(visible=0, size=(1280, 720), backend="xvfb")
        self.display.start()

        options = uc.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        proxies = get_proxies()
        if 'https' in proxies and '@' not in proxies['https']:
            options.add_argument(f"--proxy-server={proxies['https']}")

        self.driver = uc.Chrome(options=options)
        self.driver.get(POPAI_BASE_URL)

        self.user_agent = self.driver.execute_script("return navigator.userAgent")
        logging.info(f"Browser User Agent: {self.user_agent}")

    def ensure_browser(self):
        if self.driver is None:
            self.setup_browser()
        else:
            try:
                # 尝试进行一个简单的操作来检查浏览器是否仍然响应
                self.driver.current_url
            except Exception:
                # 如果出现异常，关闭现有的浏览器并重新设置
                self.close_browser()
                self.setup_browser()

    def get_user_agent(self):
        if self.user_agent is None:
            self.user_agent = self.driver.execute_script("return navigator.userAgent")
        return self.user_agent

    def get_gtoken(self):
        try:
            self.ensure_browser()

            # 获取当前脚本文件的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 构建 JS 文件的完整路径
            js_file_path = os.path.join(current_dir, 'recaptcha__zh_cn.js')
            with open(js_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                str_js = f.read()

            gtoken = self.driver.execute_async_script(str_js)
            print(f"Got new GToken: {gtoken}")
            return gtoken
        except Exception as e:
            logging.error(f"An error occurred while getting GToken: {e}")
            self.close_browser()
            self.setup_browser()
            return None

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
        if self.display:
            self.display.stop()
            self.display = None

# 创建一个全局的 GTokenManager 实例
gtoken_manager = GTokenManager()

# 提供一个获取 token 的函数，可以在其他文件中直接调用
def get_pop_gtoken():
    return gtoken_manager.get_gtoken()

def get_user_agent():
    return gtoken_manager.get_user_agent()