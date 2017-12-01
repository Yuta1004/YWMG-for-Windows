from getpass import getpass
import os
import subprocess
import sys
import re
import time
import zipfile

if __name__ == '__main__':
    username = ""
    password = []
    isInput = False
    python_path = []
    os_env = ""
    cu_dir = os.path.abspath(os.path.dirname(__file__))
    print("YWMG設定\n")

    print("1.必要なライブラリをインストールします\n")
    lib = ["selenium"]
    for count in range(len(lib)):
        return_code = subprocess.call("pip install " + lib[count])
        if return_code == 0:
            print("\n[ " + lib[count] + " ]が正常にインストールされました\n")
        else:
            print("\n[ " + lib[count] + " ]のインストールに失敗しました")
            print("プログラムを終了します")
            exit()

    print("\n2.ログインに使用するユーザ名とパスワードを入力して下さい\n")
    while not isInput:
        username = input("Username : ")
        password.append(getpass("Passeword : "))
        password.append(getpass("Passeword Again : "))
        if(password[0] == password[1]):
            isInput = True
            with open("pass.txt", "w") as f:
                f.write(username)
                f.write("\n")
                f.write(password[0])
        else:
            print("パスワードが一致しません。もう一度入力して下さい。\n")
            password = []

    print("\n3.必要なファイルを生成します")
    python_path = sys.path
    python_path = python_path[1]
    python_path = re.sub(r"\\(Python|python)..\.zip", "", python_path)
    with open("YWMG_start.bat", "w") as f:
        f.write(python_path + "\\python.exe")
        f.write(" ")
        f.write(cu_dir + "\\mailGet.py")
    with open("mail_data.json", "w") as f:
        f.write("")
    print("\n生成が完了しました")

    print("\n全ての設定が正常に終了しました")
    print("タスクスケジューラに[YWMG_start.bat] を登録してください\n")
    input("続行するには何かキーを押して下さい…")
