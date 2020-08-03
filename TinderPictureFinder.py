import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PictureProcessing import *
from TextProcessing import *
import os
from datetime import datetime, date, time
from os.path import expanduser
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import org.openqa.selenium.chrome.ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import socket
import re


class Form(QMainWindow):
    filename = []  # private
    save_dir = ''
    DeskTopPath = ''
    def __init__(self, parent=None):
        super().__init__(parent)

        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setFont(QFont('Arial', 11))

        getFileNameButton = QPushButton("Open Picture(s)")
        getFileNameButton.clicked.connect(self.getFileName)

        startResizingButton = QPushButton("Resize Picture(s)")
        startResizingButton.clicked.connect(self.resizePicture)

        findInYaImButton = QPushButton("Open in YI")
        findInYaImButton.clicked.connect(self.findInYa)

        CloseButton = QPushButton("Close Program")
        CloseButton.clicked.connect(self.close_application)

        layoutV = QVBoxLayout()
        #layoutV = QHBoxLayout()
        layoutV.setAlignment(Qt.AlignTop)
        #layoutV.addStretch()
        layoutV.addWidget(getFileNameButton)
        layoutV.addWidget(startResizingButton)
        layoutV.addWidget(findInYaImButton)
        layoutV.addWidget(CloseButton)

        layoutH = QHBoxLayout()
        layoutH.addLayout(layoutV)
        layoutH.addWidget(self.plainTextEdit)
        #self.plainTextEdit.insertPlainText("Нажмите кнопку Open Picture и выбирите файл(ы) для кадрировани. \n")

        centerWidget = QWidget()
        centerWidget.setLayout(layoutH)
        self.setCentralWidget(centerWidget)

        self.resize(740, 480)
        self.setWindowTitle("TinderPictureDetection")
        self.setWindowIcon(QIcon('favicon.ico'))

        DeskTopPath = self.getPcOwner()


    def getFileName(self):
        #print(socket.gethostname())
        self.plainTextEdit.clear()
        Form.filename, filetype = QFileDialog.getOpenFileNames(self,
                                                               "Выбрать файл",
                                                               #"D:\\",
                                                                #"/home",
                                                               #self.DeskTopPath,
                                                               "C:\\",
                                                               "PNG (*.png);;JPEG (*.jpg *.jpeg)")
                                                               #"*.jpg, *.png")
        # print(Form.filename)
        if len(Form.filename) > 0:
            self.plainTextEdit.insertPlainText("Открыты следующие файлы: \n")
        else:
            pass
        i = 1
        for ele in Form.filename:
            text = str(i) + ")" + " " + ele + "\n"
            self.plainTextEdit.insertPlainText(text)
            i = i + 1
        if len(Form.filename) > 0:
            self.plainTextEdit.insertPlainText("\nНажмите кнопку Resize Picture(s). Кадрированные фотографии будут сохранены в выбранную Вами директорию. \n")


    def resizePicture(self):
        save_dir = QFileDialog.getExistingDirectory(self, 'Resize files to:', 'С:\\', QFileDialog.ShowDirsOnly)

        images = ImageProcessing.ResizeImageFunction(Form.filename)

        print(save_dir)

        for img in images:
            now = datetime.now()
            string_i_want = str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')) + '.jpg'
            #print(string_i_want)
            cv2.imwrite(os.path.join(save_dir, str(string_i_want)), img)

        if len(images) == len(Form.filename):
            text = "\n**********************************\n"
            self.plainTextEdit.insertPlainText(text)
            text = str(len(images)) + " фото обработаны и сохранены в папку: " + str(save_dir)
            self.plainTextEdit.insertPlainText(text)
            self.plainTextEdit.insertPlainText( "\nНажмите кнопку Open in YI. Результат поиска по фото откроется в поисковике Яндекс \n")


    def findInYa(self):

        #print(TextParse.ParseImageLocation("D:/Tested/2020_07_22_15_07_30_941929.jpg"))

        # Идем по всем фото в папке куда сохраняли обрезанные фото. Для каждого сохраненного фото открываем таб.
        filestosearch, filetype = QFileDialog.getOpenFileNames(self,
                                                               "Выбрать файл",
                                                               #"D:\\",
                                                               #"/home",
                                                               #self.DeskTopPath,
                                                               "C:\\",
                                                               "JPEG (*.jpg *.jpeg);;PNG (*.png)")

        if len(filestosearch)>0:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

            for img in filestosearch:
                driver.execute_script('window.open("{}", "_blank");'.format('https://yandex.ru/images/'))

            driver.close()
            allTabs = driver.window_handles

            for i, tab in enumerate(allTabs):
                driver.switch_to.window(tab)
                time.sleep(2)
                html = driver.page_source
                index = html.find("icon_type_cbir")
                if index != -1:
                    userName = driver.find_element_by_xpath(
                        "/html/body/div[1]/div/div[1]/header/div/div[1]/div[2]/form/div[1]/span/span/span[2]")
                    userName.click()
                else:
                    userName = driver.find_element_by_xpath(
                        "/html/body/header/div/div[1]/div[2]/form/div[1]/span/span/div[2]/button")
                    userName.click()
                #driver.find_element(By.XPATH, "//input[@name=\'upfile\']").click()

                userName = driver.find_element_by_xpath("//input[@name=\'upfile\']")
                #driver.execute_script("arguments[0].click();", userName)

                #userName.send_keys("D:/Tested/2020_07_22_15_07_30_941929.jpg")
                userName.send_keys(filestosearch[i])
            else:
                pass


    def close_application(self):
        choice = QMessageBox.question(self, 'Message',
                                      "Are you sure to quit?", QMessageBox.Yes |
                                      QMessageBox.No, QMessageBox.No)
        if choice == QMessageBox.Yes:
            print('quit application')
            sys.exit()
        else:
            pass

    def getPcOwner(self):
        name = socket.gethostname()
        name = socket.gethostname().replace("-ПК","")
        desktopdir = 'C:\\Users\\' + str(name) + '\\Desktop'
        print(desktopdir)
        return desktopdir


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec_())
