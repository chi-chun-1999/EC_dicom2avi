from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
import sys, time

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
Form.setWindowTitle('oxxo.studio')
Form.resize(300, 200)

pushbutton = QtWidgets.QPushButton(Form)
pushbutton.setText('Button')


def a():
    
    data_a = 0
    for i in range(0,5):
        data_a+=1
        # label_a.setText(str(i))
        print('A:',i)
        time.sleep(0.5)
    
    return data_a

def b():
    data_b = 0
    for i in range(0,50,5):
        data_b+=1
        # label_b.setText(str(i))
        print('B:',i)
        time.sleep(0.3)
    
    return data_b


def c(data_a,data_b):
    
    thread_a.wait()
    thread_b.wait()
    
    data_c = data_a+data_c
    for i in range(0,50,5):
        data_c+=1
        print('B:',data_c)
        time.sleep(0.2)
    
    return data_c

    


def press():
    print('button')

pushbutton.clicked.connect(press)
print('-----hello----')
thread_a = QThread()   # 建立 Thread()
thread_a.run = a       # 設定該執行緒執行 a()
thread_a.start()       # 啟動執行緒

thread_b = QThread()   # 建立 Thread()
thread_b.run = b       # 設定該執行緒執行 b()
thread_b.start()       # 啟動執行緒

thread_c = QThread(c)   # 建立 Thread()
thread_c.run = c       # 設定該執行緒執行 c()
thread_c.start()       # 啟動執行緒


Form.show()
sys.exit(app.exec_())
