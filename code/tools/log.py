import ctypes
import inspect
import os
import traceback
import winsound
from datetime import datetime
import sys

from conf import config

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色
# 由于该函数的限制，应该是只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合，组合后还是在这16种颜色中

# Windows CMD命令行 字体颜色定义 text colors
FOREGROUND_BLACK = 0x00  # black.
FOREGROUND_DARKBLUE = 0x01  # dark blue.
FOREGROUND_DARKGREEN = 0x02  # dark green.
FOREGROUND_DARKSKYBLUE = 0x03  # dark skyblue.
FOREGROUND_DARKRED = 0x04  # dark red.
FOREGROUND_DARKPINK = 0x05  # dark pink.
FOREGROUND_DARKYELLOW = 0x06  # dark yellow.
FOREGROUND_DARKWHITE = 0x07  # dark white.
FOREGROUND_DARKGRAY = 0x08  # dark gray.
FOREGROUND_BLUE = 0x09  # blue.
FOREGROUND_GREEN = 0x0a  # green.
FOREGROUND_SKYBLUE = 0x0b  # skyblue.
FOREGROUND_RED = 0x0c  # red.
FOREGROUND_PINK = 0x0d  # pink.
FOREGROUND_YELLOW = 0x0e  # yellow.
FOREGROUND_WHITE = 0x0f  # white.

# Windows CMD命令行 背景颜色定义 background colors
BACKGROUND_BLUE = 0x10  # dark blue.
BACKGROUND_GREEN = 0x20  # dark green.
BACKGROUND_DARKSKYBLUE = 0x30  # dark skyblue.
BACKGROUND_DARKRED = 0x40  # dark red.
BACKGROUND_DARKPINK = 0x50  # dark pink.
BACKGROUND_DARKYELLOW = 0x60  # dark yellow.
BACKGROUND_DARKWHITE = 0x70  # dark white.
BACKGROUND_DARKGRAY = 0x80  # dark gray.
BACKGROUND_BLUE = 0x90  # blue.
BACKGROUND_GREEN = 0xa0  # green.
BACKGROUND_SKYBLUE = 0xb0  # skyblue.
BACKGROUND_RED = 0xc0  # red.
BACKGROUND_PINK = 0xd0  # pink.
BACKGROUND_YELLOW = 0xe0  # yellow.
BACKGROUND_WHITE = 0xf0  # white.

debug = 1
info = 2
warming = 4

logLevel = debug | info | warming

# dateFormat = "%Y-%m-%d  %H:%M:%S"
# dateFormat = "%H:%M:%S"
# if config.runWith == config.RUN_WITH_CMD:
#     dateFormat = "%Y-%m-%d  %H:%M:%S"


def exception(*strs):
    if config.runWith == config.RUN_WITH_CMD:
        winsound.Beep(1000,500)

    e(strs)
    et, ev, tb = sys.exc_info()
    if et==None and ev ==None and tb==None:
        if config.runWith==config.RUN_WITH_PYCHARM:
            print('\033[31m' + '无异常信息' + '\033[0m')
        elif config.runWith==config.RUN_WITH_CMD:
            set_cmd_text_color(FOREGROUND_RED)
            sys.stdout.write('无异常信息' + '\n')
            resetColor()
        else:
            print('无异常信息')
    msgs = traceback.format_exception(et, ev, tb)
    msg=''
    for m in msgs:
        # e(m.strip('\n'))
        if config.runWith==config.RUN_WITH_PYCHARM:
            print('\033[31m' + m.strip('\n') + '\033[0m')
        elif config.runWith == config.RUN_WITH_CMD:
            set_cmd_text_color(FOREGROUND_RED)
            sys.stdout.write(m.strip('\n') + '\n')
            resetColor()
        else:
            print(m.strip('\n')+ '\n')
        msg =msg+ m.strip('\n')+ '\n'
    return msg


def e(*strs):
    if config.runWith == config.RUN_WITH_CMD:
        winsound.Beep(1000,500)

    msgs = datetime.now().strftime(config.dateFormat) + ' '
    for msg in strs:
        msgs = msgs + ' ' + str(msg)
    if config.runWith==config.RUN_WITH_PYCHARM:
        print('\033[31m' + msgs + '\033[0m')
    elif config.runWith == config.RUN_WITH_CMD:
        set_cmd_text_color(FOREGROUND_RED)
        sys.stdout.write(msgs + '\n')
        resetColor()
    else:
        print(strs)


def w(*strs):
    if config.runWith == config.RUN_WITH_CMD:
        winsound.Beep(800,300)
    msgs = datetime.now().strftime(config.dateFormat) + ' '
    for msg in strs:
        msgs = msgs + ' ' + str(msg)
    if logLevel & warming == warming:
        if config.runWith==config.RUN_WITH_PYCHARM:
            print('\033[33m' + msgs + '\033[0m')
        elif config.runWith == config.RUN_WITH_CMD:
            set_cmd_text_color(FOREGROUND_YELLOW)
            sys.stdout.write(msgs + '\n')
            resetColor()
        else:
            print(strs)

def i(*strs):
    msgs = datetime.now().strftime(config.dateFormat) + ' '
    for msg in strs:
        msgs = msgs + ' ' + str(msg)
    if logLevel & info == info:
        if config.runWith==config.RUN_WITH_PYCHARM:
            print('\033[34m' + msgs + '\033[0m')
        elif config.runWith == config.RUN_WITH_CMD:
            set_cmd_text_color(FOREGROUND_GREEN)
            sys.stdout.write(msgs + '\n')
            resetColor()
        else:
            print(strs)


def d(*strs):
    msgs = datetime.now().strftime(config.dateFormat) + ' '
    for msg in strs:
        msgs = msgs + ' ' + str(msg)
    if logLevel & debug == debug:
        if config.runWith==config.RUN_WITH_PYCHARM:
            print('\033[37m' + msgs + '\033[0m')
        elif config.runWith == config.RUN_WITH_CMD:
            set_cmd_text_color(FOREGROUND_DARKGRAY)
            sys.stdout.write(msgs + '\n')
            resetColor()
        else:
            print(strs)

# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool


# reset white
def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)


if __name__ == "__main__":
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))
    # print('Argument List:', str(sys.argv))
    # print(sys.argv[1])

    print('默认')
    e('exception', '异常')
    w('warming', '警告')
    i('info', '信息')
    d('debug', '调试')