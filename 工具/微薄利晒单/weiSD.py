# 微薄利一键晒单

# 参考资料：https://www.cnblogs.com/danvy/p/11721087.html


from PIL import ImageGrab


pic = ImageGrab.grab()
# print(pic.size)
pic.save(r'E:\SVN\BeiJing-WanBaoKuangChan\05_测试\pic.jpg')