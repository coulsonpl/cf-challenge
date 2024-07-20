import logging
from datetime import datetime, timedelta
import json
from concurrent.futures import ThreadPoolExecutor
from flask import jsonify, request, Response, current_app as app

from app.config import configure_logging, get_env_value
from app.utils import handle_error
from app.pop.gtoken import get_pop_gtoken, get_user_agent

configure_logging()

@app.route("/challenge/pop/gtoken", methods=["GET", "POST", "OPTIONS"])
def onRequest():
    try:
        gtoken = get_pop_gtoken()
        if gtoken is None:
            # 如果 gtoken 为 None,返回一个错误响应
            return jsonify({
                "error": "No gtoken available",
                "status": "error"
            }), 404  # 使用 404 状态码表示未找到资源
        
        # 如果 gtoken 不为 None,返回成功响应
        res = {
            "status": "success",
            "User-Agent": get_user_agent(),
            "GToken": gtoken
        }
        return jsonify(res), 200  # 使用 200 状态码表示成功
    except Exception as e:
        logging.error("An error occurred with chat : %s", e)
        return handle_error(e)
