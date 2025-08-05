#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VRChat OSC消息定时发送器
主程序入口
"""

import sys
import os
from gui import OSCSenderGUI

if __name__ == "__main__":
    # 确保在Windows上正确显示中文
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    
    # 启动GUI
    app = OSCSenderGUI()
    app.run()