#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller打包脚本
用于生成可执行文件
"""

import PyInstaller.__main__
import os
import sys
import shutil


def build_executable():
    """构建可执行文件"""
    
    # 清理之前的构建文件
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # PyInstaller参数
    args = [
        "main.py",  # 主程序文件
        "--name=VRChat-OSC-Sender",  # 程序名称
        "--windowed",  # 无控制台窗口（GUI程序）
        "--onefile",  # 打包成单个文件
        "--clean",  # 清理临时文件
        "--noconfirm",  # 覆盖现有文件
        "--add-data=README.md;.",  # 包含README文件
        "--icon=NONE",  # 如果有图标可以添加
        "--version-file=version_info.txt",  # 版本信息文件
    ]
    
    # 执行打包
    PyInstaller.__main__.run(args)
    
    print("打包完成！")
    print("可执行文件位于: dist/VRChat-OSC-Sender.exe")


if __name__ == "__main__":
    build_executable()