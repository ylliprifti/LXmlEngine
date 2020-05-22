from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://www.checkatrade.com/trades/WayreHouseElectricalServices/reviews")
elem = driver.find_element_by_xpath("__NEXT_DATA__")
print(elem.get_attribute('innerHTML'))

driver.close()

if __name__ == "__main__":
    pass
