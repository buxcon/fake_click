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
	browser.set_page_load_timeout(30)
	browser.set_script_timeout(30)
	proxy_option = webdriver.Proxy()
	proxy_option.proxy_type = ProxyType.MANUAL
	proxy_option.http_proxy = proxy
	proxy_option.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
	try:
		browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
		browser.get('http://www.baidu.com/')
		print('通过代理%s打开了百度首页'%(proxy))
		time.sleep(random.uniform(0, 2))
		browser.maximize_window()
		for character in '配置lucene':
			browser.find_element_by_id('kw').send_keys(character)
			time.sleep(random.uniform(0, 0.5))
		browser.find_element_by_id('su').click()
		print('通过代理%s执行了搜索'%(proxy))
		#模拟浏览最终打开目标页面
		while (True):
			#模拟浏览
			print('正在通过代理%s进行模拟浏览'%(proxy))
			scroll_count = 0
			while (scroll_count < random.randint(1, 5)):
				js = 'document.body.scroll'
				if (random.randint(0, 1) == 0) :
					direction = 'Bottom'
				else :
					direction = 'Top'
				browser.execute_script('%s%s = %d'%(js, direction, random.randint(200, 500)))
				time.sleep(random.uniform(1, 2))
				scroll_count += 1
			#寻找目标页面
			results = browser.find_elements_by_class_name('result')
			target = None
			for result in results:
				if ('weaine' in result.find_element_by_class_name('c-showurl').text):
					target = result
			if target is None:
				for link in browser.find_elements_by_xpath("//div[@id='page']/a"):
					if '下一页' in link.text:
						link.click()
				time.sleep(5)
			else:
				target.find_element_by_xpath('h3/a').click()
				print('通过代理%s打开了目标网页'%(proxy))
				time.sleep(random.uniform(45, 120))
				break
		browser.quit()
		print('已通过代理%s模拟了一次搜索点击'%(proxy))
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
			thread.join(180)
		threads = []

if __name__ == '__main__':
	main()