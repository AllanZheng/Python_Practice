import codecs
import csv
import sys
from datetime import datetime
from StockAnalysis import data_struct
import matplotlib.pyplot as plt
import numpy as np
import requests




url = 'http://api.waizaowang.com/doc/getDayKLine'

def GetData(startdate,enddate,type,code):
    param = {
        'code': code,
        'type': type,
        'startDate':startdate,
        'endDate':enddate,
        'stockType':0,
    }
    res = requests.get(url,params=param)

    resdata = res.text.split("\n")
    DataList = []
    syspath = sys.path[0]
    filename = syspath+"\\data\\"+startdate+"-"+enddate+"-"+code+".csv"
    f = open(filename,'w+',encoding='utf-8-sig')
    writer = csv.writer(f)
    writer.writerow("股票代码,股票名称,交易市场,交易日,开盘价,收盘价,最高价,最低价,成交量（单位手）,成交额（单位万元）,换手率".split(","))
    for i in resdata:
        column = i.split(",")
        writer.writerow(column)
        record = data_struct.stockdata(datetime.strptime(column[3],"%Y-%m-%d").weekday(),True,column[0],column[1],column[3])
        if float(column[5])-float(column[4])>0.0:
            record.IsIncrease = True
        else:
            record.IsIncrease = False
        DataList.append(record)
    f.close()
    name = startdate+"-"+enddate+"-"+code
    return DataList,name

#统计与画图
def SatisticWeekDay(data:[data_struct.stockdata],name:str):
    Weekday =("Mon","Tue","Wed","Thur","Fri")
    IncRes =[0,0,0,0,0]
    DescRes =[0,0,0,0,0]
    if len(data)<=0:
        return
    for i in data:
        if i.IsIncrease:
            IncRes[i.Weekday]+=1
        else:
            DescRes[i.Weekday]+=1
    bar_width = 0.3  # 条形宽度
    Inc = np.arange(len(IncRes))  # 涨的横坐标
    Desc = Inc + bar_width  # 跌的横坐标
    plt.rcParams['font.sans-serif'] = 'simhei'
    # 使用两次 bar 函数画出两组条形图
    plt.bar(Inc, height=IncRes, width=bar_width, color='r', label='涨')
    plt.bar(Desc, height=DescRes, width=bar_width, color='g', label='跌')
    plt.legend()  # 显示图例
    for i in range(len(IncRes)):
        plt.text(Inc[i]-0.1, IncRes[i] + IncRes[i]/30, "%s" % IncRes[i],va ='center')
    for i in range(len(DescRes)):
        plt.text(Desc[i]-0.1, DescRes[i] + DescRes[i]/30, "%s" % DescRes[i],va = 'center')
    plt.xticks(Inc + bar_width / 2, Weekday)  # 让横坐标轴刻度显示星期， Inc + bar_width / 2 为横坐标轴刻度的位置
    plt.ylabel('天数')  # 纵坐标轴标题
    title = name+'星期涨跌统计'
    plt.title(title)
    jpgfilename = './'+'graph'+'\\'+name+'.jpg'
    plt.savefig(jpgfilename)
    plt.show()
    return

#统计与画图
def SatisticDoubleDay(data:[data_struct.stockdata],name:str):
    Weekday =("Mon","Tue","Wed","Thur","Fri")
    IncRes =[0,0,0,0,0]
    ContInc = [0,0,0,0,0]
    DescRes =[0,0,0,0,0]
    ContDesc = [0,0,0,0,0]
    for i in range(len(data)):
        if  i==len(data)-1:
            continue
        d = data[i]
        if d.IsIncrease :
            if data[i + 1].IsIncrease:
                ContInc[d.Weekday]+=1
            #
            IncRes[d.Weekday] += 1
        else:
            if not data[i+1].IsIncrease:
                ContDesc[d.Weekday] += 1
            DescRes[d.Weekday] += 1
            #else:


    bar_width = 0.2  # 条形宽度
    ContI = np.arange(len(ContInc))# 涨的横坐标
    Inc = ContI  +bar_width
    ContD = Inc+ bar_width
    Desc = ContD + bar_width  # 跌的横坐标
    plt.rcParams['font.sans-serif'] = 'simhei'
    # 使用四次 bar 函数画出四组条形图
    plt.bar(ContI, height=ContInc, width=bar_width, color='r', label='连涨')
    plt.bar(Inc, height=IncRes, width=bar_width, color='y', label='涨')
    plt.bar(ContD, height=ContDesc, width=bar_width, color='g', label='连跌')
    plt.bar(Desc, height=DescRes, width=bar_width, color='b', label='跌')
    plt.legend()  # 显示图例
    for i in range(len(ContInc)):
        plt.text(ContI[i] - 0.1, ContInc[i] + ContInc[i] / 30, "%s" % ContInc[i], va='center')
    for i in range(len(IncRes)):
        plt.text(Inc[i] - 0.1, IncRes[i] + IncRes[i] / 30, "%s" % IncRes[i], va='center')
    for i in range(len(ContDesc)):
        plt.text(ContD[i] - 0.1, ContDesc[i] + ContDesc[i] / 30, "%s" % ContDesc[i], va='center')
    for i in range(len(DescRes)):
            plt.text(Desc[i] - 0.1, DescRes[i] + DescRes[i] / 30, "%s" % DescRes[i], va='center')
    plt.xticks(Inc + bar_width, Weekday)  # 让横坐标轴刻度显示星期， Inc + bar_width / 2 为横坐标轴刻度的位置
    plt.ylabel('天数')  # 纵坐标轴标题
    title = name + '星期连续两天涨跌统计'
    plt.title(title)
    jpgfilename = './'+'graph'+'\\' + name + '.jpg'
    plt.savefig(jpgfilename)
    plt.show()
    return

data,name = GetData('2000-01-01','2021-01-31',1,'000001')
#SatisticWeekDay(data,name)
SatisticDoubleDay(data,name)