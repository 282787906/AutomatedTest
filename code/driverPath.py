from selenium.webdriver.chrome import webdriver

options = webdriver.ChromeOptions()
# 指定驱动
driver_path = "D:\pyauto_driver\chromedriver.exe"
driver = webdriver.Chrome(driver_path, options = options)
# 不指定驱动
# driver = webdriver.Chrome(options = options)
print(driver.title)