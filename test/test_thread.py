from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QThread,pyqtSignal,pyqtSlot
import sys, time

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
Form.setWindowTitle('oxxo.studio')
Form.resize(300, 200)

pushbutton = QtWidgets.QPushButton(Form)
pushbutton.setText('Button')


class ProcessThread(QtCore.QThread):
    outcome_value = pyqtSignal(int)
    def __init__(self,start_value=0,end_value=5,step=1,sleep_time = 0.3,parent=None):
        QtCore.QThread.__init__(self, parent)
        self._start_value = start_value
        self._end_value = end_value
        self._step = step
        self._sleep_time = sleep_time
    
    def run(self):
        outcome = 0
        for i in range(self._start_value,self._end_value,self._step):
            outcome+=i
            print(i)
            time.sleep(self._sleep_time)

            
        self.outcome_value.emit(outcome)


class MergeThread(QtCore.QThread):
    def __init__(self,a_thread,b_thread,parent=None):
        QtCore.QThread.__init__(self, parent)
        self._all_sum = 0
        self._a_thread = a_thread
        self._b_thread = b_thread
    
    def run(self):
        self._a_thread.wait()
        self._b_thread.wait()
        
        data_c = self._a_data+self._b_data
        
        for i in range(0,10):
            data_c+=i
        
        print('outcome c: ',data_c)
            
        
    @pyqtSlot(int)
    def getA(self,value):
        print('a outcome value: ',value)
        self._a_data = value
        return 

    @pyqtSlot(int)
    def getB(self,value):
        print('b outcome value: ',value)
        self._b_data = value
        return

    

def press():
    print('button')


pushbutton.clicked.connect(press)
print('-----hello----')



thread_a = ProcessThread()   # 建立 Thread()
thread_b = ProcessThread(0,50,5,0.5)   # 建立 Thread()

thread_c = MergeThread(thread_a,thread_b)

thread_a.outcome_value.connect(thread_c.getA)
thread_b.outcome_value.connect(thread_c.getB)
# thread_a.run = a       # 設定該執行緒執行 a()
thread_a.start()       # 啟動執行緒
thread_b.start()       # 啟動執行緒
thread_c.start()


# thread_c = QThread(c)   # 建立 Thread()
# thread_c.run = c       # 設定該執行緒執行 c()
# thread_c.start()       # 啟動執行緒


Form.show()
sys.exit(app.exec_())
