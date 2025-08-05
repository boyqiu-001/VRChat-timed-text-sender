#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息发送管理器
用于定时向VRChat发送消息
"""

import threading
import time
from osc_client import OSCClient


class MessageSender:
    """消息发送管理类"""
    
    def __init__(self, osc_client):
        self.osc_client = osc_client
        self.is_running = False
        self.timer = None
        self.message_text = ""
        self.interval = 5
        self.send_count = 0
        self.on_status_change = None  # 状态变化回调
        self.on_message_sent = None   # 消息发送回调
    
    def start_sending(self, message_text, interval):
        """开始定时发送消息"""
        if self.is_running:
            return False
        
        self.message_text = message_text
        self.interval = max(1, int(interval))  # 最小间隔1秒
        self.send_count = 0
        self.is_running = True
        
        if self.on_status_change:
            self.on_status_change(True)
        
        self._schedule_next_send()
        return True
    
    def update_message_text(self, new_message_text):
        """实时更新消息内容"""
        self.message_text = new_message_text
    
    def stop_sending(self):
        """停止定时发送"""
        self.is_running = False
        
        if self.timer:
            self.timer.cancel()
            self.timer = None
        
        if self.on_status_change:
            self.on_status_change(False)
    
    def _schedule_next_send(self):
        """调度下一次发送"""
        if self.is_running:
            self.timer = threading.Timer(self.interval, self._send_message)
            self.timer.start()
    
    def _send_message(self):
        """发送消息"""
        if not self.is_running:
            return
        
        try:
            success = self.osc_client.send_chat_message(self.message_text)
            if success:
                self.send_count += 1
                if self.on_message_sent:
                    self.on_message_sent(self.message_text, self.send_count)
        except Exception as e:
            print(f"发送消息时出错: {e}")
        
        # 继续调度下一次发送
        self._schedule_next_send()
    
    def get_status(self):
        """获取当前状态"""
        return {
            "is_running": self.is_running,
            "message_text": self.message_text,
            "interval": self.interval,
            "send_count": self.send_count
        }
    
    def is_active(self):
        """检查是否正在运行"""
        return self.is_running