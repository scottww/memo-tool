# -*- coding: utf-8 -*-
import os
import sys
import json
import codecs

# 解决 Python 2 中文输出和参数编码问题
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
    PY2 = True
except NameError:
    PY2 = False

# 配置 notes 文件夹路径
CONFIG_FILE = 'config.json'
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            NOTES_DIR = config.get("notes_dir", "./notes")
    except (TypeError, UnicodeDecodeError):
        # 兼容 Python 2
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            NOTES_DIR = config.get("notes_dir", "./notes")
else:
    NOTES_DIR = "./notes"

# 确保笔记目录存在
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

def list_notes():
    """列出所有笔记文件"""
    if not os.path.exists(NOTES_DIR):
        print_safe("[笔记目录不存在]")
        return
        
    files = [f for f in os.listdir(NOTES_DIR) if f.endswith(".txt")]
    if not files:
        print_safe("[没有找到笔记文件]")
        return
        
    for f in files:
        print_safe("- %s" % f[:-4])

def print_safe(text):
    """安全打印文本，处理编码问题"""
    if PY2:
        # Python 2 处理
        if isinstance(text, unicode):
            try:
                print(text.encode('gbk', 'ignore'))
            except UnicodeError:
                print(text.encode('utf-8', 'ignore'))
        else:
            try:
                print(text.decode('utf-8').encode('gbk', 'ignore'))
            except UnicodeError:
                print(text)
    else:
        # Python 3 处理
        print(text)

def to_unicode(text):
    """将文本转换为 unicode 格式"""
    if PY2:
        if isinstance(text, unicode):
            return text
        try:
            return text.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return text.decode('gbk')
            except UnicodeDecodeError:
                return unicode(text, errors='ignore')
    else:
        # Python 3 中所有字符串都是 unicode
        if isinstance(text, bytes):
            try:
                return text.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    return text.decode('gbk')
                except UnicodeDecodeError:
                    return text.decode('latin1')
        return text

def open_note(project_name):
    """打开并显示指定项目的笔记内容"""
    path = os.path.join(NOTES_DIR, "%s.txt" % project_name)
    if os.path.exists(path):
        try:
            # 尝试使用 codecs 打开文件（更好的编码处理）
            with codecs.open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                print_safe(content)
        except (UnicodeDecodeError, IOError):
            # 回退到传统方式
            try:
                with open(path, 'r') as f:
                    content = to_unicode(f.read())
                    print_safe(content)
            except Exception as e:
                print_safe("[读取文件时出错: %s]" % str(e))
    else:
        project_name_u = to_unicode(project_name)
        print_safe("[未找到项目: %s]" % project_name_u)


def search_notes(keyword):
    """搜索包含关键词的笔记"""
    if not os.path.exists(NOTES_DIR):
        print_safe("[笔记目录不存在]")
        return
        
    files = [f for f in os.listdir(NOTES_DIR) if f.endswith(".txt")]
    if not files:
        print_safe("[没有找到笔记文件]")
        return
        
    keyword = to_unicode(keyword)
    found = False

    # 设置颜色（红色高亮）
    HIGHLIGHT_COLOR = '\033[1;37;41m'  # 白字红底
    RESET_COLOR = '\033[0m'
    
    # 检测终端是否支持颜色
    use_color = True
    if sys.platform == 'win32':
        # Windows 命令行默认不支持 ANSI 颜色
        # 但可以通过 colorama 等库启用
        try:
            import colorama
            colorama.init()
        except ImportError:
            use_color = False

    def highlight(text, key):
        """高亮关键词"""
        if not use_color:
            return text
        # 忽略大小写查找，但保留原文大小写
        i = text.lower().find(key.lower())
        if i >= 0:
            original_key = text[i:i+len(key)]
            return text.replace(original_key, HIGHLIGHT_COLOR + original_key + RESET_COLOR)
        return text

    for f in files:
        file_path = os.path.join(NOTES_DIR, f)
        try:
            # 尝试使用 codecs 打开文件
            with codecs.open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            # 回退到传统方式
            try:
                with open(file_path, 'r') as file:
                    content = to_unicode(file.read())
            except Exception:
                print_safe("[无法读取文件: %s]" % f)
                continue

        if keyword.lower() in content.lower():
            # 输出文件名
            print_safe(to_unicode(f[:-4]) + ":")
            
            # 按行处理并高亮关键词
            for line in content.splitlines():
                if keyword.lower() in line.lower():
                    line = highlight(line, keyword)
                    print_safe(line)
            print_safe("-" * 50)
            found = True

    if not found:
        print_safe("[未找到包含关键词的记录]")





def help_menu():
    """显示帮助信息"""
    help_text = """
memo 命令行工具

用法：
  memo list                     列出所有项目备忘
  memo <项目名>                查看项目备忘内容
  memo search <关键词>         搜索内容包含关键词的笔记
  memo new <项目名> [内容]     创建或追加内容到项目备忘
  memo gui                     启动图形界面

配置 config.json（可选）：
  {
    "notes_dir": "D:/你的txt目录"
  }

当前笔记目录: {}
""".format(os.path.abspath(NOTES_DIR))
    print_safe(help_text)

def create_or_append_note(project_name, content=None):
    """创建新笔记或追加内容到现有笔记"""
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
        
    path = os.path.join(NOTES_DIR, "%s.txt" % project_name)
    mode = 'a' if os.path.exists(path) else 'w'
    
    try:
        with codecs.open(path, mode, encoding='utf-8') as f:
            if content:
                f.write(to_unicode(content))
                if not content.endswith('\n'):
                    f.write('\n')
                print_safe("[内容已添加到: %s]" % project_name)
            else:
                print_safe("[已创建笔记: %s]" % project_name)
    except Exception as e:
        print_safe("[写入文件时出错: %s]" % str(e))

def start_gui():
    """启动图形界面"""
    try:
        import memo_gui
        print_safe("[正在启动图形界面...]")
        os.system('python memo_gui.py')
    except ImportError:
        print_safe("[错误: 未找到 memo_gui.py 文件]")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        help_menu()
    elif args[0] == "list":
        list_notes()
    elif args[0] == "search" and len(args) > 1:
        search_notes(args[1])
    elif args[0] == "new" and len(args) > 1:
        if len(args) > 2:
            create_or_append_note(args[1], " ".join(args[2:]))
        else:
            create_or_append_note(args[1])
    elif args[0] == "gui":
        start_gui()
    else:
        # 默认视为项目名
        open_note(args[0])
