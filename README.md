# VRChat OSC消息定时发送器

一个使用Python开发的简单工具，用于定时向VRChat发送OSC聊天消息。(从创建到完成打包34分钟)

## 功能特点

- 🎯 支持通过OSC协议向VRChat发送聊天消息
- ⏰ 可设置任意时间间隔自动发送消息
- 🖥️ 简洁易用的图形界面
- 💾 配置自动保存和加载
- 📦 支持打包为独立可执行文件

## 安装和使用

### 方法1：直接运行Python程序

1. 安装Python 3.7或更高版本
2. 安装依赖库：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行程序：
   ```bash
   python main.py
   ```

### 方法2：使用打包好的可执行文件

1. 运行 `build.bat` 生成可执行文件
2. 在 `dist/` 目录下找到 `VRChat-OSC-Sender.exe`
3. 双击即可运行，无需安装Python环境

## 使用说明

### 界面功能

1. **OSC设置**
   - IP地址：VRChat运行的IP地址（通常是127.0.0.1）
   - 端口：VRChat的OSC端口（默认9000）
   - 测试连接：测试OSC连接是否正常

2. **消息设置**
   - 发送间隔：消息发送的时间间隔（秒）
   - 消息内容：要发送的聊天消息文本

3. **控制按钮**
   - 开始发送：启动定时消息发送
   - 停止发送：停止消息发送
   - 保存配置：保存当前设置到配置文件

### VRChat设置

在VRChat中启用OSC：
1. 打开VRChat设置
2. 进入「OSC」选项卡
3. 启用「OSC Enabled」
4. 确保端口设置为9000（或程序中设置的端口）

## 配置文件

程序会自动创建和读取 `config.json` 文件，保存以下设置：
- OSC服务器IP地址
- OSC端口
- 消息发送间隔
- 消息内容
- 窗口位置和大小

## 技术细节

- **通信协议**：OSC (Open Sound Control)
- **目标地址**：/chatbox/input
- **开发语言**：Python 3.7+
- **GUI框架**：tkinter
- **OSC库**：python-osc

## 故障排除

### 连接失败
- 确保VRChat正在运行
- 检查VRChat中是否启用了OSC
- 确认IP地址和端口设置正确
- 检查防火墙设置

### 消息不显示
- 确认VRChat中的聊天框已打开
- 检查消息内容是否为空
- 尝试手动在VRChat中发送消息确认OSC功能正常

## 开发

### 打包程序
```bash
# 安装打包工具
pip install pyinstaller

# 运行打包脚本
python build.py

# 或使用批处理文件
build.bat
```

### 项目结构
```
osc-timer/
├── main.py              # 主程序入口
├── gui.py               # GUI界面类
├── osc_client.py        # OSC通信封装
├── message_sender.py    # 消息发送管理
├── config_manager.py    # 配置文件管理
├── build.py             # 打包脚本
├── build.bat            # Windows打包批处理
├── requirements.txt     # 依赖列表
└── README.md           # 项目说明
```

## 许可证

MIT License - 详见LICENSE文件