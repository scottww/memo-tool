# -*- coding: utf-8 -*-
import os
import sys
import json

# 解决 Python 2 中文输出和参数编码问题
reload(sys)
sys.setdefaultencoding('utf-8')

# 配置 notes 文件夹路径
CONFIG_FILE = 'config1.json'
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
        NOTES_DIR = config.get("notes_dir", "./notes")
else:
    NOTES_DIR = "./notes"

def list_notes():
    files = [f for f in os.listdir(NOTES_DIR) if f.endswith(".txt")]
    for f in files:
        print("- %s" % f[:-4])

def open_note(project_name):
    path = os.path.join(NOTES_DIR, "%s.txt" % project_name)
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read().decode('utf-8')
            print(content.encode('utf-8'))
    else:
        print(u"[❌] 未找到项目: %s" % project_name.decode('utf-8')).encode('utf-8')

def search_notes(keyword):
    files = [f for f in os.listdir(NOTES_DIR) if f.endswith(".txt")]
    found = False
    try:
        keyword = keyword.decode('utf-8')
    except UnicodeDecodeError:
        keyword = keyword.decode('gbk')
    for f in files:
        with open(os.path.join(NOTES_DIR, f), 'r') as file:
            content = file.read().decode('utf-8')
            if keyword.lower() in content.lower():
                output = u"%s:\n%s\n%s" % (f.decode('utf-8'), content, u"-"*50)
                print(output.encode('gbk', 'ignore'))  # ✅ 最稳定
                found = True
    if not found:
        print(u"[❌] 未找到包含关键词的记录".encode('gbk'))



def help_menu():
    print(u"""
memo 命令行工具 📝

用法：
  memo.py list                   列出所有项目
  memo.py <project-name>         打开指定项目备忘 txt
  memo.py search <关键词>        搜索所有 txt 文件

配置文件：
  config.json 可指定 notes 路径，例如：
  { "notes_dir": "D:/ProjectNotes" }
""".encode('utf-8'))

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        help_menu()
    elif args[0] == "list":
        list_notes()
    elif args[0] == "search" and len(args) > 1:
        search_notes(args[1])
    else:
        open_note(args[0])
