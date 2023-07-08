# -*- coding: utf-8 -*-
import sys
import re
import os
import csv
import pathlib
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QTextBrowser, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import *
import writeFile

# Settings 가져오기
setting_file = f'{str(pathlib.Path.cwd())}/tag_settings.csv'
if os.path.isfile(setting_file) : # setting_file이라는 파일이 있으면 읽기
    with open(setting_file, 'r', encoding='utf-8-sig') as csvFile:
        settings = list(csv.reader(csvFile))
        bg_color = settings[1][1]
        global_color = settings[2][1]
        tag_setting = settings[3:]

else : # 아니면
    writeFile.run([['아래 셀에 태그(정규표현식)를 입력하세요.', '아래 셀에 #을 제외한 색상코드가 있는 위치\n 또는 색상코드 또는 원하는 기능을 입력하세요.'],['"Background Color"',"#D8D8D8"],['"Global Font Color"',"White"]], 'tag_settings') # setting_file 파일을 만든다.
    app = QApplication([])
    window = QWidget()
    QMessageBox.information(window, '알림', 'tag_settings.csv 파일을 생성했습니다.')
    window.show()
    exit()

def is_number(n):
    try:
        float(n)  
    except ValueError:
        return False
    return True

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    print(os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getSettings(self):
        pass

    def initUI(self):

        self.AOT_button = QPushButton(' Always on &Top ', self)
        self.AOT_button.setCheckable(True)
        self.AOT_button.clicked[bool].connect(self.always_on_top)

        #font
        font = QFont()
        font.setFamily(u"Tahoma")
        # font.setBold(True)
        # font.setWeight(75)

        # 입력 창
        self.textField_input = QTextEdit()
        self.textField_input.setAcceptRichText(False)

        # 입력 창2
        self.textField_input2 = QTextEdit()
        self.textField_input2.setAcceptRichText(False)

        #출력창
        self.textField_output = QTextBrowser()
        self.textField_output.setAcceptRichText(True)
        self.textField_output.setOpenExternalLinks(True)
        self.textField_output.setStyleSheet(f"background-color: {bg_color}")
        self.textField_output.setFont(font)

        #출력창2
        self.textField_output2 = QTextBrowser()
        self.textField_output2.setAcceptRichText(True)
        self.textField_output2.setOpenExternalLinks(True)
        self.textField_output2.setStyleSheet(f"background-color: {bg_color}")
        self.textField_output2.setFont(font)

        # 두 창에서 노출된 캐릭터 수
        self.textLabel1 = QLabel('공백 포함 : 0 Character')
        self.textLabel2 = QLabel('공백 포함 : 0 Character')
        self.textLabel3 = QLabel('공백 제외 : 0 Character')
        self.textLabel4 = QLabel('공백 제외 : 0 Character')

        # 두 창에서 노출된 캐릭터 수2
        self.textLabel5 = QLabel('공백 포함 : 0 Character')
        self.textLabel6 = QLabel('공백 포함 : 0 Character')
        self.textLabel7 = QLabel('공백 제외 : 0 Character')
        self.textLabel8 = QLabel('공백 제외 : 0 Character')

        # 캐릭터 수 수정될 수 있도록 해주는 함수 연결
        self.textField_input.textChanged.connect(self.text_changed)
        self.textField_output.textChanged.connect(self.text_changed)
        self.textField_input.textChanged.connect(self.append_text)

        # 캐릭터 수 수정될 수 있도록 해주는 함수 연결
        self.textField_input2.textChanged.connect(self.text_changed)
        self.textField_output2.textChanged.connect(self.text_changed)
        self.textField_input2.textChanged.connect(self.append_text)

        # 클리어 버튼
        self.clear_btn = QPushButton('Clear')
        self.clear_btn.pressed.connect(self.clear_input_text)

        # 수평 박스
        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.AOT_button)
        hbox0.addStretch(9)

        hbox = QHBoxLayout()
        hbox.addWidget(self.textField_input)
        hbox.addWidget(self.textField_output)
        hbox.addWidget(self.textField_output2)
        hbox.addWidget(self.textField_input2)

        # 수평 박스 2
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.textLabel1)
        hbox2.addWidget(self.textLabel2)
        hbox2.addWidget(self.textLabel5)
        hbox2.addWidget(self.textLabel7)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.textLabel3)
        hbox4.addWidget(self.textLabel4)
        hbox4.addWidget(self.textLabel6)
        hbox4.addWidget(self.textLabel8)

        hbox3 = QHBoxLayout()
        # hbox3.addWidget(self.enter_btn)
        hbox3.addWidget(self.clear_btn)

        # 수직 박스
        vbox = QVBoxLayout()
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox)
        vbox.setStretch(1, 10)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox4)
        vbox.addStretch(1)
        vbox.addLayout(hbox3)

        window_ico = resource_path('tag_icon.png')
        self.setWindowIcon(QIcon(window_ico))

        self.setLayout(vbox)
        self.setWindowTitle('Tag Reflector')
        self.resize(1600, 800)
        # self.center()
        self.show()

    def always_on_top(self, aot) :
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowStaysOnTopHint)
        self.show()

    def text_changed(self):
        text = self.textField_input.toPlainText()
        del_text = text.replace('\n', '')
        del_text3 = del_text.replace(' ', '')
        self.textLabel1.setText('공백 포함 : ' + str(len(del_text)) + ' Character')
        self.textLabel3.setText('공백 제외 : ' + str(len(del_text3)) + ' Character')

        text2 = self.textField_output.toPlainText()
        del_text2 = text2.replace('\n', '')
        del_text4 = del_text2.replace(' ', '')
        self.textLabel2.setText('공백 포함 : ' + str(len(del_text2)) + ' Character')
        self.textLabel4.setText('공백 제외 : ' + str(len(del_text4)) + ' Character')

        text3 = self.textField_input2.toPlainText()
        del_text5 = text3.replace('\n', '')
        del_text6 = del_text5.replace(' ', '')
        self.textLabel7.setText('공백 포함 : ' + str(len(del_text5)) + ' Character')
        self.textLabel8.setText('공백 제외 : ' + str(len(del_text6)) + ' Character')

        text4 = self.textField_output2.toPlainText()
        del_text7 = text4.replace('\n', '')
        del_text8 = del_text7.replace(' ', '')
        self.textLabel5.setText('공백 포함 : ' + str(len(del_text7)) + ' Character')
        self.textLabel6.setText('공백 제외 : ' + str(len(del_text8)) + ' Character')

    def append_text(self):
        try :
            if len(self.textField_output.toPlainText()) > 0:
                self.textField_output.clear()
            text = self.textField_input.toPlainText()
            text = self.line_break(text)
            text = self.color_tag(text)
            self.textField_output.append(text)

            if len(self.textField_output2.toPlainText()) > 0:
                self.textField_output2.clear()
            text3 = self.textField_input2.toPlainText()
            text3 = self.line_break(text3)
            text3 = self.color_tag(text3)
            self.textField_output2.append(text3)

        except Exception as e:
            print(e)

    def clear_input_text(self):
        self.textField_input.clear()
        self.textField_output.clear()
        self.textField_input2.clear()
        self.textField_output2.clear()

    def line_break(self, text) :
        text = re.sub(r'\"+','"',text)
        text = text.replace('\\r\\n', '\n')
        text = text.replace('\\n', '\n')
        text = text.replace('\n', '<br>')
        text = re.sub(r'⌦[bB][rR]\/{0,1}⌫','<br>', text)
        return text

    def color_tag(self, text) :
        new_text:str = text
        new_text = new_text.replace('<', '⌦').replace('>', '⌫')
        color_code_rgx1 = re.compile(r'#[a-fA-F0-9]{6}')
        color_code_rgx2 = re.compile(r'[a-fA-F0-9]{6}')
        color_list = ['red','yellow','black','gray','blue','white',
                      'green','orange','cyan','purple','pink','brown']
        for row in tag_setting :
            regex_tag = re.compile(row[0].replace('<', '⌦').replace('>', '⌫'))
            remain = row[1]
            if '~' in remain :
                remain1 = int(remain.split('~')[0])
                remain2 = int(remain.split('~')[1])

            tags = re.findall(regex_tag, new_text)
            if not tags : continue
            for tag in tags :
                # 정상적인 내용이 있으면 원복
                if re.search(r'⌦span style="color:#[a-zA-z0-9]{6}"⌫|⌦span"⌫', tag) :
                    new_text.replace('⌦', '<').replace('⌫', '>')

                elif remain and ('~' not in remain) :
                    new_text = new_text.replace(tag, remain)

                elif remain2 and is_number(remain2) :
                    # tag에 있는 색상코드만 추출해서 사용
                    # remain1 이상 - remain2 미만
                    color_code = "".join(tag[remain1:remain2])
                    # if 'skillinfo' in tag.lower():
                    #     # 색상코드 확인
                    if color_code.lower() in color_list:
                        new_text = new_text.replace(tag,
                                                    f'<span style="color:{color_code}">')
                    elif color_code_rgx1.match(color_code):
                        new_text = new_text.replace(tag,
                                                    f'< style="color:{color_code}">')
                    elif color_code_rgx2.match(color_code):
                        new_text = new_text.replace(tag,
                                                    f'<span style="color:#{color_code}">')

        new_text = self.line_break(new_text)
        new_text = new_text.replace('⌦/span⌫', '</span>')
        new_text = new_text.replace('⌦', '&lt;').replace('⌫', '&gt;')

        tags = re.finditer(r'<[\s\S]+?>', new_text.lower())
        miss_start = []
        miss_end = []

        for tag in tags:
            if re.search(r'<[bB][rR]\/{0,1}>', tag.group()) : continue
            if '/' in tag.group():
                if miss_end:
                    miss_end.pop()
                else:
                    miss_start.append(tag)
            else:
                miss_end.append(tag)

        no_opening_msg = '<span style="color:red">😡No Opening Tag</span>'
        no_closing_msg = '<span style="color:red">No Closing Tag😡</span>'

        for miss in miss_start:
            start, end = miss.start(), miss.end()
            new_text = new_text[:start] + f' {no_opening_msg} &lt;' + new_text[start+1:end-1] + '&gt;' + new_text[end:]

        for miss in miss_end:
            start, end = miss.start(), miss.end()
            new_text = new_text[:start] + '&lt;' + new_text[start+1:end-1] + f'&gt; {no_closing_msg} ' + new_text[end:]
            
        new_text = f'<span style="color:{global_color}">' + new_text + '</span>'
        return new_text


if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())