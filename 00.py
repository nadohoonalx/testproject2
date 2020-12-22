from PySide2.QtWidgets import QRadioButton
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import *
import re
import time

class Form(QWidget):

    def __init__(self):
        super(Form, self).__init__()

        self.setWindowTitle("찐리뷰")

        self.lst = []
        self.good=[]
        self.bad =[]
        self.page = 1
        self.exceptAlba = []
        self.includeSpo = []
        self.driver = webdriver.Chrome()
        self.lnKeyword = QLineEdit("")
        self.tmp_page =1

        self.rdSort_0 = QRadioButton("공감순")
        self.rdSort_1 = QRadioButton("비공감순")
        hbSort = QHBoxLayout()
        hbSort.addWidget(self.rdSort_0)
        hbSort.addWidget(self.rdSort_1)
        grpSort = QGroupBox()
        grpSort.setLayout(hbSort)

        self.rdType_0 = QRadioButton("전체")
        self.rdType_1 = QRadioButton("배우")
        self.rdType_2 = QRadioButton("스토리")
        self.rdType_3 = QRadioButton("연기")
        hbType = QHBoxLayout()
        hbType.addWidget(self.rdType_0)
        hbType.addWidget(self.rdType_1)
        hbType.addWidget(self.rdType_2)
        hbType.addWidget(self.rdType_3)
        grpType = QGroupBox()
        grpType.setLayout(hbType)

        self.rdType_4 = QRadioButton("전체")
        self.rdType_4.setChecked(True)
        self.rdType_5 = QRadioButton("알바제외")
        self.rdType_6 = QRadioButton("스포보기")
        hbFeild1 = QHBoxLayout()
        hbFeild1.addWidget(self.rdType_4)
        hbFeild1.addWidget(self.rdType_5)
        hbFeild1.addWidget(self.rdType_6)
        grpFeild1 = QGroupBox()
        grpFeild1.setLayout(hbFeild1)

        frm = QFormLayout()
        frm.addRow("영화 제목:", self.lnKeyword)
        frm.addRow("정렬기준: ", grpSort)
        frm.addRow("키워드: ", grpType)
        frm.addRow("필터링: ", grpFeild1)

        self.model = QStandardItemModel(0, 1, self)
        self.model.setHorizontalHeaderLabels(["리뷰모음"])
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setColumnWidth(0, 450)
        self.table.setFixedSize(450, 350)
        self.btnNext = QPushButton("다음")
        self.btnSearch = QPushButton("검색")



        hbPageCnt = QHBoxLayout()
        hbPageCnt.addWidget(self.btnSearch)
        hbPageCnt.addStretch()
        hbPageCnt.addWidget(self.btnNext)
        vbList = QVBoxLayout()
        vbList.addLayout(hbPageCnt)
        vbList.addWidget(self.table)

        hbMain = QHBoxLayout()
        hbMain.addLayout(frm)
        hbMain.addLayout(vbList)

        self.setLayout(hbMain)

        self.rdSort_0.toggle()
        self.rdType_0.toggle()
        self.rdType_4.toggle()

        self.rdSort_0.clicked.connect(self.radiolikehateEvent)
        self.rdSort_1.clicked.connect(self.radiolikehateEvent)

        self.rdType_4.clicked.connect(self.radiobuttonEvent)
        self.rdType_5.clicked.connect(self.radiobuttonEvent)
        self.rdType_6.clicked.connect(self.radiobuttonEvent)

        self.btnSearch.clicked.connect(self.searchNews)
        self.btnNext.clicked.connect(self.lstNext)
    def radiolikehateEvent(self):
        if len(self.lst) == 0:
            return
        if self.rdSort_0.isChecked()==True:
            self.lst.sort(reverse=False)
            self.exceptAlba.sort(reverse=False)
            self.includeSpo.sort(reverse=False)
            if self.rdType_4.isChecked() == True:
                if len(self.lst) > 0:
                    self.apply_lst(self.lst)
            elif self.rdType_5.isChecked() == True:
                self.apply_lst(self.exceptAlba)
            elif self.rdType_6.isChecked() == True:
                self.apply_lst(self.includeSpo)
        elif self.rdSort_1.isChecked() == True:
            self.lst.sort(reverse=True)
            self.exceptAlba.sort(reverse=True)
            self.includeSpo.sort(reverse=True)
            if self.rdType_4.isChecked() == True:
                if len(self.lst) > 0:
                    self.apply_lst(self.lst)
            elif self.rdType_5.isChecked() == True:
                self.apply_lst(self.exceptAlba)
            elif self.rdType_6.isChecked() == True:
                self.apply_lst(self.includeSpo)
    def radiobuttonEvent(self):
        if self.rdType_4.isChecked()==True:
            if len(self.lst) > 0:
                self.apply_lst(self.lst)
        elif self.rdType_5.isChecked()==True:
            self.apply_lst(self.exceptAlba)
        elif self.rdType_6.isChecked()==True:
            self.apply_lst(self.includeSpo)

    def lstNext(self):
        self.tmp_page +=10
        self.lst.clear()
        self.searchNews()
    def closeEvent(self, QCloseEvent):
        self.driver.close()

    def searchNews(self):
        if self.sender().text() == "검색":
            self.page = 1

        if self.page == 1:
            url = 'https://movie.naver.com/'
            self.driver.get(url)

            self.driver.find_element_by_css_selector('.ipt_tx_srch').send_keys(self.lnKeyword.text())
            self.driver.find_element_by_css_selector('.btn_srch').click()
            self.driver.find_element_by_css_selector('ul.search_list_1 li dt a').click()
            print(self.driver.current_url)
        code_st = re.search('code=[0-9]+',self.driver.current_url).group()
        code = re.search('[0-9]+',code_st).group()
        self.page = self.tmp_page
        while self.page<self.tmp_page+10:
           ##전체
           url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code='\
               +str(code)+'&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false+&page='\
             +str(self.page)
           self.driver.get(url)
           html = self.driver.page_source
           soup = BeautifulSoup(html,'html.parser')
           content_list = soup.find('div', class_='score_result').find('ul').find_all('li')
           for li in content_list:
               self.lstdata = li.find('div', class_='score_reple').find('p').text
               self.lstdata = self.lstdata.replace('\t','').replace('\n','')
               self.gooddata = li.find('div', class_='btn_area').find_all('strong')[0].text
               self.baddata = li.find('div', class_='btn_area').find_all('strong')[1].text
               if int(self.gooddata)>30 :
                   self.exceptAlba.append(self.lstdata)
               self.lst.append(self.lstdata)
               self.good.append(self.gooddata)
               self.bad.append(self.baddata)

           self.page += 1

        if self.page>1 :
            self.page = 1

        ##스포포함
        time.sleep(1)
        while self.page<10:
            url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code='\
                +str(code)+'&type=after&onlyActualPointYn=N&onlySpoilerPointYn=Y&order=sympathyScore&page='\
              +str(self.page)
            self.driver.get(url)
            html = self.driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            content_list = soup.find('div', class_='score_result').find('ul').find_all('li')
            for li in content_list:
                self.lstdata = li.find('div', class_='score_reple').find('p').text
                self.lstdata = self.lstdata.replace('\t','').replace('\n','')
                self.includeSpo.append(self.lstdata)
            self.page += 1
        self.apply_lst(self.lst)



    def apply_lst(self,data):
        self.table.reset()
        self.model.removeRows(0, self.model.rowCount())
        self.model.setRowCount(len(data))
        self.model.setRowCount(len(data))
        self.model.setVerticalHeaderLabels(['' for i in range(len(data))])


        for i in range(0,len(data),1):
            item = QStandardItem()
            item.setText(data[i])
            QStandardItemModel.insertRow(self.model,i,item)





app = QApplication([])
form = Form()
form.show()
sys.exit(app.exec_())