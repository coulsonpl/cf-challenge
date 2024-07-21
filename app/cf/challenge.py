from time import sleep
from DrissionPage import ChromiumOptions, WebPage
# import os
from pyvirtualdisplay import Display
from app.config import get_proxies, configure_logging

configure_logging()

class CFClearanceManager:
    def __init__(self):
        self.page = None
        self.display = None

    def setup_virtual_display(self):
        if self.display is None:
            self.display = Display(visible=1, size=(1280, 720))
            self.display.start()

    def setup_browser(self):
        self.setup_virtual_display()  # 确保虚拟显示已启动

        co = ChromiumOptions().auto_port()
        co.set_argument('--no-sandbox').set_argument('--disable-gpu')
        proxies = get_proxies()
        if 'https' in proxies and '@' not in proxies['https']:
            co.set_argument(f"--proxy-server={proxies['https']}")

        self.page = WebPage(chromium_options=co)

    def ensure_browser(self):
        if self.page is None:
            self.setup_browser()
        else:
            try:
                self.page.url
            except Exception:
                self.close_browser()
                self.setup_browser()

    def get_cf_clearance(self):
        self.ensure_browser()

        self.page.get('https://zhile.io/')
        self.page.wait.load_start()

        try:
            box = self.page.ele('.cf-turnstile-wrapper').shadow_root.ele('tag:iframe').ele('tag:body').shadow_root.ele('.cb-i')
            box.click()

            # 使用动作链有时候反而通不过
            # page.actions.move_to(box).click()

            # 等待指定元素被删除
            self.page.wait.ele_deleted('.cf-turnstile-wrapper', timeout=10)
            sleep(8)
            
            cookies = self.page.cookies()
            self.close_browser()

            for cookie in cookies:
                if cookie['name'] == 'cf_clearance':
                    return cookie['value']
            return None
        except Exception as e:
            print(f"Error during Cloudflare clearance: {e}")
            self.close_browser()
            return None

    def close_browser(self):
        if self.page:
            self.page.quit()
            self.page = None

cf_clearance_manager = CFClearanceManager()

def get_cf_clearance():
    return cf_clearance_manager.get_cf_clearance()