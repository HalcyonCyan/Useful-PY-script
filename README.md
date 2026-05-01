# Python Utility Scripts

一个我使用过的 Python 实用脚本集合，供大家使用

---

## 功能概览

| 脚本                | 功能                                                              |
| ------------------- | ----------------------------------------------------------------- |
| `check_cudaPLUS.py` | 自动检测系统 CUDA 版本，并提示推荐安装的 CuPy 包                  |
| `checkcuda.py`      | 检查 CuPy、CUDA Runtime、CUDA Driver 和 GPU 设备信息              |
| `check_yolo.py`     | 检查 Ultralytics YOLO、PyTorch、CUDA、OpenCV 等环境信息           |
| `check_piles.py`    | 扫描指定目录，统计文件夹大小、压缩包大小，并输出占用空间 Top 30   |
| `moveosz.py`        | 递归查找并移动 `.osz` 文件到目标目录，自动避免同名覆盖            |
| `split_pic.py`      | 将图片和 YOLO 标签按比例划分为训练集 / 验证集，并生成 `data.yaml` |

---

````

---

## 环境要求



基础脚本主要依赖 Python 标准库：

```text
os
shutil
pathlib
subprocess
platform
re
random
````

部分脚本需要额外安装依赖：

```bash
pip install pyyaml
pip install torch
pip install ultralytics
pip install opencv-python
```

```bash
pip install cupy-cuda12x
```

或者运行：

```bash
python check_cudaPLUS.py
```

---

## 使用方法

### 1. 检测 CUDA 版本并推荐 CuPy 包

```bash
python check_cudaPLUS.py
```

功能：

- 检测 `nvcc --version`
- 检测 `nvidia-smi`
- 在 Windows 上尝试读取 `CUDA_PATH`
- 根据 CUDA 版本推荐对应的 CuPy 安装包
- 可选择是否立即安装

示例输出：

```text
正在检测系统 CUDA 版本...
检测到 CUDA 版本: 12.8
建议安装的 CuPy 包: cupy-cuda12x
安装命令: pip install cupy-cuda12x
```

---

### 2. 检查 CuPy 与 CUDA 运行环境

```bash
python checkcuda.py
```

功能：

- 输出 CuPy 版本
- 输出 CUDA Runtime 版本
- 输出 CUDA Driver 版本
- 输出 GPU 数量
- 输出第 0 张 GPU 的设备名称

适用于确认 CuPy 是否能正常调用本机 CUDA 环境。

---

### 3. 检查 YOLO / PyTorch / CUDA / OpenCV 环境

```bash
python check_yolo.py
```

功能：

- 输出 Ultralytics 版本
- 输出 PyTorch 版本
- 检查 PyTorch 是否可用 CUDA
- 输出 OpenCV 版本

适用于训练 YOLO 模型前快速确认环境是否安装正确。

---

### 4. 分析目录空间占用

打开 `check_piles.py`，修改底部路径：

```python
target = r"YOURS"
```

例如：

```python
target = r"D:\Downloads"
```

然后运行：

```bash
python check_piles.py
```

功能：

- 递归统计目标目录总大小
- 统计 `.zip`、`.rar`、`.7z`、`.tar`、`.gz`、`.iso`、`.dmg` 等压缩包总大小
- 输出第一层文件 / 文件夹占用空间 Top 30

适合清理下载目录、数据集目录、实验输出目录等。

---

### 5. 批量移动 `.osz` 文件

玩osu导致的

打开 `moveosz.py`，修改源目录和目标目录：

```python
source_dir = r"YOURS"
target_dir = r"YOURS"
```

例如：

```python
source_dir = r"D:\Downloads"
target_dir = r"D:\osu_songs"
```

然后运行：

```bash
python moveosz.py
```

功能：

- 递归扫描源目录
- 查找所有 `.osz` 文件
- 移动到目标目录
- 如果目标目录存在同名文件，会自动重命名为 `xxx_1.osz`、`xxx_2.osz` 等，避免覆盖

---

### 6. 划分 YOLO 数据集并生成 `data.yaml`

`split_pic.py` 用于将按类别存放的图片和标签划分为 YOLO 训练格式。

默认类别：

```python
categories = ['shampoo', 'sprite', 'water', 'chip', 'cola', 'Handwash', 'lays', 'Pocky']
```

默认输入结构：

```text
images_root/
├── shampoo/
├── sprite/
├── water/
└── ...

labels_root/
├── shampoo/
├── sprite/
├── water/
└── ...
```

每张图片需要有对应的 YOLO 标签文件，例如：

```text
images_root/shampoo/001.jpg
labels_root/shampoo/001.txt
```

打开 `split_pic.py`，修改路径：

```python
images_root = r"YOURS\datas"
labels_root = r"YOURS\labels"
output_root = r"YOURS\yolo_dataset"
```

然后运行：

```bash
python split_pic.py
```

输出结构：

```text
yolo_dataset/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
└── data.yaml
```

生成的 `data.yaml` 类似：

```yaml
train: /path/to/yolo_dataset/train/images
val: /path/to/yolo_dataset/val/images
nc: 8
names:
  - shampoo
  - sprite
  - water
  - chip
  - cola
  - Handwash
  - lays
  - Pocky
```

---

## License

建议使用 [MIT License](https://opensource.org/license/mit/)。

---

## 贡献

欢迎提交 Issue 或 Pull Request 来改进脚本，例如：
