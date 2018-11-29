#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : yasin
# @time   : 11/29/18 8:21 PM
# @File   : config.py
import logging.config
logging.config.fileConfig("logger.conf")
logger = logging.getLogger("get-latest-novel")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.23 Safari/537.36"
}

baseOriginUrl = 'https://www.biqiuge.com'

updatePostUrl = 'http://35.234.33.9/api/novelupdate'