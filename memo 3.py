# -*- coding: utf-8 -*-

import os
import sys
import json

# 配置 notes 文件夹路径 （如果要使用config.json中的路径）
CONFIG_FILE = 'config1.json'
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
        NOTES_DIR = config.get("notes_dir", "./notes")
else:
    NOTES_DIR = "./notes"

def list_notes():
    files = [f for f in os.listdir(NOTES_DIR) if f.endswith(".txt")]
    for f in files:
        print("- {}".format(f[:-4]))  # 去掉 .txt 扩展名

def open_note(project_name):
    path = os.path.join(NOTES_DIR, "{}.txt".format(project_name))
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("[❌] 未找到项目: {}".format(project_name))

def search_notes(keyword):
    files = [f for f in os.listdir(NOTES_DIR) if f.endswith(".txt")]
    found = False
    for f in files:
        with open(os.path.join(NOTES_DIR, f), 'r', encoding='utf-8') as file:
            content = file.read()
            if keyword.lower() in content.lower():
                print("📌 {}:\n{}\n{}".format(f, content, '-'*50))
                found = True
    if not found:
        print("[❌] 未找到包含关键词的记录")

def help_menu():
    print("""
memo 命令行工具 📝

用法：
  memo list                  列出所有项目
  memo <project-name>        打开指定项目备忘 txt
  memo search <关键词>       搜索所有 txt 文件

配置文件：
  config.json 可指定 notes 路径，例如：
  { "notes_dir": "D:/ProjectNotes" }
""")

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
