import os
import logging
import random
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取环境变量值，支持大小写不敏感，空值返回默认值。
def get_env_value(key, default=None):
    value = os.getenv(key) or os.getenv(key.lower()) or os.getenv(key.upper())
    return default if value in [None, ''] else value

log_level = get_env_value('LOG_LEVEL', 'INFO').upper()

def configure_logging():
    extended_log_format = (
        '%(asctime)s | %(levelname)s | %(name)s | '
        '%(process)d | %(filename)s:%(lineno)d | %(funcName)s | %(message)s'
    )
    logging.basicConfig(level=log_level, format=extended_log_format)

def get_proxies():
    http_proxy = get_env_value('HTTP_PROXY')
    https_proxy = get_env_value('HTTPS_PROXY')

    proxy = {}
    if http_proxy:
        proxy['http'] = http_proxy
    if https_proxy:
        proxy['https'] = https_proxy
    # 若只存在一个键，使用其值填充另一个
    if 'http' in proxy or 'https' in proxy:
        proxy.setdefault('http', proxy.get('https'))
        proxy.setdefault('https', proxy.get('http'))
    # logging.info("proxy URL %s", proxy)
    return proxy if proxy else None