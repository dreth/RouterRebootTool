import json
from re import M
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from platform import system as current_os_name
from platform import architecture as current_arch
from time import sleep

# open json
with open('private.json', 'r') as f:
    data = json.load(f)
    paths = data['path']
    address = data['address']
    mode = data['headless'].capitalize()
    driver = data['driver']
    os_name = current_os_name()
    arch = current_arch()[0]

# check what to use
find_by_method = {
    'xpath':'find_element_by_xpath',
    'css_selector':'find_element_by_css_selector',
    'class_name':'find_element_by_class_name',
    'id':'find_element_by_id',
    'name':'find_element_by_name'
}

# check what to wait for
wait_by = {
    'xpath':'By.XPATH',
    'css_selector':'By.CSS_SELECTOR',
    'class_name':'By.CLASS_NAME',
    'id':'By.ID',
    'name':'By.NAME'
}

# defining browser and options
# FIREFOX
if driver == 'geckodriver':
    opts = FirefoxOptions()
    opts.headless = mode
    browser = Firefox(executable_path=f"./drivers/{os_name}/{arch}/geckodriver{'.exe' if os_name == 'Windows' else ''}", service_log_path=None, options=opts)
# CHROME
elif driver == 'chromedriver':
    opts = ChromeOptions()
    opts.headless = mode
    browser = Chrome(executable_path=f"./drivers/{os_name}/{arch}/chromedriver{'.exe' if os_name == 'Windows' else ''}", service_log_path=None, options=opts)

# wait
wait = WebDriverWait(driver=browser, timeout=1000)

# get site
router_site = browser.get(address)

# wait until login fields show up
if paths['username']['exists'].capitalize() == True:
    exec(f"wait.until(EC.visibility_of_element_located(({wait_by[paths['username']['type']]}, paths['username']['value'])))")
exec(f"wait.until(EC.visibility_of_element_located(({wait_by[paths['password']['type']]}, paths['password']['value'])))")
exec(f"wait.until(EC.visibility_of_element_located(({wait_by[paths['login_button']['type']]}, paths['login_button']['value'])))")
print("log in fields are visible.")

# find login fields when they show up and fill them
if paths['username']['exists'].capitalize() == True:
    exec(f"browser.{find_by_method[paths['username']['type']]}(paths['username']['value']).click()")
    exec(f"browser.{find_by_method[paths['username']['type']]}(paths['username']['value']).clear()")
    exec(f"browser.{find_by_method[paths['username']['type']]}(paths['username']['value']).send_keys(data['credentials']['username'])")
exec(f"browser.{find_by_method[paths['password']['type']]}(paths['password']['value']).clear()")
exec(f"browser.{find_by_method[paths['password']['type']]}(paths['password']['value']).send_keys(data['credentials']['password'])")

# click login
exec(f"browser.{find_by_method[paths['login_button']['type']]}(paths['login_button']['value']).click()")
print("log in button clicked.")

# wait until the submenu where the reboot option is located shows up
for i,current_submenu in enumerate(paths["reboot_submenus"]):

    # menu status
    print(f"intermediate menu {i} {', frame' if bool(current_submenu.get('frame')) else ''}")

    # BEFORE next step if done with frames in previous section, go to parent 
    if current_submenu.get("go_to_parent_before"):
        levels_back = int(current_submenu.get("go_to_parent_before"))
        print(f'going to parent frame, {levels_back} levels back')
        for i in range(levels_back):
            browser.switch_to.default_content()

    # wait until the item is visible
    # if manually_wait is present, then the timeout is set to the value of that variable and uses sleep instead of selenium's wait
    if current_submenu.get('manually_wait') and int(current_submenu.get('manually_wait')) > 0:
        print(f'waiting manually a total of {current_submenu.get("manually_wait")} seconds')
        sleep(int(current_submenu['manually_wait']))
    else:
        exec(f"wait.until(EC.visibility_of_element_located(({wait_by[current_submenu['type']]}, current_submenu['value'])))")

    # if the first submenu shows up, the login was successful
    if i == 0:
        print("log in was sucessful.")

    # if the item is inside a frame, switch to it
    if bool(current_submenu.get("frame")):
        print('switching to frame')
        browser.switch_to.frame(current_submenu['value']) # this seems to only work by name?
    else:
        # click the designated item
        exec(f"browser.{find_by_method[current_submenu['type']]}(current_submenu['value']).click()")
    
    # AFTER last click, if done with frames in previous section, go to parent 
    if current_submenu.get("go_to_parent_after"):
        levels_back = int(current_submenu.get("go_to_parent_after"))
        print(f'going to parent frame, {levels_back} levels back')
        for i in range(levels_back):
            browser.switch_to.default_content()

# wait until reboot button shows up
exec(f"wait.until(EC.visibility_of_element_located(({wait_by[paths['reboot_button']['type']]}, paths['reboot_button']['value'])))")
if exec(f"browser.{find_by_method[paths['reboot_button']['type']]}(paths['reboot_button']['value'])"):
    print("reboot button is visible.")

# click the reboot button
exec(f"browser.{find_by_method[paths['reboot_button']['type']]}(paths['reboot_button']['value']).click()")
print("successfully clicked on the reboot button!")

# close driver
browser.quit()
