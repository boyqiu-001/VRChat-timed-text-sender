#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件管理器
用于保存和加载用户设置
"""

import json
import os


class ConfigManager:
    """配置文件管理类"""
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        default_config = {
            "osc_ip": "127.0.0.1",
            "osc_port": 9000,
            "message_interval": 5,
            "message_text": "Hello VRChat!",
            "window_geometry": "400x300+100+100"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 合并默认配置和加载的配置
                    for key, value in default_config.items():
                        if key not in loaded_config:
                            loaded_config[key] = value
                    return loaded_config
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                return default_config
        else:
            return default_config
    
    def save_config(self, config_dict):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def get(self, key, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置项"""
        self.config[key] = value
    
    def get_all(self):
        """获取所有配置"""
        return self.config.copy()
    
    def update_all(self, config_dict):
        """更新所有配置"""
        self.config.update(config_dict)
        self.save_config(self.config)