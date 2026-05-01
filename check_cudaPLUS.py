#!/usr/bin/env python3
"""
自动检测 CUDA 版本并提示安装正确 CuPy 包的脚本
"""

import subprocess
import sys
import re
import platform


def run_command(cmd):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None


def get_cuda_version():
    """获取 CUDA 版本"""
    # 方法1: 检查 nvcc 版本
    nvcc_output = run_command("nvcc --version")
    if nvcc_output:
        match = re.search(r"release (\d+\.\d+)", nvcc_output)
        if match:
            return match.group(1)

    # 方法2: 检查 nvidia-smi 中的 CUDA 版本
    nvidia_smi_output = run_command("nvidia-smi")
    if nvidia_smi_output:
        match = re.search(r"CUDA Version:\s*(\d+\.\d+)", nvidia_smi_output)
        if match:
            return match.group(1)

    # 方法3: 在 Windows 上检查 CUDA 安装路径
    if platform.system() == "Windows":
        import os
        cuda_path = os.environ.get("CUDA_PATH", "")
        if cuda_path:
            version_match = re.search(r"v(\d+\.\d+)", cuda_path)
            if version_match:
                return version_match.group(1)

    return None


def get_cupy_cuda_package(cuda_version):
    """根据 CUDA 版本返回对应的 CuPy 包名"""
    if not cuda_version:
        return None

    major, minor = cuda_version.split('.')[:2]
    version_code = f"{major}{minor}"

    # CuPy 包命名规则
    cupy_packages = {
        "12": "cupy-cuda12x",
        "11": "cupy-cuda11x",
        "10": "cupy-cuda10x",
        "9": "cupy-cuda90",
    }

    # 查找最接近的版本
    for ver in sorted(cupy_packages.keys(), reverse=True):
        if int(version_code) >= int(ver):
            return cupy_packages[ver]

    return None


def main():
    print("正在检测系统 CUDA 版本...")

    cuda_version = get_cuda_version()

    if not cuda_version:
        print("未检测到 CUDA 安装，请先安装 CUDA Toolkit")
        print("访问: https://developer.nvidia.com/cuda-downloads")
        return

    print(f"检测到 CUDA 版本: {cuda_version}")

    cupy_package = get_cupy_cuda_package(cuda_version)

    if not cupy_package:
        print(f"未找到适用于 CUDA {cuda_version} 的 CuPy 包")
        print("请访问 https://docs.cupy.dev/en/stable/install.html 查看支持的版本")
        return

    print(f"\n建议安装的 CuPy 包: {cupy_package}")
    print(f"安装命令: pip install {cupy_package}")

    # 询问用户是否立即安装
    response = input("\n是否立即安装? (y/N): ").lower()
    if response in ['y', 'yes']:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", cupy_package], check=True)
            print("安装完成!")
        except subprocess.CalledProcessError:
            print("安装失败，请检查网络连接或手动安装")


if __name__ == "__main__":
    main()