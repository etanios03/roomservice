import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import csv

#initializing
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options = options)
url = "https://coursesearch92.ais.uchicago.edu/psc/prd92guest/EMPLOYEE/HRMS/c/UC_STUDENT_RECORDS_FL.UC_CLASS_SEARCH_FL.GBL"
driver.get(url)

#random initializations
output = []
filepath = '/Users/arnavagarwal/Desktop/Arnav/University/Year 2/Q3/Hackathon/webscrape.csv'

#identifying department dropdown
select = Select(driver.find_element(By.ID, 'UC_CLSRCH_WRK2_SUBJECT'))
options = select.options
wait = WebDriverWait(driver, 30)

#loop start and end
start = 40
end = len(options) - 1
count = 675

#SPECIAL HANDLING: In the case of really large subjects
#end = start+1

for index in range(start, end):
    select = Select(driver.find_element(By.ID, 'UC_CLSRCH_WRK2_SUBJECT'))
    select.select_by_index(index)
   
    search = wait.until(EC.element_to_be_clickable((By.ID, "UC_CLSRCH_WRK2_SEARCH_BTN")))
    search.click()

    time.sleep(3)

    #identifying number of classes returned
    results = wait.until(EC.presence_of_element_located((By.ID, 'UC_RSLT_NAV_WRK_PTPG_ROWS_GRID'))).text
    classcnt = int(results.split(" ")[0])
    flag = 1

    while (flag):
        #iterating through classes table
        mytable = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="win0divDESCR100$grid$0"]/table')))
        rows = mytable.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            #clicking class
            rows = mytable.find_elements(By.TAG_NAME, 'tr')
            driver.execute_script('arguments[0].click()', row)

            #saving info
            time.sleep(2)
            info = str(driver.find_element(By.XPATH, '//*[@id="win0divSSR_CLSRCH_MTG1$grid$0"]/table').text)
            lst = info.split("\n")
            
            #parser
            
            # Extract days and start/end times
            daytime = lst[1].split(" : ")
            
            if len(daytime) > 1:
                # Split days, start time and end time
                days, times = daytime[0].split(" "), daytime[1].split("-")
                stime, etime = times[0], times[1]
            else:
                # If time is TBA, set days, start time and end time to TBA as well
                days, stime, etime = "TBA", "TBA", "TBA"
                
            # Extract building and room
            place = lst[3]  
            room = [int(i) for i in place.split() if i.isdigit()]
            
            if len(room) > 0: 
                room = str(room[0])
                building = place.replace(room, "")[:-1]
            else:
                building, room = "TBA", "TBA"
            
            if isinstance(days, list):
                for day in days:
                    output = [building, room, day, stime, etime]
            else:
                output = [building, room, days, stime, etime]
                
            # Open CSV file in write mode
            with open(filepath, 'a', newline='') as file:

                # Create a CSV writer object
                writer = csv.writer(file)

                # Write the list to the CSV file as a row
                writer.writerow(output)

            #tracker
            count += 1
            classcnt -= 1
            print("Total Count:"+str(count)+", Current Remaining:"+str(classcnt))

            #going back
            back = wait.until(EC.element_to_be_clickable((By.ID, "UC_CLS_DTL_WRK_RETURN_PB$0")))
            back.click()
            time.sleep(2)
        
        if(classcnt > 0):
            #next page
            nextp = wait.until(EC.element_to_be_clickable((By.ID, "UC_RSLT_NAV_WRK_SEARCH_CONDITION2")))
            nextp.click()
            time.sleep(2)
        else: 
            flag = 0


    