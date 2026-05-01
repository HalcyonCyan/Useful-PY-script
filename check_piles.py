import os
from pathlib import Path

def get_size(path):
    """递归计算路径大小（文件直接返回，文件夹计算所有子项）"""
    p = Path(path)
    try:
        if p.is_file():
            return p.stat().st_size
        elif p.is_dir():
            # 使用 sum 和 generator 提高效率
            return sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
    except (PermissionError, FileNotFoundError):
        return 0
    return 0

def format_size(size):
    """单位转换"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def analyze_downloads(target_path):
    root = Path(target_path)
    if not root.exists():
        print(f"路径不存在: {target_path}")
        return

    archive_exts = {'.zip', '.rar', '.7z', '.tar', '.gz', '.iso', '.dmg'}
    
    total_folder_size = 0
    total_archives_size = 0
    items_list = []

    print(f"正在深度扫描: {target_path} ...\n")

    # 遍历第一层级
    for entry in root.iterdir():
        try:
            # 计算该项大小（若是文件夹则递归）
            current_size = get_size(entry)
            total_folder_size += current_size
            
            # 判断类型
            is_dir = entry.is_dir()
            entry_type = "文件夹" if is_dir else "文件"
            
            # 统计压缩包总大小（包括第一层和文件夹内部的）
            if not is_dir:
                if entry.suffix.lower() in archive_exts:
                    total_archives_size += current_size
            else:
                # 统计子文件夹内包含的压缩包
                for f in entry.rglob('*'):
                    if f.is_file() and f.suffix.lower() in archive_exts:
                        try:
                            total_archives_size += f.stat().st_size
                        except: pass

            items_list.append({
                "name": entry.name,
                "size": current_size,
                "type": entry_type
            })
        except Exception as e:
            continue

    # 排序并取前30
    items_list.sort(key=lambda x: x['size'], reverse=True)
    top_30 = items_list[:30]

    # 输出统计概要
    print("=" * 60)
    print(f"【总体统计】")
    print(f"下载文件夹总占用: {format_size(total_folder_size)}")
    print(f"各类压缩包总占用: {format_size(total_archives_size)}")
    print("=" * 60)

    # 输出 Top 30 表格
    print(f"{'排名':<4} | {'类型':<8} | {'大小':<12} | {'名称'}")
    print("-" * 80)
    for i, item in enumerate(top_30, 1):
        print(f"{i:<4} | {item['type']:<8} | {format_size(item['size']):<12} | {item['name']}")

if __name__ == "__main__":
    # 指定路径
    target = r"YOURS"
    analyze_downloads(target)