
import itchat
if __name__ == "__main__":
    itchat.auto_login(hotReload=True)  # 扫码自动登陆

    itchat.send(u'你好，文件传输助手', 'filehelper')

    itchat.send(u' 使用python测试消息', '@619ae4625f3ef39e7fd65a0456a3bc87')