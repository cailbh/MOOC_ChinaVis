import json
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import requests
import cv2
import numpy
from browsermobproxy import Server
import os

# session_requests = requests.session()
#
# login_url = "https://pintia.cn/auth/login"
# result = session_requests.get(login_url)
#
# print(result.text)
# D:\browsermob-proxy-2.1.4\browsermob-proxy.bat
# 开启代理
BMPserver = Server(r'D:\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
BMPserver.start()
BMPproxy = BMPserver.create_proxy()

# 配置代理启动webdriver
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--proxy-server={}'.format(BMPproxy.proxy))

web = webdriver.Chrome(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe', options=chrome_options)
# web.implicitly_wait(5)


# 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
web.get('https://pintia.cn/auth/login')
zh = web.find_element_by_xpath('//*[@id="username"]')
mm = web.find_element_by_xpath('//*[@id="password"]')
print(zh)
zh.send_keys('zhgzhou@hdu.edu.cn')
mm.send_keys('zhou@123456')
web.find_element_by_xpath('//*[@class="pc-text-raw ellipsis"]').click()
web.find_element_by_xpath('//*[@class="pc-text-raw ellipsis"]').click()
for i in range(5):
    # 等待一会，时间间隔可根据网速调整，验证码加载完成
    time.sleep(10)

    print('当前url:' + web.current_url)
    # 如果当前url没变说明验证未通过，循环5（可修改）次重新验证
    if web.current_url != 'https://pintia.cn/auth/login':
        break
    # bg背景图片
    bg_img_src = web.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[1]').get_attribute('src')
    # front可拖动图片
    front_img_src = web.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[2]').get_attribute('src')

    # 保存图片
    with open("bg.jpg", mode="wb") as f:
        f.write(requests.get(bg_img_src).content)
    with open("front.jpg", mode="wb") as f:
        f.write(requests.get(front_img_src).content)

    # 将图片加载至内存
    bg = cv2.imread("bg.jpg")
    front = cv2.imread("front.jpg")

    # 将背景图片转化为灰度图片，将三原色降维
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    # 将可滑动图片转化为灰度图片，将三原色降维
    front = cv2.cvtColor(front, cv2.COLOR_BGR2GRAY)
    front = front[front.any(1)]
    # 用cv算法匹配精度最高的xy值
    result = cv2.matchTemplate(bg, front, cv2.TM_CCOEFF_NORMED)
    # numpy解析xy，注意xy与实际为相反，x=y,y=x
    x, y = numpy.unravel_index(numpy.argmax(result), result.shape)
    # 找到可拖动区域
    div = web.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]')
    # 拖动滑块，以实际相反的y值代替x
    ActionChains(web).drag_and_drop_by_offset(div, xoffset=y // 0.946, yoffset=0).perform()
    # 至此成功破解验证码，由于算法问题，准确率不能达到100%，所以加了循环判断
time.sleep(3)

# url = 'https://pintia.cn/problem-sets/1601015996159377408/submissions'
# response = requests.get(url)
# data = response.content
# print(data)
#
# url1 = 'https://pintia.cn/api/problem-sets/1601015996159377408/submissions?limit=50&filter=%7B%7D'
# response1 = requests.get(url1)
# data1 = response1.content
# print(data1)
# da = [data1]
# # print(subw)

# 获取返回内容
url = "https://pintia.cn/problem-sets/1601015996159377408/submissions"
# BMPproxy.new_har("video", options={'captureHeaders': True, 'captureContent': True})

# 模拟浏览器
BMPproxy.new_har("video", options={'captureHeaders': True, 'captureContent': True})
web.get(url)
# time.sleep(3)
# web.find_element_by_xpath('//*[@id="kw"]').send_keys("python")
# web.find_element_by_xpath('//*[@id="su"]').click()
# time.sleep(3)
json_data = BMPproxy.har
# print(json_data)
result = BMPproxy.har
content = []
res = {}
for entry in result['log']['entries']:
    _url = entry['request']['url']
    if "https://pintia.cn/api/problem-sets/1601015996159377408/submissions?limit=50&filter=%7B%7D" in entry['request'][
        'url']:
        content = entry['response']['content']
        res = entry
# 将json数据存储到本地
result_json = res
# result_json = json.dumps(res, indent=4)
print(result_json)
print(result_json['request'])
# print(res.json())
# result_json = res.json()
# with open("baidu.json", "w", errors="igone", encoding="utf-8") as f:
#     f.write(result_json)
# 1601015996159377408

final_result = []
url = "https://pintia.cn/api/problem-sets/1601015996159377408/submissions"
# url = result_json['request']['url']
parms02 = {
    'limit': '200'
}
headers = result_json['request']['headers']
head = {}
for h in headers:
    head[h['name']] = h['value']
ret = requests.get(url, params=parms02, headers=head)
cur_rel = ret.json()['submissions']
cont = 0
for s in cur_rel:
    curl = "https://pintia.cn/api/submissions/" + s['id'] + "?"
    parms = {
        'limit': '200'
    }
    time.sleep(0.5)
    cret = requests.get(curl, params=parms, headers=head)
    print(cont)
    cont += 1
    final_result.append(cret.json()['submission'])

fid = cur_rel[199]['id']
i = 200
while i == 200:
    url = "https://pintia.cn/api/problem-sets/1601015996159377408/submissions?before=" + fid
    # url = result_json['request']['url']
    parms02 = {
        'limit': '200'
    }
    headers = result_json['request']['headers']
    head = {}
    for h in headers:
        head[h['name']] = h['value']
    ret = requests.get(url, params=parms02, headers=head)
    cur_rel = ret.json()['submissions']
    for s in cur_rel:
        curl = "https://pintia.cn/api/submissions/" + s['id'] + "?"
        parms = {
            'limit': '200'
        }
        time.sleep(0.5)
        cret = requests.get(curl, params=parms, headers=head)
        print(cont)
        cont += 1
        final_result.append(cret.json()['submission'])
    if len(cur_rel) < 200:
        break
    else:
        fid = cur_rel[199]['id']

with open("baidu.json", "w", errors="igone", encoding="utf-8") as f:
    f.write(json.dumps(final_result, indent=4, ensure_ascii=False))
#
# BMPserver.stop()
# web.quit()
