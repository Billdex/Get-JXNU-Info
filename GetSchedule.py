import requests
from bs4 import BeautifulSoup
import bs4
import re
import json
import sys
from spiderUtils import *



def getSchedule(stuNum, year, semester):
    data = {
        "__VIEWSTATE": "/wEPDwUINTczMTc3MzMPZBYCAgMPZBYCAgEPZBYCZg9kFgwCAQ8PFgIeBFRleHQFHuaxn+ilv+W4iOiMg+Wkp+WtpuWtpueUn+ivvuihqGRkAgMPDxYCHwAFgAHnj63nuqflkI3np7DvvJo8VT4xNue6p+i9r+S7tuW3peeoi++8iOiZmuaLn+eOsOWunuaWueWQke+8ieePrTwvVT7jgIDjgIDlrablj7fvvJo8VT4yMDE2MjY3MDMwMTE8L3U+44CA44CA5aeT5ZCN77yaPHU+572X6ZGrPC91PmRkAgUPEA8WBh4NRGF0YVRleHRGaWVsZAUM5a2m5pyf5ZCN56ewHg5EYXRhVmFsdWVGaWVsZAUM5byA5a2m5pel5pyfHgtfIURhdGFCb3VuZGdkEBUIDzE5LTIw56ysMeWtpuacnw8xOC0xOeesrDLlrabmnJ8PMTgtMTnnrKwx5a2m5pyfDzE3LTE456ysMuWtpuacnw8xNy0xOOesrDHlrabmnJ8PMTYtMTfnrKwy5a2m5pyfDzE2LTE356ysMeWtpuacnw8xNS0xNuesrDLlrabmnJ8VCBAyMDE5LzkvMSAwOjAwOjAwEDIwMTkvMy8xIDA6MDA6MDAQMjAxOC85LzEgMDowMDowMBAyMDE4LzMvMSAwOjAwOjAwEDIwMTcvOS8xIDA6MDA6MDAQMjAxNy8zLzEgMDowMDowMBAyMDE2LzkvMSAwOjAwOjAwEDIwMTYvMy8xIDA6MDA6MDAUKwMIZ2dnZ2dnZ2dkZAIJDw8WAh4HVmlzaWJsZWhkZAIKDzwrAAsBAA8WCB4IRGF0YUtleXMWAB4LXyFJdGVtQ291bnQC/////w8eFV8hRGF0YVNvdXJjZUl0ZW1Db3VudAL/////Dx4JUGFnZUNvdW50ZmRkAgsPPCsACwIADxYIHwUWAB8GAv////8PHwcC/////w8fCGZkATwrAAcBBjwrAAQBABYCHwRoZGS03nP34SbWiixRa28kr8vQ4gXm//NIq0uJanf1SWVY4Q==",
        "__EVENTVALIDATION": "/wEWCgKCu+TwDgL2sNicBgKXsNDICALLn/r/AQLon/KrAgL64auvDwKb4aObAQLfyNWPCgL8yM37DAL074zzDRwc6rsnM/1ErlY7oO8HUz+sgDyYpperRBqzHVo6rudL",
        "_ctl11:ddlSterm": "{}/{}/1 0:00:00".format(year+semester-1, 15-semester*6),
        "_ctl11:btnSearch": "确定"
    }
    url = "http://jwc.jxnu.edu.cn/MyControl/All_Display.aspx?UserControl=Xfz_Kcb.ascx&UserType=Student&UserNum={}".format(stuNum)
    html = postHtmlText(url, data, 'UTF-8')
    # 获取课程表信息
    ScheduleInfo = []
    table = re.search(r'<div id=\"_ctl11_NewKcb\">(.*?)</div>', html, re.S).group(1)
    trs = re.findall(r'<TR>(.*?)</TR>', table, re.S)
    del trs[0]
    del trs[-1]
    for tr in trs:
        trInfo = []
        tr = tr.replace('\t', '').replace('\r', '').replace('\n', '').replace('<BR>', '').replace(' ', '').replace('&nbsp;', '')
        tds = re.findall(r'<TD.*?>(.*?)</TD>', tr, re.S)
        del tds[0]
        for td in tds:
            # tdInfo = re.findall(r'<DIV.*?>(.*?)</DIV>', td, re.S)[0].split('<br>')
            Infos = re.findall(r'<DIV.*?>(.*?)</DIV>', td, re.S)[0].split('、')
            for i in range(len(Infos)):
                Infos[i] = Infos[i].split('<br>')
            tdInfo = Infos
            # tdInfo = re.findall(r'<DIV.*?>(.*?)</DIV>', td, re.S)[0].replace('<br>', '')
            if not (tdInfo[0][0].isdigit() or tdInfo[0][0] == '晚'):
                trInfo.append(tdInfo)
        ScheduleInfo.append(trInfo)
    # 将1、2节，6、7节，8、9节以及晚上的被合并的课程拆开
    ScheduleInfo.insert(1, ScheduleInfo[0])
    ScheduleInfo.insert(6, ScheduleInfo[5])
    ScheduleInfo.insert(8, ScheduleInfo[7])
    ScheduleInfo.insert(10, ScheduleInfo[9])
    # with open('./scheduleInfo.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(ScheduleInfo, ensure_ascii=False))
    # 获取课程列表
    lessons = []
    table = re.search(r'<table.*?id=\"_ctl11_dgStudentLesson\".*?>(.*?)</table>', html, re.S).group(1)
    trs = re.findall(r'<tr style="color:#330099;background-color:White;">(.*?)</tr>', table, re.S)
    for tr in trs:
        tds = re.findall(r'<td>(.*?)</td>', tr, re.S)
        lesson = {}
        lesson["course_id"] = tds[0].replace(' ', '')
        lesson["course_name"] = tds[1]
        lesson["course_class_name"] = tds[2].replace(' ', '')
        lesson["teacher_name"] = tds[3]
        course_class_id = re.findall(r'bjh=(.*?)&', tds[4], re.S)[0]
        lesson["course_class_id"] = course_class_id
        lesson["course_class_roster_url"] = \
            "http://jwc.jxnu.edu.cn/MyControl/All_Display.aspx?UserControl=Xfz_Class_student2.ascx&bjh={}&kch={}&xq={}/{}/1"\
                .format(lesson["course_class_id"], lesson["course_id"], year+semester-1, 15-semester*6)
        lessons.append(lesson)

    # with open('./lesson.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(lessons, ensure_ascii=False))

    # 制作json格式的课程表信息
    Schedule = []
    for i in range(len(ScheduleInfo)):
        for j in range(len(ScheduleInfo[i])):
            for course in ScheduleInfo[i][j]:
                if len(course) > 1:
                    course_name = course[0]
                    course_address = course[1].replace('(', '').replace(')', '')
                    week = j + 1
                    begin_at = i + 1
                    class_hour = 1
                    for k in range(i + 1, len(ScheduleInfo)):
                            for l in range(len(ScheduleInfo[k][j])):
                                if len(ScheduleInfo[k][j][l]) > 1 \
                                        and course_name == ScheduleInfo[k][j][l][0] \
                                        and course_address == ScheduleInfo[k][j][l][1].replace('(', '').replace(')', ''):
                                    class_hour += 1
                                    ScheduleInfo[k][j][l] = [""]
                    for k in range(len(lessons)):
                        if lessons[k]["course_name"] == course_name:
                            class_info = lessons[k].copy()
                            class_info["course_address"] = course_address
                            class_info["week"] = week
                            class_info["begin_at"] = begin_at
                            class_info["lessons"] = class_hour
                            Schedule.append(class_info)


    # 写入json课程表
    with open('./Schedule.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(Schedule, ensure_ascii=False))
    print(Schedule)
    return Schedule



if __name__ == '__main__':
    getSchedule(201626703044, 2019, 1)
    # print(sys.argv)
    # if len(sys.argv) == 4:
    #     try:
    #         stuNum = int(sys.argv[1])
    #         year = int(sys.argv[2])
    #         semester = int(sys.argv[3])
    #         getSchedule(stuNum, year, semester)
    #     except:
    #         print('parameter error!')
    # else:
    #     print('parameter false!')
