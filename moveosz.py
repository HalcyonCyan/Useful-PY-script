import os
import shutil

source_dir = r"YOURS"
target_dir = r"YOURS"

# 确保目标文件夹存在
os.makedirs(target_dir, exist_ok=True)

moved_count = 0
skipped_count = 0

for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith(".osz"):
            src_path = os.path.join(root, file)
            dst_path = os.path.join(target_dir, file)

            # 如果目标目录里已经有同名文件，自动改名避免覆盖
            if os.path.exists(dst_path):
                name, ext = os.path.splitext(file)
                i = 1
                while True:
                    new_name = f"{name}_{i}{ext}"
                    new_dst_path = os.path.join(target_dir, new_name)
                    if not os.path.exists(new_dst_path):
                        dst_path = new_dst_path
                        break
                    i += 1

            try:
                shutil.move(src_path, dst_path)
                print(f"已移动: {src_path} -> {dst_path}")
                moved_count += 1
            except Exception as e:
                print(f"移动失败: {src_path}\n原因: {e}")
                skipped_count += 1

print(f"\n完成！共移动 {moved_count} 个文件，失败/跳过 {skipped_count} 个文件。")