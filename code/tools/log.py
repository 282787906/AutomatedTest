debug = 1
info = 2
warming = 4

logLevel = debug|info | warming


def e(*str):
    print('\033[31;0m', str, '\033[0m')


def w(*str):
    if logLevel & warming == warming:
        print('\033[33;0m', str, '\033[0m')


def i(*str):
    if logLevel & info == info:
        print('\033[32;0m', str, '\033[0m')


def d(*str):
    if logLevel & debug == debug:
        print('\033[37;0m', str, '\033[0m')


if __name__ == "__main__":
    # for i in range(30, 48):
    #     print("{} \033[{};1mhello\033[0m".format(i, str(i)))

    e('exception', 'msg')
    w('warming', 'msg')
    i('info', 'msg')
    d('debug', 'msg')
