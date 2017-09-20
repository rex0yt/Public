#coding:utf-8

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.support.select import Select

url = "http://authserver.nwafu.edu.cn/authserver/login\
?service=http%3A%2F%2Fjwgl.nwsuaf.edu.cn%2Facademic%2Flogin%2Fnwsuaf%2FloginIds6Valid.jsp"

driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
#driver = webdriver.Firefox()

alltr = list()
pagesource = ""

def login(username, password):
    driver.get(url)
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("send-btn").click()


def getAllGrades():
    gradeUrl = "http://jwgl.nwsuaf.edu.cn/academic/manager/score/studentOwnScore.do?groupId=&moduleId=2020"
    driver.get(gradeUrl)
    alltag = driver.find_elements_by_tag_name("select")
    #print(alltag)
    timetag = alltag[0]
    seasontag = alltag[-1]
    Select(timetag).select_by_value("")
    Select(seasontag).select_by_value("")
    driver.find_element_by_class_name("button").click()
    global pagesource
    pagesource = driver.page_source
    driver.quit()


def parserPage():
    soup = BeautifulSoup(pagesource,"html.parser")    
    table = soup.find_all("table", class_="datalist")

    global alltr
    alltr = table[0].find_all("tr", class_="")


def calcGrade(alltr):
    isum = 0
    cntxuefen = 0

    for itr in alltr:
        alltext = itr.find_all("td")
        if(len(alltext) > 1):
            if(alltext[14].text.strip() != "任选"):
                thisxuefen = float(alltext[11].text.strip())
                thischenji = float(alltext[10].text.strip())
                cntxuefen = cntxuefen + thisxuefen
                isum = isum + thischenji*thisxuefen
                #outfile.write(tmp.text.strip()+" ")
    
    print("总学分：", cntxuefen, "总成绩", isum)
    print("学分成绩：", isum/cntxuefen)


def outputTxt(alltr):
    outfile = open("data.txt","w")


    # for i in range(1,21):
    #     outfile.write(str(i)+" ")
    # outfile.write("\n")

    for itr in alltr:
        alltext = itr.find_all("th")
        for tmp in alltext:
            outfile.write(tmp.text.strip()+" ")
    outfile.write("\n")

    for itr in alltr:
        alltext = itr.find_all("td")
        for tmp in alltext:
            outfile.write(tmp.text.strip()+" ")
        outfile.write("\n")

    outfile.close()


def main():
    print("首先确保你处于校园网络下！！！")
    username = input("请输入你的学号:\n").strip()
    password = input("请输入你的教务系统密码:\n").strip()

    print(username, password)
    login(username, password)
    getAllGrades()
    parserPage()
    global alltr
    calcGrade(alltr)
    outputTxt(alltr)
    print("在当前目录下查看data.txt成绩文件")
    print("按回车键结束")
    tmp = input()

main()

