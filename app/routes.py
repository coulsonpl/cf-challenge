import logging
from datetime import datetime, timedelta
import json
from concurrent.futures import ThreadPoolExecutor
from flask import request, Response, current_app as app

from app.config import configure_logging, get_env_value
from app.utils import handle_error
from app.pop.gtoken import get_pop_gtoken

configure_logging()

@app.route("/challenge/pop/gtoken", methods=["GET", "POST", "OPTIONS"])
def onRequest():
    try:
        return get_pop_gtoken()
    except Exception as e:
        logging.error("An error occurred with chat : %s", e)
        return handle_error(e)
