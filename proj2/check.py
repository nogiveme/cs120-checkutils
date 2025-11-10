#!/usr/bin/env python3
import random
import secrets
import os
import sys  # 导入 sys 模块来读取命令行参数

def generate(filename, key, count_bytes=6250):
    """
    使用一个 key 稳定地生成一个指定字节长度的二进制文件。
    Key 限制在 0-99 之间。
    """
    if not (0 <= key <= 99):
        print(f"Error: Key must be between 0 and 99. Got: {key}")
        return

    # 打印将要使用的 key，格式化为两位数 (例如 05, 12, 99)
    print(f"using key: {key:02d}")
    
    # 使用 key 作为随机种子
    random.seed(key)
    
    # 生成指定字节数的随机二进制数据
    data = random.randbytes(count_bytes)
    
    if os.path.exists(filename):
        print(f"Error: File {filename} already exists. Generation aborted.")
        return
    

    with open(filename, 'wb') as f:
        f.write(data)
    
    print(f"generated: {filename} ({count_bytes} bytes)")


def diff(file1, file2):
    """
    比较两个文件的二进制内容。
    """
    try:
        # 以二进制读取 ('rb') 模式打开文件
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            c1, c2 = f1.read(), f2.read()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    max_len = max(len(c1), len(c2))
    matches = sum(a == b for a, b in zip(c1, c2))
    similarity = matches / max_len * 100 if max_len else 100
    
    print(f"\n{'='*50}")
    print(f"file 1: {file1} ({len(c1)} bytes)")
    print(f"file 2: {file2} ({len(c2)} bytes)")
    print(f"matches: {matches}/{max_len}")
    print(f"similarity: {similarity:.2f}%")
    print(f"identical: {'yes ✓' if c1 == c2 else 'no ✗'}")
    print(f"{'='*50}\n")


def main():
    num_args = len(sys.argv)
    
    if num_args == 1:
        # 场景 2: 直接运行 python check.py
        # 生成一个 0-99 之间的随机 key
        key = secrets.randbelow(100)
        print("No arguments provided. Generating INPUT.bin with random key...")
        generate('INPUT.bin', key, count_bytes=6250)
    elif num_args == 2:
        # 运行 python check.py <key>
        key = int(sys.argv[1])
        print("Generating OUTPUT.bin with key:", key)
        generate('OUTPUT.bin', key, count_bytes=6250)
    elif num_args == 3:
        # 场景 3: 运行 python check.py in.bin out.bin
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        diff(file1, file2)
        
    else:
        print("Usage:")
        print("  python check.py             (Generates INPUT.bin with a random 00-99 key)")
        print("  python check.py <file1> <file2> (Compares two files)")


if __name__ == '__main__':
    main()