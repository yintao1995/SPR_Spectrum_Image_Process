# _*_ coding:utf-8 _*_
"""
A portable integrated tool with GUI in processing SPR data.
Including resonance of spectrums and hue of images.
"""
import sys
import matplotlib.pyplot as plt
# from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QProgressDialog
from image_viewer import ImageWidget
from gui_design import *
from spr_data_read import visual_data, read_data
from hue_of_image import draw_image, hue_of_image


class MyMainWindow(QMainWindow, Ui_MainWindow):
    """
    Main GUI.
    """
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        # Do things more than designer did about widgets, set attributes.
        self.lineEdit_1.setFixedSize(40, 20)
        self.lineEdit_2.setFixedSize(40, 20)
        self.lineEdit_3.setFixedSize(40, 20)
        self.lineEdit_4.setFixedSize(40, 20)
        self.pushButton_4.setFixedSize(35, 55)
        self.pushButton_7.setMaximumWidth(40)
        self.lineEdit_8.setMaximumWidth(70)
        self.lineEdit_9.setMaximumWidth(70)
        self.checkBox_1.setChecked(True)

        # Signals and Slots.
        self.pushButton_0.clicked.connect(self.choose_files)
        self.textEdit.textChanged.connect(self.drag_files_supported)
        self.pushButton_1.clicked.connect(self.draw_spectrum_separately)
        self.pushButton_2.clicked.connect(self.draw_spectrum_together)
        self.pushButton_3.clicked.connect(self.calculate_hue)
        self.pushButton_4.clicked.connect(self.relation_hue_vary_with_resonance)
        self.pushButton_5.clicked.connect(self.relation_hue_vary_with_time)
        self.pushButton_6.clicked.connect(self.relation_resonance_vary_with_time)
        self.pushButton_7.clicked.connect(self.open_image_viewer)

    def choose_files(self):
        """
        Choose multiple data files and displaying them.
        More convenient for visualized management and operation.
        """
        files = QFileDialog.getOpenFileNames(self, 'Choose files', '',
            "All files(*);;TXT(*.txt);;Image(*.bmp *.jpg *.png)", None, QFileDialog.DontUseNativeDialog)
        filename_list = files[0]
        if not filename_list:
            return
        # print(filename_list)
        self.textEdit.clear()
        name_list = []
        for filename in filename_list:
            self.textEdit.append(filename)
            name_list.append(filename.split('/')[-1])
        self.textEdit.append('\n')
        self.lineEdit_5.setText(str(name_list))

    def draw_spectrum_separately(self):
        """
        Draw spectrum separately, one spectrum for one image.
        Better for save single spectrum image.
        """
        filename_list = self.textEdit.toPlainText().strip().split('\n')
        try:
            resonance_wavelength_list = []
            label = []
            for filename in filename_list:
                if not filename:
                    continue
                data = visual_data(read_data(filename, '\t'))
                plt.figure()
                plt.plot(data[0], data[1])
                plt.axvline(data[2], c='red', alpha=0.5)
                plt.text(500, 0.2, "resonance wavelength=" + str(data[2]) + "nm")
                resonance_wavelength_list.append(data[2])
                label.append(filename.split('/')[-1])
                plt.legend(label)
            if resonance_wavelength_list:
                self.lineEdit_6.setText(str(resonance_wavelength_list))
                plt.show()
        except:
            pass

    def draw_spectrum_together(self):
        """
        Draw spectrum together, multiple spectrums in one image.
        Focus on results.
        Choose whether to display images by enable/disable Checkbox.
        """
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
                    plt.plot(data[0], data[1])
                    plt.scatter(data[2], data[3], s=5)
                    label.append(filename.split('/')[-1] + "[" + ("%.2f" % data[2]) + "nm]")
                file_existing_flag = 1
            if resonance_wavelength_list:
                self.lineEdit_6.setText(str(resonance_wavelength_list))
                QMessageBox.information(self, 'Done', 'Process Done')
                if not self.checkBox_1.isChecked():
                    plt.legend(label)
                    plt.show()
        except:
            pass

    def calculate_hue(self):
        """
        Calculate hue value and it's distribution of SPR images.
        Still, choose whether to display images by enable/disable Checkbox.
        """
        filename_list = self.textEdit.toPlainText().strip().split('\n')
        self.lineEdit_7.clear()
        try:
            average_hue_list = []
            x_1 = int(self.lineEdit_1.text())
            x_2 = int(self.lineEdit_2.text())
            x_3 = int(self.lineEdit_3.text())
            x_4 = int(self.lineEdit_4.text())
            n = len(filename_list)
            progress_dialog = QProgressDialog(self)
            progress_dialog.setWindowTitle('Please wait')
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setLabelText('processing...')
            progress_dialog.setRange(0, n)
            progress_dialog.show()
            i = 0
            for filename in filename_list:
                i = i+1
                progress_dialog.setValue(i)
                if x_1+x_2+x_3+x_4 == 0:
                    data = hue_of_image(filename)
                else:
                    data = hue_of_image(filename, x_1, x_2, x_3, x_4)
                if not self.checkBox_1.isChecked():
                    draw_image(filename.split('/')[-1], data[0], data[1])
                average_hue_list.append(data[0])
            self.lineEdit_7.setText(str(average_hue_list))
            QMessageBox.information(self, 'Done', 'Process Done')
            if not self.checkBox_1.isChecked():
                plt.show()
        except:
            pass

    def relation_hue_vary_with_resonance(self):
        """
        Draw relative curve between resonance wavelengths and their
        corresponding hue values after data processed.
        """
        try:
            list_wavelength = [float(i) for i in self.lineEdit_6.text()[1:-1].split(',')]
            list_hue = [float(i) for i in self.lineEdit_7.text()[1:-1].split(',')]
            if len(list_wavelength) != len(list_hue):
                QMessageBox.warning(self, "警告", "两个列表数量不相等")
            plt.figure()
            plt.title("wavelength-hue")
            plt.plot(list_wavelength, list_hue)
            plt.show()
        except:
            pass

    def relation_hue_vary_with_time(self):
        """
        Draw relative curve between time and hue value.
        A sampling interval (unit: sec) should be configured.
        """
        try:
            interval = float(self.lineEdit_8.text())
            list_hue = [float(i) for i in self.lineEdit_7.text()[1:-1].split(',')]
            list_time = [i*interval for i in range(len(list_hue))]
            plt.figure()
            plt.title("Hue values vary with time")
            plt.plot(list_time, list_hue)
            plt.ylabel("Hue")
            plt.xlabel("Time/s")
            plt.show()
        except:
            pass

    def relation_resonance_vary_with_time(self):
        """
        Draw relative curve between time and resonance wavelengths.
        A sampling interval (unit: sec) should be configured.
        """
        try:
            interval = float(self.lineEdit_9.text())
            list_wavelength = [float(i) for i in self.lineEdit_6.text()[1:-1].split(',')]
            list_time = [i*interval for i in range(len(list_wavelength))]
            plt.figure()
            plt.title("Resonance wavelength varies with time")
            plt.plot(list_time, list_wavelength)
            plt.ylabel('$\lambda$/nm')
            plt.xlabel("Time/s")
            plt.show()
        except:
            pass

    def open_image_viewer(self):
        """
        Self-made Image Viewer has been added In order to make a
        well-chosen selection over image.
        """
        image_viewer_widget = ImageWidget()
        image_viewer_widget.setAttribute(Qt.WA_DeleteOnClose)
        image_viewer_widget.show()
        image_viewer_widget.mySignal.connect(
            lambda: self.obtain_selection_parameters(image_viewer_widget))

    def obtain_selection_parameters(self, image_viewer_widget):
        """
        Pass parameters of selections.
        """
        try:
            size_data = image_viewer_widget.transmit_selection()
            self.lineEdit_1.setText(str(size_data[0]))
            self.lineEdit_2.setText(str(size_data[1]))
            self.lineEdit_3.setText(str(size_data[2]))
            self.lineEdit_4.setText(str(size_data[3]))
        except:
            pass

    def drag_files_supported(self):  # 拖拽文件到文本框时，会以'file:///'开头显示文件路径，此函数将此前缀删除
        """
        When dragging files from File Explorer to edit area directly,
        delete the prefix 'file:///' automatically.
        When dragging multiple files, please make sure your mouse pointer
        is over the first one if U wanna keep the order as it originally be.
        """
        if self.textEdit.toPlainText().find('file:///') != -1:
            self.textEdit.setText(self.textEdit.toPlainText().replace('file:///', '')+'\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MyMainWindow()
    mw.show()
    sys.exit(app.exec_())
