import json
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def webdriver_init():
    print ("Initializing hub .....")
    SELENIUM_HUB = 'http://172.18.0.3:4444/wd/hub'
    PROXY = '172.18.0.2:8118'
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "noProxy": None,
        "proxyType": "MANUAL",
        "class": "org.openqa.selenium.Proxy",
        "autodetect": False
    }
    driver = webdriver.Remote(
            command_executor=SELENIUM_HUB,
            desired_capabilities=DesiredCapabilities.CHROME,
        )
    print ("Driver initalized...")
    return driver

def webdriver_del(driver):
    driver.close()

valid_data = lambda v: v[0] if len(v) > 0 else None


driver = webdriver_init()
driver.get("https://check.torproject.org/api/ip")
print "CHECK IP LEAK:"
doc = html.fromstring(driver.page_source)
ip_check = valid_data(doc.xpath("//pre/text()"))
if ip_check:
    try:
        ip_check = json.loads(ip_check)
        print "IP:",ip_check.get("IP")
    except:
        print "IP:",driver.page_source
else:
    print "IP:",driver.page_source
driver.get("https://www.dnsleaktest.com/")
print "CHECK DNS LEAK:"
doc = html.fromstring(driver.page_source)
dns_leak_ip = valid_data(doc.xpath("//div[@class='welcome']/p[1]/text()"))
dns_leak_region = valid_data(doc.xpath("//div[@class='welcome']/p[2]/text()"))
if dns_leak_ip:
    dns_leak_ip = dns_leak_ip.replace("Hello ","")
print "IP:",dns_leak_ip
print "REGION:",dns_leak_region
webdriver_del(driver)
