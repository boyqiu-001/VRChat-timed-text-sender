@echo off
echo 正在安装依赖...
pip install -r requirements.txt

echo 正在构建可执行文件...
python build.py

echo 构建完成！
pause