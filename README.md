# Selenium-based router reboot script

A simple selenium-based tool to reboot a router by navigating to its configuration static site without physical access to it.

For install instructions (if you need them) go to [Install instructions](#install-instructions), otherwise, you can continue reading.

The only requirements for this to run are at least Python 3.8.8 (I guess it could also work with python 3.8 but I haven't tested) and selenium version `3.141.0`. I've already included a working geckodriver (and chromedriver) that the script uses. The drivers I include will work on Windows, macOS (arm64) or Linux. 

The driver versions included are:
- geckodriver 0.31.0 (2022-04-11, b617178ef491)
- chromedriver 104.0.5112.79

The selenium package used in this repo is not up to date and the selenium API has changed kind of meaningfully, so if you want to use it, stick to the version in the `requirements.txt` file, otherwise it won't work.

## Disclaimer

For this project I heavily rely on python's `exec()` function. If you find this useful and want to use it, be extremely careful where you use this and make sure that nothing being passed to the code is malicious. I am not responsible for anything you do, you use this tool at your own risk.

## How to use

1. Clone this repository.

2. Create a copy of `data.json` and name it `private.json`, this file is deliberately ignored by the `.gitignore` file to avoid being pushed to version control. You should fill up this file as follows:
   
    + Under the `driver` key you must choose to either use `geckodriver` or `chromedriver`. E.g. `"driver":"geckodriver"`

    + Under the `address` key, fill up the local address that can access the configuration frontend. This can typically be something like `http://10.0.0.1` or something like this. Don't forget to add `http://`.

    + Under the `headless` key you should type if you want to run it in headless mode (`True`) or not (`False`). If to see the browser interface set this as `False`.

    + Under the `credentials` key, fill up the `username` and `password` to log into your router's configuration interface. If there IS a username, then you must write `"True"` under the `exists` key under `username`. If it does NOT have a username, then just write `"False"`

    + Under the `path` key you have to fill up several things, to get this information you can use inspect element on your browser after right clicking on the input field for your router username in the login page and then in the html shown by the inspect element menu, right click on the highlighted text and copy what identifier should be used. In general for my purposes, the xpath works well, but you can also use the CSS Selector or ID of the field. After you have the unique identifier then:
  
      + The `type` field should have the type of identifier you used, either `xpath`, `css_selector`, `class_name`, `id` or `name` (`name` is required for frames).
      + The `value` field should have the unique identifier for the field.
      + If the item is a frame, you must add the key-value `"frame":"True"`
      + If you want to go back from a frame any number of times to the previous parent element, you must add `"go_to_parent_after":"number_of_times"` where `"number_of_times"` is a number (e.g. "1") if you want to go to the parent *after* interacting with that intermediate element or `"go_to_parent_before":"number_of_times"` in the opposite case, with the same change for `"number_of_times"`.
      + Optionally, you can add `manually_wait` to an intermediate item so that the script will use `sleep` as opposed to selenium's native `WebDriverWait()`

    + Each field key corresponds with the following things:
      + `username` should be the **input field for the router's login username**
      + `password` should be the **input field for the router's login password**
      + `login_button` should be the **button to log in**
      + `reboot_submenus` is an array of objects of the same sort as the previous fields. As with most routers, there will be **several intermediate menus until you reach the reboot button** and its confirmation prompt (if present). Here you should add as many `{"type":"", "value":""}` objects as you need for these intermediate menus, in my case I had to click on about 4 links/menus before I reached the reboot button confirmation, so I needed 4 xpaths (because I used xpath) for the values of these 4 intermediate buttons and given that I always used xpath, the `type` key for my 4 intermediate menus was always filled with `xpath`.
      + `reboot_button` is the **final button or link that confirms the reboot**. 

3. Run the script in console using `python reboot_router.py` or `python3 reboot_router.py`.

## Install instructions

If you already have a python environment with selenium version `3.141.0` installed, you can skip this step.

### Using a basic python installation

If you have at least python 3.8 installed, you can just `pip install selenium=='3.141.0'`.

### Setting up a venv

If you want to set up an environment for this using `venv`, you can do as follows depending on your OS:

#### Linux, macOS

Create a new python 3 environment.

```
python -m venv selenium-router-rebooter
```

Activate the new environment.

```
source selenium-router-rebooter/bin/activate
```

Install the packages in the new environment.

```
pip install -r requirements.txt
```

#### Windows

Create a new python 3 environment.

```
python -m venv selenium-router-rebooter
```

Activate the new environment.

```
.\selenium-router-rebooter\Scripts\activate.bat 
```

Install the packages in the new environment.

```
pip install -r requirements.txt
```
