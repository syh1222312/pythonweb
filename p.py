import traceback
from selenium import webdriver
from lxml import etree
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv


url_fre = 'https://nanjing.newhouse.fang.com/house/s/'
# 创建一个driver对象
driver = webdriver.Chrome()

positions = []


def spider(url):
    """获取主页信息"""
    # 访问
    driver.get(url)
    while True:
        # 拿到网页源代码
        source = driver.page_source
        # 获取当前窗口的句柄
        listA_win = driver.window_handles

        # 获取
        html = etree.HTML(source)
        if html is not None:
          links = html.xpath('//div[@class="nlcd_name"]/a[@target="_blank"]/@href')
        else:
            continue
        # 访问当前页面之后，还需要翻页
        for index, link in enumerate(links):
            print(link)
            detail(link)

        break


def detail(url):
    """详情页信息"""
    # 打开新的页面
    driver.execute_script('window.open("%s")' % url)
    driver.switch_to.window(driver.window_handles[1])

    try:
        WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="firstbox"]'))
        )
        # 信息获取
        source = driver.page_source
        get_detail_info(source)
        # 页面关闭
        driver.close()
        # 返回原始窗口的句柄
        driver.switch_to.window(driver.window_handles[0])
    except:
        traceback.print_exc()
        time.sleep(2)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


def get_detail_info(source):
    """获取信息"""
    html = etree.HTML(source)
    name = html.xpath('//div[@class="tit clearfix"]//strong/text()')[0]
    try:
        address = html.xpath('//div[@id="xfptxq_B04_12"]/span/text()')[0]
    except:
        address = ''
    rooms = html.xpath('//div[@id="xfptxq_B04_13"]//a/text()')
    prices = html.xpath('//div[@class="price_line clearfix"]//span/text()')
    # print('价格数量：', len(prices))
    price = prices[0] + "元/m^2"
    total_price = None
    if len(prices) > 1:
        total_price = prices[1] + "万元"

    phone = html.xpath('//div[@id="xfptxq_B02_01"]//span[1]/text()')[0]
    print(name)
    position = {
        'name': name,
        'address': address,
        'rooms': rooms,
        'price': price,
        'total_price': total_price,
        'phone': phone
    }
    print(position)
    positions.append(position)
    # time.sleep(random.randint(2, 7))  # 很急睡不了一点

def writer_csv():
    """保存数据成csv格式"""
    headers = ['name', 'address', 'rooms', 'price', 'total_price', 'phone']
    with open('/Users/sheyunhan/PycharmProjects/pythonweb/nanjing.csv', 'a') as fp:
        writer = csv.DictWriter(fp, headers)
        writer.writeheader()
        writer.writerows(positions)


if __name__ == '__main__':
    for i in range(1, 30):  # 46 ,45最后一页
        print(i)
        add = 'b9{}/'
        url = url_fre + add.format(i)
        print(url)
        spider(url)
        print('=' * 40)
    print('爬虫程序结束')
    writer_csv()
    print('写入csv文件结束')

