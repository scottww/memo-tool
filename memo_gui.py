# -*- coding: utf-8 -*-
try:
    # Python 3
    import tkinter as tk
    from tkinter import font as tkFont
    from tkinter import messagebox
    PY3 = True
except ImportError:
    # Python 2
    import Tkinter as tk
    import tkFont
    import tkMessageBox as messagebox
    PY3 = False

import os
import sys
import json
import codecs

# 加载配置
def load_config():
    CONFIG_FILE = 'config.json'
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get("notes_dir", "./notes")
        except (TypeError, UnicodeDecodeError):
            # 兼容 Python 2
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get("notes_dir", "./notes")
    return "./notes"

class MemoApp(object):
    def __init__(self, root):
        self.root = root
        root.title("Memo 笔记管理器")
        root.geometry("1280x800")  # 设置窗口大小
        
        # 设置图标（如果有）
        try:
            if PY3:
                root.iconbitmap("memo.ico")
            else:
                root.iconbitmap(default="memo.ico")
        except:
            pass  # 图标不存在则忽略
            
        # 创建菜单
        self.create_menu()
        
        # 顶部工具栏
        top_frame = tk.Frame(root, bd=1, relief=tk.RAISED)
        top_frame.pack(side='top', fill='x', padx=5, pady=5)

        # 搜索区域
        tk.Label(top_frame, text="搜索关键词:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(top_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search())
        
        search_btn = tk.Button(top_frame, text="搜索", command=self.search)
        search_btn.pack(side='left', padx=5)
        
        # 新建笔记按钮
        new_btn = tk.Button(top_frame, text="新建笔记", command=self.new_note)
        new_btn.pack(side='left', padx=15)
        
        # 刷新按钮
        refresh_btn = tk.Button(top_frame, text="刷新列表", command=self.load_projects)
        refresh_btn.pack(side='left', padx=5)

        # 主区域：左边列表 + 右边内容
        main_frame = tk.Frame(root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # 左侧列表
        list_frame = tk.Frame(main_frame)
        list_frame.pack(side='left', fill='y')
        
        # 列表标题
        list_label = tk.Label(list_frame, text="笔记列表", font=("微软雅黑", 10, "bold"))
        list_label.pack(side='top', fill='x', pady=5)

        # 列表和滚动条
        list_container = tk.Frame(list_frame)
        list_container.pack(side='top', fill='both', expand=True)
        
        self.listbox = tk.Listbox(list_container, width=25, font=("微软雅黑", 12), 
                                 selectbackground="#4a6984", selectforeground="white")
        self.listbox.pack(side='left', fill='both', expand=True)

        list_scroll = tk.Scrollbar(list_container, command=self.listbox.yview)
        list_scroll.pack(side='right', fill='y')
        self.listbox.config(yscrollcommand=list_scroll.set)

        self.listbox.bind("<<ListboxSelect>>", self.show_content)
        self.listbox.bind("<Double-Button-1>", self.edit_mode_toggle)

        # 右侧内容区
        text_frame = tk.Frame(main_frame)
        text_frame.pack(side='right', fill='both', expand=True, padx=10)
        
        # 内容区标题和按钮
        text_header = tk.Frame(text_frame)
        text_header.pack(side='top', fill='x')
        
        self.content_title = tk.Label(text_header, text="笔记内容", font=("微软雅黑", 10, "bold"))
        self.content_title.pack(side='left', pady=5)
        
        self.edit_button = tk.Button(text_header, text="编辑", command=self.edit_mode_toggle)
        self.edit_button.pack(side='right')
        
        self.save_button = tk.Button(text_header, text="保存", command=self.save_content)
        self.save_button.pack(side='right', padx=5)
        self.save_button.config(state=tk.DISABLED)

        # 文本区和滚动条
        text_container = tk.Frame(text_frame)
        text_container.pack(side='top', fill='both', expand=True)
        
        self.text = tk.Text(text_container, wrap='word', font=("Consolas", 12), 
                           bg='#f9f9f9', padx=10, pady=10)
        self.text.pack(side='left', fill='both', expand=True)
        self.text.config(state=tk.DISABLED)  # 默认为只读模式

        text_scroll = tk.Scrollbar(text_container, command=self.text.yview)
        text_scroll.pack(side='right', fill='y')
        self.text.config(yscrollcommand=text_scroll.set)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 笔记目录
        self.notes_dir = load_config()
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)
            
        # 当前编辑状态
        self.edit_mode = False
        self.current_note = None

        # 加载项目列表
        self.load_projects()
        
        # 设置窗口关闭事件
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="新建笔记", command=self.new_note)
        file_menu.add_command(label="保存", command=self.save_content)
        file_menu.add_separator()
        file_menu.add_command(label="刷新列表", command=self.load_projects)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_close)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="编辑/查看模式切换", command=self.edit_mode_toggle)
        edit_menu.add_separator()
        edit_menu.add_command(label="删除当前笔记", command=self.delete_note)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.root.config(menu=menubar)

    def load_projects(self):
        """加载项目列表"""
        self.listbox.delete(0, tk.END)
        try:
            files = [f for f in os.listdir(self.notes_dir) if f.endswith(".txt")]
            files.sort()  # 按字母顺序排序
            for f in files:
                self.listbox.insert(tk.END, f[:-4])
            self.status_var.set("已加载 {} 个笔记 | 笔记目录: {}".format(len(files), os.path.abspath(self.notes_dir)))
        except Exception as e:
            self.status_var.set("加载笔记失败: {}".format(str(e)))
            if not PY3:
                messagebox.showerror("错误", "加载笔记失败: " + str(e))
            else:
                messagebox.showerror("错误", "加载笔记失败: " + str(e))

    def show_content(self, event):
        """显示选中项目的内容"""
        sel = self.listbox.curselection()
        if not sel:
            return
            
        # 如果当前正在编辑，提示保存
        if self.edit_mode and self.current_note:
            if not PY3:
                save = messagebox.askyesnocancel("保存更改", 
                                              "当前笔记有未保存的更改，是否保存？")
            else:
                save = messagebox.askyesnocancel("保存更改", 
                                              "当前笔记有未保存的更改，是否保存？")
            if save is None:  # 取消操作
                return
            if save:  # 保存更改
                self.save_content()
        
        project = self.listbox.get(sel[0])
        self.current_note = project
        file_path = os.path.join(self.notes_dir, project + ".txt")
        
        # 更新标题
        self.content_title.config(text="笔记内容: {}".format(project))
        
        # 设置为只读模式
        self.text.config(state=tk.NORMAL)
        self.text.delete('1.0', tk.END)
        
        try:
            # 尝试使用 codecs 打开文件
            with codecs.open(file_path, "r", encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # 回退到传统方式
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    content = self.to_unicode(content)
            except Exception as e:
                if PY3:
                    content = "读取失败: {}".format(str(e))
                else:
                    content = u"读取失败: %s" % unicode(str(e), errors='ignore')
        except Exception as e:
            if PY3:
                content = "读取失败: {}".format(str(e))
            else:
                content = u"读取失败: %s" % unicode(str(e), errors='ignore')
                
        self.text.insert(tk.END, content)
        
        # 恢复只读状态（如果不在编辑模式）
        if not self.edit_mode:
            self.text.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
            self.edit_button.config(text="编辑")
        else:
            self.save_button.config(state=tk.NORMAL)
            
        self.status_var.set("已加载: {}".format(project))
        
    def edit_mode_toggle(self, event=None):
        """切换编辑/查看模式"""
        if not self.current_note:
            return
            
        self.edit_mode = not self.edit_mode
        
        if self.edit_mode:
            self.text.config(state=tk.NORMAL)
            self.save_button.config(state=tk.NORMAL)
            self.edit_button.config(text="查看")
            self.status_var.set("编辑模式: {}".format(self.current_note))
        else:
            self.text.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
            self.edit_button.config(text="编辑")
            self.status_var.set("查看模式: {}".format(self.current_note))
            
    def save_content(self):
        """保存当前笔记内容"""
        if not self.current_note:
            return
            
        content = self.text.get('1.0', tk.END)
        file_path = os.path.join(self.notes_dir, self.current_note + ".txt")
        
        try:
            with codecs.open(file_path, "w", encoding='utf-8') as f:
                f.write(content)
            self.status_var.set("已保存: {}".format(self.current_note))
        except Exception as e:
            self.status_var.set("保存失败: {}".format(str(e)))
            if not PY3:
                messagebox.showerror("保存失败", "无法保存文件: " + str(e))
            else:
                messagebox.showerror("保存失败", "无法保存文件: " + str(e))
                
    def new_note(self):
        """创建新笔记"""
        # 创建输入对话框
        if not PY3:
            import tkSimpleDialog
            project_name = tkSimpleDialog.askstring("新建笔记", "请输入笔记名称:")
        else:
            from tkinter import simpledialog
            project_name = simpledialog.askstring("新建笔记", "请输入笔记名称:")
            
        if not project_name:
            return
            
        # 检查是否已存在
        file_path = os.path.join(self.notes_dir, project_name + ".txt")
        if os.path.exists(file_path):
            if not PY3:
                overwrite = messagebox.askyesno("笔记已存在", 
                                             "笔记 '{}' 已存在，是否打开?".format(project_name))
            else:
                overwrite = messagebox.askyesno("笔记已存在", 
                                             "笔记 '{}' 已存在，是否打开?".format(project_name))
            if overwrite:
                # 选择并显示已存在的笔记
                for i in range(self.listbox.size()):
                    if self.listbox.get(i) == project_name:
                        self.listbox.selection_clear(0, tk.END)
                        self.listbox.selection_set(i)
                        self.listbox.see(i)
                        self.show_content(None)
                        break
            return
            
        # 创建新笔记文件
        try:
            with codecs.open(file_path, "w", encoding='utf-8') as f:
                f.write("")
                
            # 刷新列表并选择新笔记
            self.load_projects()
            for i in range(self.listbox.size()):
                if self.listbox.get(i) == project_name:
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(i)
                    self.listbox.see(i)
                    self.show_content(None)
                    # 自动进入编辑模式
                    self.edit_mode = False  # 确保状态正确
                    self.edit_mode_toggle()
                    break
                    
            self.status_var.set("已创建新笔记: {}".format(project_name))
        except Exception as e:
            self.status_var.set("创建笔记失败: {}".format(str(e)))
            if not PY3:
                messagebox.showerror("错误", "创建笔记失败: " + str(e))
            else:
                messagebox.showerror("错误", "创建笔记失败: " + str(e))
                
    def delete_note(self):
        """删除当前笔记"""
        if not self.current_note:
            return
            
        if not PY3:
            confirm = messagebox.askyesno("确认删除", 
                                       "确定要删除笔记 '{}' 吗？此操作不可恢复。".format(self.current_note))
        else:
            confirm = messagebox.askyesno("确认删除", 
                                       "确定要删除笔记 '{}' 吗？此操作不可恢复。".format(self.current_note))
        if not confirm:
            return
            
        file_path = os.path.join(self.notes_dir, self.current_note + ".txt")
        try:
            os.remove(file_path)
            self.text.config(state=tk.NORMAL)
            self.text.delete('1.0', tk.END)
            self.text.config(state=tk.DISABLED)
            self.content_title.config(text="笔记内容")
            self.current_note = None
            self.load_projects()
            self.status_var.set("笔记已删除")
        except Exception as e:
            self.status_var.set("删除失败: {}".format(str(e)))
            if not PY3:
                messagebox.showerror("错误", "删除笔记失败: " + str(e))
            else:
                messagebox.showerror("错误", "删除笔记失败: " + str(e))
                
    def on_close(self):
        """窗口关闭前检查是否有未保存内容"""
        if self.edit_mode and self.current_note:
            if not PY3:
                save = messagebox.askyesnocancel("保存更改", 
                                              "有未保存的更改，是否保存？")
            else:
                save = messagebox.askyesnocancel("保存更改", 
                                              "有未保存的更改，是否保存？")
            if save is None:  # 取消关闭
                return
            if save:  # 保存更改
                self.save_content()
                
        self.root.destroy()
        
    def show_about(self):
        """显示关于信息"""
        about_text = """Memo 笔记管理器
版本: 1.0

一个简单的笔记管理工具，用于记录和查找项目相关信息。

支持功能:
- 创建和编辑笔记
- 搜索笔记内容
- 管理多个项目笔记
"""
        if not PY3:
            messagebox.showinfo("关于 Memo", about_text)
        else:
            messagebox.showinfo("关于 Memo", about_text)

    def search(self):
        """搜索包含关键词的笔记"""
        keyword = self.search_var.get().strip()
        
        # 转换关键词为 unicode
        if PY3:
            keyword_u = keyword  # Python 3 中字符串默认是 unicode
        else:
            # 兼容 keyword 是 str 或 unicode
            if isinstance(keyword, str):
                try:
                    keyword_u = keyword.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        keyword_u = keyword.decode('gbk')
                    except UnicodeDecodeError:
                        keyword_u = unicode(keyword, errors='ignore')
            else:
                keyword_u = keyword  # 已是 unicode

        if not keyword_u:
            self.load_projects()
            return

        results = []
        for f in os.listdir(self.notes_dir):
            if f.endswith(".txt"):
                try:
                    # 尝试使用 codecs 打开文件
                    with codecs.open(os.path.join(self.notes_dir, f), "r", encoding='utf-8') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    # 回退到传统方式
                    try:
                        with open(os.path.join(self.notes_dir, f), "r") as file:
                            content = file.read()
                            content = self.to_unicode(content)
                    except Exception:
                        continue
                except Exception:
                    continue
                    
                # 忽略大小写搜索
                if keyword_u.lower() in content.lower():
                    results.append(f[:-4])

        self.listbox.delete(0, tk.END)
        for r in results:
            self.listbox.insert(tk.END, r)
            
        # 清空内容区
        self.text.config(state=tk.NORMAL)
        self.text.delete('1.0', tk.END)
        self.text.config(state=tk.DISABLED)
        
        # 更新状态
        if results:
            self.status_var.set("找到 {} 个包含 '{}' 的笔记".format(len(results), keyword))
            self.content_title.config(text="笔记内容")
        else:
            self.status_var.set("未找到包含 '{}' 的笔记".format(keyword))
            self.content_title.config(text="笔记内容")
            
        # 重置当前笔记
        self.current_note = None


    def to_unicode(self, content):
        """将文本转换为 unicode 格式"""
        if PY3:
            # Python 3 中所有字符串都是 unicode
            if isinstance(content, bytes):
                try:
                    return content.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        return content.decode('gbk')
                    except UnicodeDecodeError:
                        return content.decode('latin1', errors='ignore')
            return content
        else:
            # Python 2 处理
            if isinstance(content, unicode):
                return content
            try:
                return content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    return content.decode('gbk')
                except UnicodeDecodeError:
                    return unicode(content, errors='ignore')

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoApp(root)
    root.mainloop()
