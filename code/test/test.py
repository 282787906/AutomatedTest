import os
import shutil

from selenium import webdriver
from HTMLTestRunner import HTMLTestRunner  # 导入HTMLTestRunner模块
import unittest, time

from conf import config

if __name__ == "__main__":
    shutil.rmtree(config.FILE_DOWNLOAD)
    os.mkdir(config.FILE_DOWNLOAD)