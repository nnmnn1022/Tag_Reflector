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
        bg_color = '#D8D8D8'
        global_color = 'Black'
        global_font = 'Tahoma, Arial'
        is_allow_overlapping_tags = False
        tag_setting = []

        # 반드시 엑셀의 순서와 동일해야 함 1~
        settings_list = ['bg_color', 'global_color', 'global_font', 'is_allow_overlapping_tags', 'tag_setting']

        for i, set in enumerate(settings_list):
            try:
                if set == 'global_font' and settings[i+1][1]:
                    exec(f'{set} = settings[{i+1}][1] + ", " + {set}')
                elif set == 'is_allow_overlapping_tags':
                    if settings[i+1][1].lower() == 'y' or settings[i+1][1].lower() == 'yes' or settings[i+1][1].lower() == 'true':
                        exec(f'{set} = True')
                elif set == 'tag_setting':
                    exec(f'{set} = settings[{i+1}:]')
                else:
                    exec(f'{set} = settings[{i+1}][1]')

            except IndexError:
                continue
            except Exception as e :
                app = QApplication([])
                window = QWidget()
                QMessageBox.warning(window, '오류', 'tag_settings.csv 파일에 이상이 있습니다.')
                window.show()
            
else : # 아니면
    writeFile.run([['아래 셀에 태그(정규표현식)를 입력하세요.', '아래 셀에 #을 제외한 색상코드가 있는 위치\n 또는 색상코드 또는 원하는 기능을 입력하세요.'],['"Background Color"',"#D8D8D8"],['"Global Font Color"',"White"],['"Global Font"',""]], 'tag_settings') # setting_file 파일을 만든다.
    app = QApplication([])
    window = QWidget()
    QMessageBox.information(window, '알림', 'tag_settings.csv 파일을 생성했습니다.')
    window.show()
    
def is_number(n):
    try:
        float(n)  
    except Exception:
        return False
    return True

def tag_to_nomal_text(text:str, matches:list, msg:str, is_left:bool=True) -> str:
    new_text = ""
    last_end = 0
    for match in matches:
        new_text += text[last_end:match.start()]
        if is_left:
            new_text += f' {msg} ⌦' + match.group()[1:-1] + '⌫' 
        else:
            new_text += '⌦' + match.group()[1:-1] + f'⌫ {msg} ' 
        last_end = match.end()
    new_text += text[last_end:]
    return new_text

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
            # 출력창1 데이터
            if len(self.textField_output.toPlainText()) > 0:
                self.textField_output.clear()
            text = self.textField_input.toPlainText()
            text = self.line_break(text)
            text = self.color_tag(text)

            # 출력창2 데이터
            if len(self.textField_output2.toPlainText()) > 0:
                self.textField_output2.clear()
            text3 = self.textField_input2.toPlainText()
            text3 = self.line_break(text3)
            text3 = self.color_tag(text3)

            if text and text3:
                text, text3 = self.validate(text, text3)
            text = self.replace_for_visible_tag(text)
            text3 = self.replace_for_visible_tag(text3)

            self.textField_output.append(text)
            self.textField_output2.append(text3)

        except Exception as e:
            print(e)

    def replace_for_visible_tag(self, text:str):
        if not text: return text
        text = re.sub(r'⌦[bB][rR]\/{0,1}⌫','<br>', text)
        text = text.replace('⨴', '<span style="color:red">').replace('⨵', '</span>')
        text = text.replace('⌦', '<span style="color:red">&lt;</span>').replace('⌫', '<span style="color:red">&gt;</span>')
        text = f'<span style="color:{global_color}; font-family:{global_font}">' + text + '</span>'
        
        return text

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
        return text
    
    def checkTagPairs(self, text:str, mode:str='start'):
        tags = re.finditer(r'<[\s\S]+?>', text)

        if mode in ['start', 'end']:
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

            if mode == 'start':
                msg = '⨴😡No Opening Tag⨵'
                new_text = tag_to_nomal_text(text, miss_start, msg)

            else:
                msg = '⨴No Closing Tag😡⨵'
                new_text = tag_to_nomal_text(text, miss_start, msg, False)
        # overlap
        else:
            overlap = []
            tag_list = []
            flag1 = True    # True:여는태그 False:닫는 태그
            flag2 = True    # 1이 이전, 2는 새로 들어온 태그

            for tag in tags:
                if re.search(r'<[bB][rR]\/{0,1}>', tag.group()) : continue
 
                # 들어온 tag가 여는태그, 닫는태그인지 확인해서 플래그 주기
                flag2 = False if '/' in tag.group() else True

                # 앞에서 짝이 안 맞는 태그들은 모두 걸러냈다고 가정
                # 그러므로 맨 앞에 flag2 = false 일 수 없음
                # 이미 들어온 게 있을 때
                if tag_list:
                    # 여는 태그가 또 들어올 때
                    if flag1 == flag2:
                        overlap.append(tag_list.pop())
                        tag_list.append(tag)
                    # 닫는 태그가 들어올 때
                    else:
                        tag_list.pop()
                # 들어와 있는 게 없을 때
                else:
                    if flag2 == False:
                        overlap.append(tag)
                    else:
                        tag_list.append(tag)

                flag1 = flag2

            msg = '⨴Overlapping Tag⨵'
            new_text = ""
            last_end = 0
            for match in overlap:
                new_text += text[last_end:match.start()]
                if '/' in match.group():
                    new_text += f'😡{msg} ⌦' + match.group()[1:-1] + '⌫'
                else:
                    new_text += '⌦' + match.group()[1:-1] + f'⌫ {msg}😡'
                last_end = match.end()
            new_text += text[last_end:]

        return new_text

    def color_tag(self, text) :
        new_text:str = text
        new_text = new_text.replace('<', '⌦').replace('>', '⌫')
        color_code_rgx0 = re.compile(r'#[a-fA-F0-9]{8}')
        color_code_rgx1 = re.compile(r'#[a-fA-F0-9]{6}')
        color_code_rgx2 = re.compile(r'[a-fA-F0-9]{6}')
        color_list = ['red','yellow','black','gray','blue','white',
                      'green','orange','cyan','purple','pink','brown','lightgreen']
        for row in tag_setting :
            regex_tag = re.compile(row[0].replace('<', '⌦').replace('>', '⌫'))
            remain = row[1]
            if '~' in remain :
                remain1 = int(remain.split('~')[0])
                remain2 = None if remain.split('~')[1] == '' else int(remain.split('~')[1])

            tags = re.findall(regex_tag, new_text)
            if not tags : continue
            for tag in tags :
                # 정상적인 내용이 있으면 원복
                if re.search(r'⌦span style="color:#[a-zA-z0-9]{6}"⌫|⌦span⌫', tag) :
                    new_text = new_text.replace('⌦', '<').replace('⌫', '>')

                # 태그를 직접 입력하는 경우
                elif remain and ('~' not in remain) :
                    new_text = new_text.replace(tag, remain)

                elif remain2 == None or (is_number(remain2)) :
                    # tag에 있는 색상코드만 추출해서 사용
                    # remain1 이상 - remain2 미만
                    color_code = "".join(tag[remain1:remain2])
                    # if 'skillinfo' in tag.lower():
                    # 색상코드 확인
                    if regex_tag == color_code_rgx0:
                        new_text = new_text.replace(tag, '#' + color_code)
                    elif color_code.lower() in color_list:
                        new_text = new_text.replace(tag,
                                                    f'<span style="color:{color_code}">')
                    elif color_code_rgx1.match(color_code):
                        new_text = new_text.replace(tag,
                                                    f'<span style="color:{color_code}">')
                    elif color_code_rgx2.match(color_code):
                        new_text = new_text.replace(tag,
                                                    f'<span style="color:#{color_code}">')

        new_text = self.line_break(new_text)
        new_text = new_text.replace('⌦/span⌫', '</span>')

        new_text = self.checkTagPairs(new_text, mode='start')
        new_text = self.checkTagPairs(new_text, mode='end')
        if not is_allow_overlapping_tags:
            new_text = self.checkTagPairs(new_text, mode='overlap')

        return new_text

    def validate(self, text, text2):

        # validate
        def validate_matches(tags1:list, tags2:list):
            errors = []
            for match in tags1:
                # 문자열이 right_tags에 있으면 삭제하고 없으면 left_errors에 값 추가
                try:
                    tags2.remove(match)
                except ValueError :
                    errors.append(match)
            return errors

        regex = re.compile(r'<.+?>')
        regex2 = re.compile(r'⌦.*?⌫')
        br = re.compile(r'⌦[bB][rR]\/{0,1}⌫')

        # 태그 데이터 추출
        # left_matches = [m for m in regex.finditer(text)]
        # right_matches = [m for m in regex.finditer(text2)]

        # 다른 오류 나고 있는 태그들도 포함시키기
        left_error_tags = [m.replace('⌦', '<').replace('⌫', '>') for m in regex2.findall(text) if not br.match(m)]
        right_error_tags = [m.replace('⌦', '<').replace('⌫', '>') for m in regex2.findall(text2) if not br.match(m)]

        # 태그 내용만 추출
        left_tags = regex.findall(text)
        left_tags.extend(left_error_tags)

        right_tags = regex.findall(text2)
        right_tags.extend(right_error_tags)

        left_errors = list(map(lambda x: '⌦' + x[1:-1] + '⌫' , validate_matches(left_tags, right_tags)))
        right_errors = list(map(lambda x: '⌦' + x[1:-1] + '⌫' , validate_matches(right_tags, left_tags)))
        
        msg1 = f'<br><br> ⨴#오른쪽에 존재하지 않는 태그 목록: {", ".join(left_errors)}⨵'
        msg2 = f'<br><br> ⨴#왼쪽에 존재하지 않는 태그 목록: {", ".join(right_errors)}⨵'

        if left_errors: text += msg1
        if right_errors: text2 += msg2

        return text, text2

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())