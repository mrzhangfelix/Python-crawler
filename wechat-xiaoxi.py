import pyautogui
import time
import win32api
import win32con
import win32gui
import win32clipboard as w

def FindWindow(chatroom):
    win = win32gui.FindWindow('WeChatMainWndForPC',chatroom)
    print('正在启动微信')
    print('-----------------')
    if win != 0:
        win32gui.ShowWindow(win, win32con.SW_SHOWMINIMIZED)
        win32gui.ShowWindow(win, win32con.SW_SHOWNORMAL)
        win32gui.ShowWindow(win, win32con.SW_SHOW)
        win32gui.SetWindowPos(win, win32con.HWND_TOP, 0, 0, 500, 700, win32con.SWP_SHOWWINDOW)
        win32gui.SetForegroundWindow(win)  # 获取控制
        time.sleep(1)
        tit = win32gui.GetWindowText(win)
        print('已启动【'+str(tit)+'】窗口')
        print('-----------------')
    else:
        print('找不到【%s】窗口' % chatroom)
        print('-----------------')
        exit()

# 设置和粘贴剪贴板
def ClipboardText(ClipboardText):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, ClipboardText)
    w.CloseClipboard()
    time.sleep(1)
    win32api.keybd_event(17,0,0,0)
    win32api.keybd_event(86,0,0,0)
    win32api.keybd_event(86,0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)

# 模拟发送动作
def SendMsg():
    win32api.keybd_event(18, 0, 0, 0)
    win32api.keybd_event(83,0,0,0)
    win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0)

# 模拟发送微信文本消息
def SendWxMsg(wxid,sendtext):
    # 先启动微信
    FindWindow('微信')
    time.sleep(1)
    # 定位到搜索框
    pyautogui.moveTo(143, 39)
    pyautogui.click()
    # 搜索微信
    ClipboardText(wxid)
    time.sleep(1)
    # 进入聊天窗口
    pyautogui.moveTo(155, 120)
    pyautogui.click()
    # 粘贴文本内容
    ClipboardText(sendtext)
    # 发送
    SendMsg()
    print('已发送')
    # 关闭微信窗口
    time.sleep(1)
    pyautogui.moveTo(683, 16)
    pyautogui.click()

# 打开控制台运行
print('欢迎使用Python自动发微信脚本')
print('---------------------')
print('正在启动中...')
print('已启动')
print('---------------------')

# WxMsg = input('你要发送的内容是：')
WxMsg = "ceshi"
print('---------------------')
# ToWx = input('你要发送给谁（填微信号）：')
ToWx = "mataopuge"
print('---------------------')
# yanshi = input('延迟多少秒发送（单位/秒，无需填写单位，只需填写数字）：')
yanshi = 3
print('---------------------')
print('倒计时中...')
print('---------------------')

# 延时发送
time.sleep(int(yanshi))

# 执行发送动作
SendWxMsg(ToWx,WxMsg)