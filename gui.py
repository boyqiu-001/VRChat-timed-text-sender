#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI界面类
使用tkinter创建用户界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
from osc_client import OSCClient
from message_sender import MessageSender
from config_manager import ConfigManager
import threading


class OSCSenderGUI:
    """OSC消息发送器GUI类"""
    
    def __init__(self):
        self.root = None
        self.config = ConfigManager()
        self.osc_client = OSCClient()
        self.message_sender = MessageSender(self.osc_client)
        
        # 设置回调函数
        self.message_sender.on_status_change = self.on_sending_status_change
        self.message_sender.on_message_sent = self.on_message_sent
        
        # UI元素引用
        self.ip_entry = None
        self.port_entry = None
        self.interval_entry = None
        self.message_text = None
        self.status_label = None
        self.send_count_label = None
        self.start_button = None
        self.stop_button = None
        self.test_button = None
        
    def run(self):
        """运行GUI"""
        self.root = tk.Tk()
        self.root.title("VRChat OSC消息定时发送器")
        self.root.geometry(self.config.get("window_geometry", "500x400+100+100"))
        self.root.resizable(True, True)
        
        # 设置窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 创建界面
        self.create_widgets()
        
        # 加载保存的配置
        self.load_config_to_ui()
        
        # 启动主循环
        self.root.mainloop()
    
    def create_widgets(self):
        """创建界面控件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置主框架网格权重以支持缩放
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)  # 让状态区域也能扩展
        
        # OSC设置区域
        osc_frame = ttk.LabelFrame(main_frame, text="OSC设置", padding="10")
        osc_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        osc_frame.columnconfigure(1, weight=1)
        
        # IP地址
        ttk.Label(osc_frame, text="IP地址:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.ip_entry = ttk.Entry(osc_frame, width=15)
        self.ip_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        self.ip_entry.insert(0, "127.0.0.1")
        
        # 端口
        ttk.Label(osc_frame, text="端口:").grid(row=0, column=2, sticky=tk.W, padx=(20, 5), pady=2)
        self.port_entry = ttk.Entry(osc_frame, width=8)
        self.port_entry.grid(row=0, column=3, sticky=tk.W, pady=2)
        self.port_entry.insert(0, "9000")
        
        # 测试连接按钮
        self.test_button = ttk.Button(osc_frame, text="测试连接", command=self.test_connection)
        self.test_button.grid(row=0, column=4, sticky=tk.W, padx=(10, 0), pady=2)
        
        # 消息设置区域
        message_frame = ttk.LabelFrame(main_frame, text="消息设置", padding="10")
        message_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        message_frame.columnconfigure(0, weight=1)
        
        # 发送间隔
        ttk.Label(message_frame, text="发送间隔(秒):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.interval_entry = ttk.Entry(message_frame, width=10)
        self.interval_entry.grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        self.interval_entry.insert(0, "5")
        
        # 消息内容
        ttk.Label(message_frame, text="消息内容:").grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # 创建消息文本框和滚动条的容器
        text_frame = ttk.Frame(message_frame)
        text_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=2)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.message_text = tk.Text(text_frame, height=4, width=40)
        self.message_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.message_text.insert("1.0", "Hello VRChat!")
        
        # 绑定文本变化事件
        self.message_text.bind("<KeyRelease>", self.on_message_change)
        self.message_text.bind("<FocusOut>", self.on_message_change)
        
        # 绑定配置变化自动保存
        self.ip_entry.bind("<FocusOut>", self.auto_save_config)
        self.port_entry.bind("<FocusOut>", self.auto_save_config)
        self.interval_entry.bind("<FocusOut>", self.auto_save_config)
        self.message_text.bind("<FocusOut>", self.auto_save_config)
        
        # 滚动条
        message_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.message_text.yview)
        message_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.message_text.configure(yscrollcommand=message_scrollbar.set)
        
        # 控制按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="开始发送", command=self.start_sending)
        self.start_button.grid(row=0, column=0, padx=(0, 5))
        
        self.stop_button = ttk.Button(button_frame, text="停止发送", command=self.stop_sending, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=(5, 0))
        
        # 状态显示区域
        status_frame = ttk.LabelFrame(main_frame, text="状态信息", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(1, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="就绪", foreground="blue")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.send_count_label = ttk.Label(status_frame, text="发送次数: 0")
        self.send_count_label.grid(row=1, column=0, sticky=tk.W)
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)  # 让状态区域也能扩展
        osc_frame.columnconfigure(1, weight=1)
        message_frame.columnconfigure(0, weight=1)
    
    def load_config_to_ui(self):
        """加载配置到UI"""
        config = self.config.get_all()
        
        # 清空现有内容
        self.ip_entry.delete(0, tk.END)
        self.port_entry.delete(0, tk.END)
        self.interval_entry.delete(0, tk.END)
        self.message_text.delete("1.0", tk.END)
        
        # 加载配置值
        self.ip_entry.insert(0, config.get("osc_ip", "127.0.0.1"))
        self.port_entry.insert(0, str(config.get("osc_port", 9000)))
        self.interval_entry.insert(0, str(config.get("message_interval", 5)))
        self.message_text.insert("1.0", config.get("message_text", "Hello VRChat!"))
    
    def auto_save_config(self, event=None):
        """自动保存配置（静默模式）"""
        try:
            config = {
                "osc_ip": self.ip_entry.get().strip(),
                "osc_port": int(self.port_entry.get().strip()),
                "message_interval": int(self.interval_entry.get().strip()),
                "message_text": self.message_text.get("1.0", tk.END).strip(),
                "window_geometry": self.root.geometry()
            }
            self.config.update_all(config)
        except (ValueError, Exception):
            # 静默处理错误，不提示用户
            pass
    
    def test_connection(self):
        """测试OSC连接"""
        ip = self.ip_entry.get().strip()
        try:
            port = int(self.port_entry.get().strip())
        except ValueError:
            messagebox.showerror("错误", "端口必须是数字!")
            return
        
        # 禁用测试按钮
        self.test_button.config(state=tk.DISABLED)
        self.status_label.config(text="测试中...", foreground="orange")
        
        def test_thread():
            try:
                if self.osc_client.test_connection(ip, port):
                    self.root.after(0, lambda: self.status_label.config(text="连接成功", foreground="green"))
                    self.root.after(0, lambda: messagebox.showinfo("成功", "OSC连接成功!"))
                else:
                    self.root.after(0, lambda: self.status_label.config(text="连接失败", foreground="red"))
                    self.root.after(0, lambda: messagebox.showerror("失败", "OSC连接失败，请检查IP和端口!"))
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(text="连接错误", foreground="red"))
                self.root.after(0, lambda: messagebox.showerror("错误", f"连接测试失败: {e}"))
            finally:
                self.root.after(0, lambda: self.test_button.config(state=tk.NORMAL))
        
        # 在新线程中测试连接，避免阻塞UI
        threading.Thread(target=test_thread, daemon=True).start()
    
    def start_sending(self):
        """开始发送消息"""
        # 获取配置值
        ip = self.ip_entry.get().strip()
        try:
            port = int(self.port_entry.get().strip())
            interval = int(self.interval_entry.get().strip())
        except ValueError:
            messagebox.showerror("错误", "端口和间隔必须是数字!")
            return
        
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("错误", "消息内容不能为空!")
            return
        
        # 更新OSC客户端配置
        self.osc_client.ip = ip
        self.osc_client.port = port
        
        # 尝试连接
        if not self.osc_client.connect():
            messagebox.showerror("错误", "无法连接到OSC服务器，请检查设置!")
            return
        
        # 开始发送
        if self.message_sender.start_sending(message, interval):
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="正在发送...", foreground="green")
    
    def stop_sending(self):
        """停止发送消息"""
        self.message_sender.stop_sending()
        self.osc_client.disconnect()
    
    def on_sending_status_change(self, is_running):
        """发送状态变化回调"""
        if not is_running:
            self.root.after(0, self.update_ui_on_stop)
    
    def on_message_sent(self, message, count):
        """消息发送回调"""
        self.root.after(0, lambda: self.update_send_count(count))
    
    def update_ui_on_stop(self):
        """更新UI为停止状态"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="已停止", foreground="blue")
    
    def update_send_count(self, count):
        """更新发送计数"""
        self.send_count_label.config(text=f"发送次数: {count}")
    
    def on_message_change(self, event=None):
        """消息内容变化时的处理"""
        # 如果正在发送，实时更新消息内容
        if self.message_sender and self.message_sender.is_active():
            new_message = self.message_text.get("1.0", tk.END).strip()
            self.message_sender.update_message_text(new_message)
    
    def on_closing(self):
        """窗口关闭事件处理"""
        # 停止发送
        if self.message_sender.is_active():
            self.message_sender.stop_sending()
        
        # 断开OSC连接
        self.osc_client.disconnect()
        
        # 自动保存所有配置
        self.auto_save_config()
        
        # 关闭窗口
        self.root.destroy()