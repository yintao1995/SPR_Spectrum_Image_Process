import sys
import time
from gui_design import *
from spr_data_read import visual_data, read_data
from hue_of_image import draw_image, hue_of_image
import matplotlib.pyplot as plt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QProgressDialog
import json
from image_viewer import ImageWidget

class MyMainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.lineEdit_1.setFixedSize(40, 20)
        self.lineEdit_2.setFixedSize(40, 20)
        self.lineEdit_3.setFixedSize(40, 20)
        self.lineEdit_4.setFixedSize(40, 20)
        # self.pushButton_1.setMaximumWidth(200)
        self.pushButton_4.setFixedSize(35,55)
        self.pushButton_7.setMaximumWidth(40)
        self.lineEdit_8.setMaximumWidth(70)
        self.lineEdit_9.setMaximumWidth(70)
        self.checkBox_1.setChecked(True)


       #这里面可以继续对控件进行操作
        self.pushButton_0.clicked.connect(self.choose_files)
        self.textEdit.textChanged.connect(self.func100)
        self.pushButton_1.clicked.connect(self.func_1)
        self.pushButton_2.clicked.connect(self.func_2)
        self.pushButton_3.clicked.connect(self.func_3)
        self.pushButton_4.clicked.connect(self.func_4)
        self.pushButton_5.clicked.connect(self.func_5)
        self.pushButton_6.clicked.connect(self.func_6)
        self.pushButton_7.clicked.connect(self.func_7)

    def choose_files(self):
        files = QFileDialog.getOpenFileNames(self, 'Choose files', '', "*", None, QFileDialog.DontUseNativeDialog)
        # print(type(files)) # tuple
        filename_list = files[0]
        if not filename_list:
            return
        print(filename_list)
        self.textEdit.clear()
        name_list = []
        for filename in filename_list:
            self.textEdit.append(filename)
            name_list.append(filename.split('/')[-1])
        self.textEdit.append('\n')
        # with open('filename.json', 'w') as file_obj:    #文件名依次存入文件
        #     json.dump(name_list, file_obj)
        self.lineEdit_5.setText(str(name_list))

    def func_1(self):  # 呈现方式：一个光谱一张图（包括一个光谱和多个光谱）
        filename_list = self.textEdit.toPlainText().strip().split('\n')  # 将文本框内容转换成列表，其中每个元素都是一个完整的路径
        try:
            resonance_wavelength_list = []
            for filename in filename_list:
                if not filename:
                    continue
                data = visual_data(read_data(filename, '\t'))
                fig = plt.figure()
                plt.plot(data[0], data[1])
                plt.axvline(data[2], c='red', alpha=0.5)
                plt.text(500, 0.2, "resonance wavelength=" + str(data[2]) + "nm")
                resonance_wavelength_list.append(data[2])
                label = []
                label.append(filename.split('/')[-1])
                plt.legend(label)
            # with open('wavelength.json', 'w') as file_obj:
            #     json.dump(resonance_wavelength_list, file_obj)
            if resonance_wavelength_list:   #有文件存在才显示，不然画空白图
                self.lineEdit_6.setText(str(resonance_wavelength_list))
                plt.show()
            # QMessageBox.information(self, 'Done', 'Process Done')
        except:
            pass

    def func_2(self): # 呈现方式：多个光谱在同一张图，图例中显示颜色对应与各光谱的共振波长
        filename_list = self.textEdit.toPlainText().strip().split('\n')
        file_existing_flag = 0
        self.lineEdit_6.clear()
        try:
            label = []
            resonance_wavelength_list = []
            for filename in filename_list:
                if not filename:
                    continue
                print(filename)
                data = visual_data(read_data(filename, '\t'))
                resonance_wavelength_list.append(data[2])
                if not self.checkBox_1.isChecked():
                    plt.plot(data[0], data[1] )
                    plt.scatter(data[2], data[3], s=5)
                    label.append(filename.split('/')[-1] + "[" + ("%.2f" % data[2]) + "nm]")
                file_existing_flag =1
            # with open('wavelength.json', 'w') as file_obj:
            #     json.dump(resonance_wavelength_list, file_obj)
            if resonance_wavelength_list:
                self.lineEdit_6.setText(str(resonance_wavelength_list))
                QMessageBox.information(self,'Done','Process Done')
                if not self.checkBox_1.isChecked():
                    plt.legend(label)
                    plt.show()
                
        except:
            pass

    def func_3(self):   # 单个图像的二维色相以及平均色相值（显示在图的标题）
        filename_list = self.textEdit.toPlainText().strip().split('\n')
        self.lineEdit_7.clear()
        try:
            average_hue_list = []
            x1 = int(self.lineEdit_1.text())
            x2 = int(self.lineEdit_2.text())
            x3 = int(self.lineEdit_3.text())
            x4 = int(self.lineEdit_4.text())
            n = len(filename_list)
            progressdialog = QProgressDialog(self)
            progressdialog.setWindowTitle('Please wait')
            progressdialog.setWindowModality(Qt.WindowModal)
            progressdialog.setLabelText('processing...')
            progressdialog.setRange(0, n)
            progressdialog.show()
            i = 0
            for filename in filename_list:
                i = i+1
                progressdialog.setValue(i)
                if x1+x2+x3+x4==0:
                    data = hue_of_image(filename)
                else:
                    data = hue_of_image(filename, x1, x2, x3, x4)
                if not self.checkBox_1.isChecked():
                    draw_image(filename.split('/')[-1], data[0], data[1])
                average_hue_list.append(data[0])
            # with open('average_hue.json', 'w') as file_obj:
            #     json.dump(average_hue_list, file_obj)
            self.lineEdit_7.setText(str(average_hue_list))
            # print(self.lineEdit_7.text(), type(self.lineEdit_7.text()))
            QMessageBox.information(self, 'Done', 'Process Done')

            if not self.checkBox_1.isChecked():
                plt.show()
            
        except:
            pass

    def func_4(self):   #   绘制共振波长-色相曲线图
        try:
            a = [float(i) for i in self.lineEdit_6.text()[1:-1].split(',')]
            b = [float(i) for i in self.lineEdit_7.text()[1:-1].split(',')]
            if len(a)!=len(b):
                QMessageBox.warning(self,"警告","两个列表数量不相等")
            fig = plt.figure()
            plt.title("wavelength-hue")
            plt.plot(a, b)
            plt.show()
        except:
            pass

    def func_5(self):   # 色相随时间变化关系，需要设置采样时间间隔(单位：秒s)
        try:
            interval = float(self.lineEdit_8.text())
            b = [float(i) for i in self.lineEdit_7.text()[1:-1].split(',')]
            t = [i*interval for i in range(len(b))]
            fig = plt.figure()
            plt.title("Hue values vary with time")
            plt.plot(t, b)
            plt.ylabel("Hue")
            plt.xlabel("Time/s")
            plt.show()
        except:
            pass

    def func_6(self):   # 共振波长随时间变化关系，需要设置采样时间间隔(单位：秒s)
        try:
            interval = float(self.lineEdit_9.text())
            b = [float(i) for i in self.lineEdit_6.text()[1:-1].split(',')]
            t = [i*interval for i in range(len(b))]
            fig = plt.figure()
            plt.title("Resonance wavelength varies with time")
            plt.plot(t, b)
            plt.ylabel('$\lambda$/nm')
            plt.xlabel("Time/s")
            plt.show()
        except:
            pass

    def func_7(self): # 点击view按钮打开图像视察器，通过它可以选择选区并将选区参数传回主窗口
        image_viewer_widget = ImageWidget()
        image_viewer_widget.setAttribute(Qt.WA_DeleteOnClose)
        image_viewer_widget.show()
        image_viewer_widget.mySignal.connect(lambda : self.func_8(image_viewer_widget))

    def func_8(self,image_viewer_widget):
        try:
            size_data=image_viewer_widget.transmit_selection()
            self.lineEdit_1.setText(str(size_data[0]))
            self.lineEdit_2.setText(str(size_data[1]))
            self.lineEdit_3.setText(str(size_data[2]))
            self.lineEdit_4.setText(str(size_data[3]))
        except:
            pass

    def func100(self):  # 拖拽文件到文本框时，会以'file:///'开头显示文件路径，此函数将此前缀删除
        # print(self.textEdit.toPlainText())
        if self.textEdit.toPlainText().find('file:///')!=-1:
            self.textEdit.setText(self.textEdit.toPlainText().replace('file:///','')+'\n')



if __name__=='__main__':
    app = QApplication(sys.argv)
    mw = MyMainWindow()
    mw.show()
    sys.exit(app.exec_())
