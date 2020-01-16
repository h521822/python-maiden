# 知识盲点：
## 使用webdriver的元素定位不熟练
## webdriver获取元素信息
```
# 获取元素标签的内容：
print(logo.get_attribute('textContent'))
# 获取元素内的全部HTML：
print(logo.get_attribute('innerHTML'))
# 获取包含选中元素的HTML：
print(logo.get_attribute('outerHTML'))

```

## 使用`AutoIt v3`做文件上传(第一次)
参考:
1、https://www.cnblogs.com/FR-Long/p/7239919.html

2、https://www.cnblogs.com/yaoze2018/p/10816129.html

3、https://www.cnblogs.com/caoj/p/7815835.html


### 固定文件路径,意义不大,用于测试
```
;ControlFocus()方法用于识别Window窗口
ControlFocus("打开","","Edit1");

; WinWait()设置10秒钟用于等待窗口的显示
WinWait("[CLASS:#32770]","",10)

; ControlSetText()用于向“文件名”输入框内输入本地文件的路径，如果是在桌面第三个参数直接写文件名
ControlSetText("打开","","Edit1","D:\yongzhou.jpg");
Sleep(2000);

; ControlClick()用于点击上传窗口中的“打开”按钮
ControlClick("打开","","Button1");


```

```
# python调用
os.system(r"C:\D:\222222.exe")

```

### 动态文件路径
```

;ControlFocus()方法用于识别Window窗口
ControlFocus("打开","","Edit1");

; WinWait()设置10秒钟用于等待窗口的显示
WinWait("[CLASS:#32770]","",10)

; ControlSetText()用于向“文件名”输入框内输入本地文件的路径，如果是在桌面第三个参数直接写文件名
ControlSetText("打开","","Edit1",$CmdLine[1]);
Sleep(2000);

; ControlClick()用于点击上传窗口中的“打开”按钮
ControlClick("打开","","Button1");

```

```
# 需上传图片的路径
file_path = "D:\\1.png"

# 执行autoit上传文件
os.system("C:\\Users\Gloria\Desktop\cmdjpg.exe %s" % file_path)  # 你自己本地的
```

## 浏览器窗口切换
参考：https://www.bbsmax.com/A/gAJG9DXodZ/

```
# 打开最后一个窗口(参数从0开始)
self.browser.switch_to.window(self.browser.window_handles[-1])
print(self.browser.title) 
```

## 打开浏览器新窗口
方法一：
```
# 新开一个窗口，通过执行js来新开一个窗口
# js='window.open("http://www.baidu.com");'
self.browser.execute_script('window.open("http://www.baidu.com");')
```

方法二：
```

import win32api, win32con  # 安装 pywin32或者pypiwin32

VK_CODE ={'ctrl':0x11, 't':0x54, 'tab':0x09}

# 键盘键按下
def keyDown(keyName):
    win32api.keybd_event(VK_CODE[keyName], 0, 0, 0)
# 键盘键抬起
def keyUp(keyName):
    win32api.keybd_event(VK_CODE[keyName], 0, win32con.KEYEVENTF_KEYUP, 0)

# 封装的按键方法
def simulateKey(firstKey, secondKey):
    keyDown(firstKey)
    keyDown(secondKey)
    keyUp(secondKey)
    keyUp(firstKey)



# 开个新的标签页
simulateKey("ctrl", "t")

```

## 安装 pywin32 教程
参考：
1、https://www.cnblogs.com/yjlch1016/p/8469429.html

2、https://github.com/mhammond/pywin32/