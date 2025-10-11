#!/usr/bin/env python3
import random
import argparse
import secrets


def generate(filename, count=10000, seed=None):
    if seed is None:
        seed = secrets.randbits(32)
        print(f"using random seed: {seed}")
    else:
        print(f"using seed: {seed}")
    
    random.seed(seed)
    data = ''.join(str(random.randint(0, 1)) for _ in range(count))
    
    with open(filename, 'w') as f:
        f.write(data)
    print(f"generated: {filename} ({count} bits)")


def diff(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        c1, c2 = f1.read().strip(), f2.read().strip()
    
    max_len = max(len(c1), len(c2))
    matches = sum(a == b for a, b in zip(c1, c2))
    similarity = matches / max_len * 100 if max_len else 100
    
    print(f"\n{'='*50}")
    print(f"file 1: {file1} ({len(c1)} bits)")
    print(f"file 2: {file2} ({len(c2)} bits)")
    print(f"matches: {matches}/{max_len}")
    print(f"similarity: {similarity:.2f}%")
    print(f"identical: {'yes ✓' if c1 == c2 else 'no ✗'}")
    print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(description='binary file generator and diff tool')
    sub = parser.add_subparsers(dest='cmd')
    
    gen = sub.add_parser('generate', help='generate binary file')
    gen.add_argument('filename')
    gen.add_argument('--count', type=int, default=10000)
    gen.add_argument('--seed', type=int)

    dif = sub.add_parser('diff', help='compare two files')
    dif.add_argument('file1')
    dif.add_argument('file2')
    
    args = parser.parse_args()
    
    if args.cmd == 'generate':
        generate(args.filename, args.count, args.seed)
    elif args.cmd == 'diff':
        diff(args.file1, args.file2)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
