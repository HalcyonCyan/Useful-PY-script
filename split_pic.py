import os
import shutil
import random
import yaml
from pathlib import Path


def split_dataset(images_root, labels_root, output_root, train_ratio=0.8):
    """
    分离数据集为训练集和验证集

    参数:
    images_root: 原始图片根目录
    labels_root: 原始标签根目录
    output_root: 输出根目录
    train_ratio: 训练集比例
    """
    # 创建输出目录结构
    train_images_dir = os.path.join(output_root, 'train', 'images')
    train_labels_dir = os.path.join(output_root, 'train', 'labels')
    val_images_dir = os.path.join(output_root, 'val', 'images')
    val_labels_dir = os.path.join(output_root, 'val', 'labels')

    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(val_images_dir, exist_ok=True)
    os.makedirs(val_labels_dir, exist_ok=True)

    # 获取所有类别
    categories = ['shampoo', 'sprite', 'water', 'chip', 'cola', 'Handwash', 'lays', 'Pocky']

    # 处理每个类别
    for category in categories:
        print(f"处理类别: {category}")

        # 获取当前类别的所有图片和标签
        category_images_dir = os.path.join(images_root, category)
        category_labels_dir = os.path.join(labels_root, category)

        # 获取所有图片文件
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
            image_files.extend(Path(category_images_dir).glob(ext))

        # 随机打乱文件列表
        random.shuffle(image_files)

        # 计算训练集和验证集的分界点
        split_idx = int(len(image_files) * train_ratio)
        train_files = image_files[:split_idx]
        val_files = image_files[split_idx:]

        print(f"  {category}: 总共 {len(image_files)} 个样本, 训练集 {len(train_files)}, 验证集 {len(val_files)}")

        # 复制训练集
        for img_path in train_files:
            # 复制图片
            img_name = img_path.name
            dst_img_path = os.path.join(train_images_dir, img_name)
            shutil.copy2(img_path, dst_img_path)

            # 复制对应的标签文件
            label_name = img_path.stem + '.txt'
            src_label_path = os.path.join(category_labels_dir, label_name)
            dst_label_path = os.path.join(train_labels_dir, label_name)

            if os.path.exists(src_label_path):
                shutil.copy2(src_label_path, dst_label_path)
            else:
                print(f"警告: 未找到标签文件 {src_label_path}")

        # 复制验证集
        for img_path in val_files:
            # 复制图片
            img_name = img_path.name
            dst_img_path = os.path.join(val_images_dir, img_name)
            shutil.copy2(img_path, dst_img_path)

            # 复制对应的标签文件
            label_name = img_path.stem + '.txt'
            src_label_path = os.path.join(category_labels_dir, label_name)
            dst_label_path = os.path.join(val_labels_dir, label_name)

            if os.path.exists(src_label_path):
                shutil.copy2(src_label_path, dst_label_path)
            else:
                print(f"警告: 未找到标签文件 {src_label_path}")

    print(f"数据集分离完成! 输出目录: {output_root}")

    return train_images_dir, train_labels_dir, val_images_dir, val_labels_dir, categories


def create_data_yaml(output_root, categories, train_images_dir, val_images_dir):
    """
    创建 data.yaml 文件

    参数:
    output_root: 输出根目录
    categories: 类别列表
    train_images_dir: 训练集图片目录
    val_images_dir: 验证集图片目录
    """
    # 创建数据配置
    data_config = {
        'train': str(Path(train_images_dir).as_posix()),  # 使用正斜杠路径
        'val': str(Path(val_images_dir).as_posix()),  # 使用正斜杠路径
        'nc': len(categories),
        'names': categories
    }

    # 写入YAML文件
    yaml_path = os.path.join(output_root, 'data.yaml')
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(data_config, f, default_flow_style=False, allow_unicode=True)

    print(f"data.yaml 文件已创建: {yaml_path}")

    return yaml_path


def main():
    # 设置路径
    images_root = r"YOURS\datas"  # 图片根目录
    labels_root = r"YOURS\labels"  # 标签根目录
    output_root = r"YOURS\yolo_dataset"  # 输出根目录

    # 分离数据集
    train_images_dir, train_labels_dir, val_images_dir, val_labels_dir, categories = split_dataset(
        images_root, labels_root, output_root, train_ratio=0.8
    )

    # 创建data.yaml文件
    yaml_path = create_data_yaml(output_root, categories, train_images_dir, val_images_dir)

    print("\n完成!")
    print(f"数据集已分离到: {output_root}")
    print(f"训练集: {len(os.listdir(train_images_dir))} 张图片")
    print(f"验证集: {len(os.listdir(val_images_dir))} 张图片")
    print(f"配置文件: {yaml_path}")


if __name__ == "__main__":
    main()