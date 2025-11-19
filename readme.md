# 关于网页

这是21点助手，帮助你做出最佳决策

可以部署到CF/Github Pages

# 使用前安装外部库

- `pip install keyboard`

- `pip install psutil`

# 打包说明

1. 安装 PyInstaller

- `pip install pyinstaller`

2. 打包

- `pyinstaller --noconsole --onefile ./罪神辅助.py`
- `pyinstaller --onefile .\挂机.py`

- `dist/` 目录：存放最终生成的可执行文件

# git走代理

- 设置代理`git config --global http.proxy http://127.0.0.1:6666`

- 取消代理`git config --global --unset http.proxy`