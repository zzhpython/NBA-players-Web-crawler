


import os,time,json,random
import re,csv
import matplotlib.pyplot as plt
import numpy as np





def getyls(svp,k1,kds):
  with open(svp,"r",newline='',encoding="u8") as f:
    data=csv.reader(f)
    fst=True
    for row in data:
      if fst:
        fst=False
        continue
      
      x="%s:%s" %(row[2],row[1])
      isyou=False
      for j in k1:
        if j[0]==x:
          isyou=True
          break
      if not isyou:
        y=float(row[rls.index(kds)].replace("%",""))
        k1.append([x,y])
  


  


def main(kds):
  k1=[]
  getyls(svp,k1,kds)
  #排序
  l=len(k1)
  for i in range(0,l):
    for j in range(0,l-i-1):
      if k1[j][1]<k1[j+1][1]:
        tmp=k1[j]
        k1[j]=k1[j+1]
        k1[j+1]=tmp
  ##横坐标名字
  x=[]
  ##纵坐标
  y=[]

  
  for i in k1[0:10]:
    x.append(i[0])
    y.append(i[1])
  
  #柱形图
  total_width, n= 1,10   # 有多少个类型，只需更改n即可
  width = total_width / (n*0.3)
  #重置以下
  plt.figure()
  plt.bar(x, y, color = "#5a98ff",width=width,label='数值')
  # 在每个柱子上添加数值标签
  for i in range(10):
      plt.text(i, y[i], str(y[i]), ha='center', va='bottom')
  plt.xlabel("前10球员")
  plt.ylabel(kds)
  plt.legend(loc = "best")
  plt.xticks(rotation=60)
  plt.tight_layout() 
  plt.savefig(kds+'top10柱形图.jpg')
  print("保存：%stop10柱形图.jpg" %kds)

if __name__ == '__main__':
  rls=["排名","球员姓名","球队","比赛场次","出场时间","得分","篮板","助攻","抢断","盖帽","投篮命中率","三分命中数","三分命中率","罚球命中率"]
  
  plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
  plt.rcParams["axes.unicode_minus"]=False #正常显示负号
  svp="数据.csv"
  
  main("得分")
  main("助攻")
  main("篮板")
  main("三分命中率")
  input("全部完成")





