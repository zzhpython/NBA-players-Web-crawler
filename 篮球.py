import csv
import re,os,time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

#返回列表0:想要的字符1:下标位置后
#s_tr字符串头ed尾
def strfml(dta,s_tr,ed="<",hst=0,ind=0):
  hst=dta.find(s_tr,hst)
  if hst<0:
    return ["",-1]
  hst+=len(s_tr)+ind
  tag=dta.find(ed,hst)
  return [dta[hst:tag],tag]

def we(x,y,z="w",n="",ecd=None,tis=True,r=None):
  msg=""
  iscsv=False
  try:
    if r:
      text=r
    elif z.find("b")<0:
      text=open(x,z,newline=n,encoding=ecd)
      if x[x.rfind("."):]==".csv":
        iscsv=True
        csv_w = csv.writer(text)
        csv_w.writerows(y)
        y=[]
    else:
      text=open(x,z)
    if not iscsv:
      text.write(y)
      y=""
    if not r:
      text.close()
    msg="数据更新:"+x
  except Exception as e:
    msg="更新失败:"+str(e)
  if tis:print(msg)
  return y

# 自定义find_element
def nfind_element(driver: uc,by, value,n=1):
    element=None
    while n:
      if n>0:n-=1
      try:
        element = WebDriverWait(driver, 1.4).until(EC.presence_of_element_located((by, value)))
        break
      except:1
    return element


def get_driver(hide=10,poxy=None,down=None,hads=None,udr=False,ismax=False,ddir=dir,inco=None,iscaps=False):
  chrome_options = uc.ChromeOptions()
  #chrome_options.add_argument('--user-data-dir=%s' %dir[0]) #用户配置
  #chrome_options.add_argument("--disable-extensions")  #禁用扩展程序
  chrome_options.add_argument("--disable-popup-blocking") #允许弹窗
  chrome_options.add_argument("--profile-directory=Default")
  chrome_options.add_argument("--ignore-certificate-errors")
  chrome_options.add_argument("--disable-plugins-discovery")
  #chrome_options.add_argument("--incognito") #无痕模式
  chrome_options.add_argument('--no-first-run')
  chrome_options.add_argument('--no-service-autorun')
  chrome_options.add_argument('--no-default-browser-check')
  chrome_options.add_argument('--password-store=basic')
  
  chrome_options.add_argument('--no-sandbox')
  
  #prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': tmp}
  chrome_options.add_experimental_option("prefs", {
  "credentials_enable_service":False,
  "profile.password_manager_enabled":False,
  'profile.default_content_setting_values':
        {
            'notifications': 2
        }
  }) ##关掉密码弹窗  exit_type未正常退出提示框
  chrome_options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug

   # hide=1则隐藏，为其他值则显示浏览器页面
  if udr:
    chrome_options.add_argument('--user-data-dir=%s' %ddir[0]) #用户配置
  if down: #默认下载路径
    chrome_options.add_experimental_option("prefs", {'profile.default_content_settings.popups': 0, 'download.default_directory': down})
  if hide == 1:
    #chrome_options.add_argument("--window-size=1600,800")
    #chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless')
  if ismax:
    chrome_options.add_argument("--start-maximized")
  if inco:
    chrome_options.add_argument("--incognito")
  #ip="http://101.34.72.57:7890"

  if poxy:
    print("当前代理为:",poxy)
    chrome_options.add_argument('--proxy-server=%s'%poxy) 

  #caps = None
  if iscaps:
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})
    #caps={"goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}}

  #chrome_options.add_argument('--user-agent=%s' %UserAgent().random)
  
  headers='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
  if hads:
    headers=hads
  chrome_options.add_argument('--user-agent=%s'%headers)
  #加标头文件解决无头模式没内容
  chrome_options.binary_location = ddir[2]
  browser = uc.Chrome(options=chrome_options,driver_executable_path=ddir[1])
  #browser.delete_all_cookies()
  
  #browser.set_window_size(400, 400) 
  #截图看看无头加载没
  #browser.save_screenshot("tmsf.png")
  '''browser.maximize_window()'''

  return browser



def getresponse(browser,urlkds=None,types=None):
  performance_log = browser.get_log('performance')  # 获取名称为 performance 的日志
  for i in range(len(performance_log)):
    message = performance_log[i].get('message') # 获取message的数据
    if strfml(message,'method','"',ind=3)[0] != 'Network.responseReceived':  # 如果method 不是 responseReceived 类型就不往下执行
      continue
    packet_type = strfml(message,'mimeType','"',ind=3)[0]  # 获取该请求返回的type
    _types = [
      'application/javascript', 'application/x-javascript', 'text/css', 'webp', 'image/png', 'image/gif',
      'image/jpeg', 'image/x-icon', 'application/octet-stream'
    ]
    if types and (packet_type not in types): 
        continue
    elif packet_type in _types: #过滤type
        continue

    _url = strfml(message,'"url"','"',ind=2)[0]  # 获取 该请求  url
    requestId = strfml(message,'requestId','"',ind=3)[0]  # 唯一的请求标识符。相当于该请求的身份证
    if _url.find(urlkds)>-1:
      #print(f'type: {requestId} _url: {_url}')
      try:
        res=browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})["body"]  # selenium调用 cdp
        return res
      except:
        getresponse(browser,urlkds)
      



def getdata(browser,pg):
  pm=(pg-1)*50
  lrows=[]
  time.sleep(1.3)
  resp=None
  while not resp:
    
    resp=getresponse(browser,"playerstats?")
    time.sleep(0.5)
    print("等待数据返回")

  idx=json.loads(resp)
  for i in idx["data"]["player"]["Data"]:
    ls=["" for i in rls]
    pm+=1
    ls[rls.index("排名")]=pm
    ls[rls.index("球员姓名")]=i["Player"]["displayName"]
    ls[rls.index("球队")]=i["Team"]["name"]
    ls[rls.index("比赛场次")]=i["Games"]
    ls[rls.index("出场时间")]=i["Minspg"]
    ls[rls.index("得分")]=i["Pointspg"]
    ls[rls.index("篮板")]=i["Rebspg"]
    ls[rls.index("助攻")]=i["Assistspg"]
    ls[rls.index("抢断")]=i["Stealspg"]
    ls[rls.index("盖帽")]=i["Blockspg"]
    ls[rls.index("投篮命中率")]="{}%".format(i["Fgpct"])
    ls[rls.index("三分命中数")]=i["Tpm"]
    ls[rls.index("三分命中率")]="{}%".format(i["Tppct"])
    ls[rls.index("罚球命中率")]="{}%".format(i["Ftpct"])
    lrows.append(ls)
    print(ls)
  return lrows


def main(browser):
  
  pg=0
  rows=[rls]
  while 1:
    
    pg+=1
    div=nfind_element(browser, By.XPATH,'//*[@id="app"]//section[1]/ul',n=-1)
    a_ls=browser.execute_script('return arguments[0].getElementsByTagName("li");', div)
    _error=1
    for next in a_ls:
      if next.text.strip()==str(pg):
        print("下页",pg)
        browser.execute_script('arguments[0].click()',next)
        time.sleep(0.3)
        nfind_element(browser, By.XPATH,'//*[@id="app"]//section[1]/ul',n=-1)
        _error=0
        break
      
    
    if _error:
      we("数据.csv",rows,ecd="u8")
      break
    
    time.sleep(0.3)
    ls=getdata(browser,pg)
    rows.extend(ls)

if __name__ == '__main__':
  dir=["" for i in range(3)]
  dir[1]="运行库\\chromedriver.exe"
  dir[2]=os.getcwd() +"\\运行库\\chrome.sync\\Chrome-bin\\chrome1.exe"
  browser=get_driver(ddir=dir,iscaps=1)
  browser.get("https://china.nba.cn/statistics/playerstats")
 

  rls=["排名","球员姓名","球队","比赛场次","出场时间","得分","篮板","助攻","抢断","盖帽","投篮命中率","三分命中数","三分命中率","罚球命中率"]
  main(browser)
  print("全部完成")
  
  
