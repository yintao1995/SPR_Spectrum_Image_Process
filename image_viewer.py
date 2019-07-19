from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QApplication,QPushButton,QProgressDialog,QHBoxLayout, QLineEdit, QVBoxLayout, QLabel,QScrollArea
import sys
import math
from PIL import Image
import qtawesome as qta


class ImageWidget(QWidget):
    mySignal = pyqtSignal()
    def __init__(self,parent=None):
        super(ImageWidget, self).__init__(parent)
        self.resize(400,300)
        self.setWindowTitle("Image Viewer")
        self.setWindowIcon(qta.icon('fa5.eye', color='gray'))
        self.x0=10
        self.y0=20
        self.w=30
        self.h=40


        pushbutton0 = QPushButton("Open Img")
        pushbutton1 = QPushButton("Zoom In")
        pct_lineedit = QLineEdit()
        pushbutton2 = QPushButton("Zoom Out")

        pushbutton0.setMaximumSize(80, 50)
        pushbutton1.setMaximumSize(80, 50)
        pct_lineedit.setMaximumSize(80, 50)
        pushbutton2.setMaximumSize(80, 50)
        ## 左侧栏布局
        vlayout_52_left = QVBoxLayout()
        vlayout_52_left.addSpacing(10)
        vlayout_52_left.addWidget(pushbutton0)
        vlayout_52_left.addStretch(1)
        vlayout_52_left.addWidget(pushbutton1)
        vlayout_52_left.addWidget(pct_lineedit)
        vlayout_52_left.addWidget(pushbutton2)
        vlayout_52_left.addStretch(1)
        vlayout_52_left.addSpacing(10)

        # 右侧布局
        edit1 = QLineEdit('0')
        edit2 = QLineEdit('0')
        edit3 = QLineEdit('0')
        edit4 = QLineEdit('0')
        edit1.setAlignment(Qt.AlignCenter)
        edit2.setAlignment(Qt.AlignCenter)
        edit3.setAlignment(Qt.AlignCenter)
        edit4.setAlignment(Qt.AlignCenter)
        select_bt = QPushButton('Select')
        cancel_bt = QPushButton('Cancel')

        # 右上角布局
        hlayout_52_rt = QHBoxLayout()
        hlayout_52_rt.addStretch(3)
        hlayout_52_rt.addWidget(edit1, stretch=1)
        hlayout_52_rt.addWidget(edit2, stretch=1)
        hlayout_52_rt.addWidget(edit3, stretch=1)
        hlayout_52_rt.addWidget(edit4, stretch=1)
        hlayout_52_rt.addWidget(select_bt, stretch=1)
        hlayout_52_rt.addWidget(cancel_bt, stretch=1)
        hlayout_52_rt.addStretch(3)

        label0 = MyLabel()
        # label0.setStyleSheet("border:2px solid grey;")
        # pixmap = QPixmap()
        image_scroll_area = myWidgetScrollArea()
        image_scroll_area.setMinimumSize(600, 480)
        # image_scroll_area.setFixedSize(800,600)
        image_scroll_area.setWidget(label0)
        image_scroll_area.setAlignment(Qt.AlignCenter)
        # print(image_scroll_area.width()," -- ",image_scroll_area.height())

        # 右侧布局
        vlayout_52_right = QVBoxLayout()
        vlayout_52_right.addLayout(hlayout_52_rt)
        vlayout_52_right.addWidget(image_scroll_area)
        # 整体布局(参数为窗口)
        hlayout52_total = QHBoxLayout(self)
        hlayout52_total.addLayout(vlayout_52_left)
        hlayout52_total.addLayout(vlayout_52_right)

        # 按钮信号连接
        pushbutton0.clicked.connect(lambda: self.open_img(label0, cancel_bt, image_scroll_area, pct_lineedit))
        pushbutton1.clicked.connect(lambda: self.zoom_in(label0, select_bt, image_scroll_area, pct_lineedit))
        pushbutton2.clicked.connect(lambda: self.zoom_out(label0, select_bt, image_scroll_area, pct_lineedit))

        select_bt.clicked.connect(lambda: self.selection_functon(label0, edit1, edit2, edit3, edit4, 1))
        cancel_bt.clicked.connect(lambda: self.selection_functon(label0, edit1, edit2, edit3, edit4, 0))

        label0.mySignal1.connect(lambda: self.set_size(label0, edit1, edit2, edit3, edit4))

    def set_size(self, label, edit1, edit2, edit3, edit4):  # 将鼠标选择的区域显示在框里
        # print('yeaaaaaaaaaaahhhhh')
        new_x = label.x0  # 根据鼠标滑动的四种方向，重新矫正选框左上角的坐标
        new_y = label.y0
        if label.w < 0:
            new_x = label.x0 + label.w
        if label.h < 0:
            new_y = label.y0 + label.h
        edit1.setText(str(int(new_x / label.ratio)))
        edit2.setText(str(int(new_y / label.ratio)))
        edit3.setText(str(abs(int(label.w / label.ratio))))  # 绝对值,比例
        edit4.setText(str(abs(int(label.h / label.ratio))))


    def selection_functon(self, label, edit1, edit2, edit3, edit4, flag):
        # painEvent不能传递参数，因此通过改变label属性来传递参数
        # 四个参数分别为：选区左上角的(x,y)以及选区的宽和高度
        #
        # 【注意】：我们看到的尺寸是标签大小label.width()，而实际尺寸是
        #                   图像大小label.pixmap().width()，这二者存在缩放比的关系
        #                   作画时，是在标签上作画，因此显示的矩形框应与实际的尺寸存在缩放比计算
        #                   这样才能保证缩放过程中选框选的是同一位置
        #                   在参数传递过程中，应完成此缩放比计算
        #                   但是在实际操作中，如裁剪、计算选区色相，由于是从源图片上操作的，所以对输入参数不需要变换
        try:
            w1 = label.width()
            w2 = label.pixmap().width()
            ratio = w1 / w2
            x = [int(edit1.text()), int(edit2.text()), int(edit3.text()), int(edit4.text())]
            self.x0 = x[0]
            self.y0 = x[1]
            self.w = x[2]
            self.h = x[3]
            self.mySignal.emit()

            x = [a * ratio for a in x]
            if flag:
                label.x0 = x[0]
                label.y0 = x[1]
                label.w = x[2]
                label.h = x[3]
                self.mySignal.emit()
            else:
                label.x0 = 0
                label.y0 = 0
                label.w = 0
                label.h = 0
                edit1.setText('0')
                edit2.setText('0')
                edit3.setText('0')
                edit4.setText('0')
            label.repaint() # 更新窗口，以使得新的paintevent触发
        except:
            pass

    def transmit_selection(self):
        return self.x0,self.y0,self.w,self.h


    def open_img(self, label, button, scroll_area, lineedit):
        filename = QFileDialog.getOpenFileName(self, "Open file", '',
                                               "Images(*.png *.jpg *.bmp)", None, QFileDialog.DontUseNativeDialog)
        if not filename[0]:
            return
        print(filename[0])
        # settings=QSettings('./Setting.ini',QSettings.IniFormat)
        # settings.setValue('saa',filename[0])

        pixmap = QPixmap(filename[0])
        w1 = pixmap.width()
        h1 = pixmap.height()
        w2 = scroll_area.width()
        h2 = scroll_area.height()
        print(w1, " -- ", h1)
        print(w2, " -- ", h2)
        # label.resize(pixmap.width(),pixmap.height())
        fit_size = self.fit_image(w1, h1, w2, h2)
        label.resize(fit_size[0], fit_size[1])  # 这里把label的尺寸设置为和
        # 图片一样的宽高比并且自适应于滚动区域的大小
        label.setPixmap(pixmap)
        # label.setStyleSheet("background-image:url(filename[0])")
        label.ratio = fit_size[0] / w1
        print("加载图片相对于原始尺寸时的缩放比例:", label.ratio)
        lineedit.setText(str(math.floor(100 * label.ratio)) + "%")
        label.setToolTip(filename[0])  # 将图片路径作为标签的tooltip内容，以便后续操作
        label.setScaledContents(True)

        button.click()  # 新打开一张图片时调用cancel_bt将label上的矩形框清除


    def zoom_in(self, label, button, scroll_area, lineedit):  # 放大
        print("zoom in + clicked")
        if not label.pixmap():
            print('no image')
            return
        zoomin_factor = 1.1
        new_width = label.width() * zoomin_factor
        new_height = label.height() * zoomin_factor
        if new_width < 5 * label.pixmap().width() and new_width < 5000 and new_height < 5000:
            label.resize(new_width, new_height)
            # print(new_width,new_height)
            label.ratio = new_width / label.pixmap().width()
            lineedit.setText(str(math.floor(100 * label.ratio)) + "%")

        scroll_area.setAlignment(Qt.AlignCenter)
        scroll_area.setWidgetResizable(False)  # 不加这一句的话，可能放大的时候不会出现滚动条
        label.setScaledContents(True)
        button.click()  # 缩放过程中保持矩形选框的一致性

    def zoom_out(self, label, button, scroll_area, lineedit):  # 缩小
        print("zoom out - clicked")
        if not label.pixmap():
            print('no image')
            return
        zoomout_factor = 0.90
        new_width = label.width() * zoomout_factor
        new_height = label.height() * zoomout_factor
        label.resize(new_width, new_height)
        label.ratio = new_width / label.pixmap().width()
        lineedit.setText(str(math.floor(100 * label.ratio)) + "%")

        scroll_area.setAlignment(Qt.AlignCenter)
        scroll_area.setWidgetResizable(False)
        label.setScaledContents(True)
        button.click()

    def fit_image(self, w1, h1, w2, h2):  # 加载图片的时候自适应滚动区域的大小
        if w1 < w2 and h1 < h2:
            return (w1, h1)
        else:  # 剩余三种情况，可以划分为两类
            if w1 * h2 > h1 * w2:  # 宽的比例更大，则以此比例作为缩放标准
                ratio = (w1 / w2)
            else:  # 否则高的比例更大，则以高的比例为标准
                ratio = (h1 / h2)
            print("加载时为缩小到滚动区域的比例为：", ratio)
            ratio = ratio * 1.03  # 这个因子是让图片与边框之间留点缝隙
            return (math.floor(w1 / ratio), math.floor(h1 / ratio))


class MyLabel(QLabel):
    mySignal1 = pyqtSignal()
    def __init__(self):
        super(MyLabel, self).__init__()
        self.x0 = 0 # 要划矩形框的参数
        self.y0 = 0
        self.w = 0
        self.h = 0

        self.press_flag=False #判断在label上的鼠标按下后是否抬起，按下置为True，抬起置为False

        self.ratio=1 #label相对于图像原始尺寸的缩放比例
        # 自定义Label，额外添加四个属性，分别为要设置选区的左上角(x0,y0)和选区宽、高

        self.mouse_position=(0,0) # 用来指示当前鼠标（右键）点击的地方相对label的位置
    def paintEvent(self, event):
        super(MyLabel,self).paintEvent(event)
        painter=QPainter(self)
        # painter.begin(self)
        painter.setPen(QPen(Qt.yellow,2,Qt.DashLine))
        print('--paintevent function triggered--')
        print(QRect(self.x0,self.y0,self.w,self.h))
        painter.drawRect(QRect(self.x0,self.y0,self.w,self.h))
        # paintEvent似乎不允许传递自定义参数？因此通过调用MyLabel属性来实现参数传递
    def mousePressEvent(self, event):
        # print(self.pos()) # label左上角的位置
        self.press_flag=True
        x=event.x()
        y=event.y()
        # if event.button()==Qt.RightButton: #右键点击显示当前鼠标相对于label的位置
        self.x0=x
        self.y0=y
        self.mouse_position=(round(x/self.ratio),round(y/self.ratio))
        print("鼠标在图像中的实际位置：",self.mouse_position)
    def mouseReleaseEvent(self, event):
        self.press_flag=False #抬起则置为false
    def mouseMoveEvent(self, event): #限制鼠标在label内，超出无效
        if self.press_flag:
            x = event.x()
            y = event.y()
            if x>=0 and x<=self.width():
                self.w = x - self.x0
            if y>=0 and y<=self.height():
                self.h=y-self.y0
            self.mySignal1.emit()
            self.update()


class myWidgetScrollArea(QScrollArea):
    def __init__(self):
        print("---my widgetscrollarea checked---")
        super().__init__()

        self.last_time_move_x = 0
        self.last_time_move_y = 0

        self.scrollBarX = self.horizontalScrollBar()
        self.scrollBarY = self.verticalScrollBar()

    def eventFilter(self, QObject, QEvent):

        if QEvent.type() == QEvent.MouseMove and QEvent.button()==Qt.RightButton:
            #后半句有些问题，去掉后半句，则可用鼠标拖动滚动区域
            if self.last_time_move_x == 0:
                self.last_time_move_x = QEvent.pos().x()

            if self.last_time_move_y == 0:
                self.last_time_move_y = QEvent.pos().y()

            distance_x = self.last_time_move_x - QEvent.pos().x()
            distance_y = self.last_time_move_y - QEvent.pos().y()

            # print(self.last_time_move_y, QEvent.pos().y(), distance_y, self.scrollBarY.value())
            self.scrollBarX.setValue(self.scrollBarX.value() + distance_x)
            self.scrollBarY.setValue(self.scrollBarY.value() + distance_y)

        elif QEvent.type() == QEvent.MouseButtonRelease:
            self.last_time_move_x = self.last_time_move_y = 0

        return QWidget.eventFilter(self, QObject, QEvent)

    def mousePressEvent(self, event):
        # print(self.pos()) # l滚动区域左上角的位置
        print("鼠标相对于滚动区域的位置:",event.pos()) # 鼠标相对于滚动区域的位置
        # if event.button()==Qt.LeftButton:
        #     print('11')


if __name__=='__main__':
    app = QApplication(sys.argv)
    mywidget=ImageWidget()
    mywidget.show()
    sys.exit(app.exec_())