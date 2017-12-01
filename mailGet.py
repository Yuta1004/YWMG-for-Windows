from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import os
import json

cu_dir = os.path.abspath(os.path.dirname(__file__))


def main():
    addEnvirionPath()
    saveOldMailTop = readJson({}, False)
    return_code = getMailDataToJson()
    if not return_code == 0:
        print("Error! \n{0}".format(return_code))
        exit()
    readJson(saveOldMailTop, True)


def addEnvirionPath():
    os_env = os.environ.get('Path')
    os_env_list = os_env.split(";")
    phantom_path = cu_dir + '\\phantomjs-2.1.1-windows\\bin'
    if not phantom_path in os_env_list:
        os.environ['Path'] = os_env + ";" + phantom_path


def getMailDataToJson():
    with open(cu_dir + "\\pass.txt") as f:
        file_ = f.read()
        file_ = file_.split()
        username = file_[0]
        password = file_[1]
    print("Username : {0}".format(username))
    print("Password : " + "*" * len(password))
    print("Connecting...")
    url = 'https://www.center.yuge.ac.jp/webmail/src/'

    try:
        driver = webdriver.PhantomJS()
        driver.get(url + 'login.php')
        print("Logging in...")
        time.sleep(1)
        element_user = driver.find_element_by_name('login_username')
        element_user.send_keys(username)
        element_pass = driver.find_element_by_name('secretkey')
        element_pass.send_keys(password)
        element_pass.send_keys(Keys.RETURN)
        if not driver.current_url == url + "webmail.php":
            print("Login Faild")
            return 1
    except Exception as e:
        return e

    driver.get(url + 'right_main.php')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    mail_data = soup.findAll("tr", valign="top")
    mail_list = list(map(lambda n: str(n).split("\n"), mail_data))
    mail_list = \
        list(map(lambda n: list(map(lambda m: delTag(m), n)), mail_list))
    mail_list = list(map(lambda n: toDict([n[2], n[4], n[6]]), mail_list))
    mail_dict = {}
    for idx, item in enumerate(mail_list):
        mail_dict[idx] = item
    with open("mail_data.json", 'w', encoding='utf-8') as json_file:
        json.dump(mail_dict, json_file, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))
    driver.quit()
    return 0


def toDict(mail_list_n):
    return {"Sender": mail_list_n[0], "Date": mail_list_n[1], "Title": mail_list_n[2]}


def delTag(data):
    data = str(BeautifulSoup(data, 'html.parser').string)
    if not data == ("None" or ""):
        return data


def readJson(saveOldMailTop, isNewMailGet):
    try:
        with open("mail_data.json", 'r', encoding='utf-8') as f:
            json_data = dict(json.load(f))
    except Exception as e:
        return {"": ""}

    if not isNewMailGet:
        return json_data["0"]
    find_idx = 0
    for idx in json_data:
        if saveOldMailTop == json_data[str(idx)]:
            find_idx = idx
            break
        else:
            find_idx += 1
    if find_idx == "0":
        print("\n新着メールはありません。\n")
    else:
        if find_idx == 15:
            print("\n新着メールが15件以上あります。\n")
        else:
            print("\n新着メールが{0}件あります。\n".format(find_idx))
        for idx in json_data:
            if idx == find_idx:
                break
            print("{0}件目\tfrom: {1}".format(
                str(int(idx) + 1), json_data[idx]["Sender"]))
            print("\t受信日時: {0}".format(json_data[idx]["Date"]))
            print("\t件名: {0}".format(json_data[idx]["Title"]))
            print()
        input("続行するには何かキーを押して下さい…")


if __name__ == '__main__':
    main()
