#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSC客户端封装
用于与VRChat进行OSC通信
"""

from pythonosc import udp_client
from pythonosc import osc_message_builder
import socket


class OSCClient:
    """OSC客户端类"""
    
    def __init__(self, ip="127.0.0.1", port=9000):
        self.ip = ip
        self.port = port
        self.client = None
        self.connected = False
    
    def connect(self):
        """连接到OSC服务器"""
        try:
            self.client = udp_client.SimpleUDPClient(self.ip, self.port)
            # 测试连接
            self.client.send_message("/test", 1)
            self.connected = True
            return True
        except Exception as e:
            print(f"OSC连接失败: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """断开连接"""
        self.client = None
        self.connected = False
    
    def send_chat_message(self, message):
        """发送聊天消息到VRChat
        
        VRChat接收聊天消息的OSC地址是：/chatbox/input
        参数：消息文本，布尔值（是否立即发送），布尔值（是否覆盖）
        """
        if not self.connected or not self.client:
            return False
        
        try:
            # VRChat的OSC聊天消息格式
            self.client.send_message("/chatbox/input", [message, True, False])
            return True
        except Exception as e:
            print(f"发送消息失败: {e}")
            return False
    
    def set_keyboard(self, enabled=True):
        """设置键盘输入状态"""
        if not self.connected or not self.client:
            return False
        
        try:
            self.client.send_message("/chatbox/typing", enabled)
            return True
        except Exception as e:
            print(f"设置键盘状态失败: {e}")
            return False
    
    def test_connection(self, ip, port):
        """测试OSC连接"""
        try:
            test_client = udp_client.SimpleUDPClient(ip, port)
            test_client.send_message("/test", 1)
            return True
        except Exception:
            return False