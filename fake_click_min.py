import time
import random
import httplib2
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import ProxyType

def exec(proxy):
	#模拟手工打开浏览器提交搜索
	#options = webdriver.ChromeOptions()
	#options.add_argument('--proxy-server=http://' + proxy)
	#browser = webdriver.Chrome('chromedriver.exe', chrome_options = options)
	browser = webdriver.PhantomJS(executable_path = 'phantomjs.exe')
	browser.set_page_load_timeout(10)
	browser.set_script_timeout(10)
	proxy_option = webdriver.Proxy()
	proxy_option.proxy_type = ProxyType.MANUAL
	proxy_option.http_proxy = proxy
	proxy_option.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
	try:
		browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
		browser.get('http://www.baidu.com/')
		print('通过代理%s打开了百度首页'%(proxy))
		browser.maximize_window()
		for character in '配置lucene':
			browser.find_element_by_id('kw').send_keys(character)
		browser.find_element_by_id('su').click()
		print('通过代理%s执行了搜索'%(proxy))
		time.sleep(5)
		#模拟浏览最终打开目标页面
		for i in range(0, 10):
			#模拟浏览
			results = browser.find_elements_by_class_name('result')
			target = None
			for result in results:
				if 'weaine' in result.find_element_by_class_name('c-showurl').text:
					target = result
			if target is None:
				for link in browser.find_elements_by_xpath("//div[@id='page']/a"):
					if '下一页' in link.text:
						link.click()
				time.sleep(5)
			else:
				target.find_element_by_xpath('h3/a').click()
				print('通过代理%s打开了目标网页'%(proxy))
				time.sleep(5)
				break
			if i == 9:
				print('通过代理%s的搜索未找到目标页面'%(proxy))
		browser.quit()
	except:
		browser.quit()
		print('通过代理%s的连接出现错误'%(proxy))

def main():
	while (True):
		conn = httplib2.Http()
		resp, content = conn.request('http://vtp.daxiangdaili.com/ip/?tid=558491667144729&num=1&filter=on')
		threads = []
		for addr in content.split():
			threads.append(threading.Thread(target = exec, args=(addr.decode(encoding = 'utf-8'),)))
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join(120)
		threads = []

if __name__ == '__main__':
	main()