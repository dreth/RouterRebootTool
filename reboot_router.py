import json
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# open json
with open('private.json', 'r') as f:
    data = json.load(f)
    paths = data['path']
    address = data['address']
    mode = data['headless'].capitalize()

# check what to use
find_by_method = {
    'xpath':'find_element_by_xpath',
    'css_selector':'find_element_by_css_selector',
    'class_name':'find_element_by_class_name',
    'id':'find_element_by_id'
}

# check what to wait for
wait_by = {
    'xpath':'By.XPATH',
    'css_selector':'By.CSS_SELECTOR',
    'class_name':'By.CLASS_NAME',
    'id':'By.ID'
}

# setting options
opts = Options()
opts.headless = mode

# defining browser
browser = Firefox(executable_path="./geckodriver", service_log_path=None, options=opts)

# wait
wait = WebDriverWait(driver=browser, timeout=1000)

# get site
router_site = browser.get(address)

# wait until login fields show up
if paths['username']['exists'] == True:
    exec(f"wait.until(EC.visibility_of_element_located(({wait_by[paths['username']['type']]}, paths['username']['value'])))")
exec(f"wait.until(EC.visibility_of_element_located(({wait_by[paths['password']['type']]}, paths['password']['value'])))")
exec(f"wait.until(EC.visibility_of_element_located(({wait_by[paths['login_button']['type']]}, paths['login_button']['value'])))")
print("log in fields are visible.")

# find login fields when they show up and fill them
if paths['username']['exists'] == True:
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
    print(f"intermediate menu {i}")

    # wait until the xpath is visible
    exec(f"wait.until(EC.visibility_of_element_located(({wait_by[current_submenu['type']]}, current_submenu['value'])))")

    # if the first submenu shows up, the login was successful
    if i == 0:
        print("log in was sucessful.")

    # click the designated xpath
    exec(f"browser.{find_by_method[current_submenu['type']]}(current_submenu['value']).click()")

# wait until reboot button shows up
exec(f"wait.until(EC.visibility_of_element_located(({wait_by[paths['reboot_button']['type']]}, paths['reboot_button']['value'])))")
if exec(f"browser.{find_by_method[paths['reboot_button']['type']]}(paths['reboot_button']['value'])"):
    print("reboot button is visible.")

# click the reboot button
exec(f"browser.{find_by_method[paths['reboot_button']['type']]}(paths['reboot_button']['value']).click()")
print("successfully clicked on the reboot button!")

# close driver
browser.quit()
