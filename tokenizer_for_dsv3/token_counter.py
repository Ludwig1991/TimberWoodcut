# -*- coding: utf-8 -*-
"""
Token 计数器 - DeepSeek-V3 (128K BPE)
用法:
  python token_counter.py "你好世界"
  python token_counter.py -f input.txt
  python token_counter.py -c 65536 -v "很长的文本..."
  echo "文本" | python token_counter.py -
"""
import sys
import argparse

TOKENIZER_PATH = r"E:\deepseek_v3_tokenizer\deepseek_v3_tokenizer\tokenizer.json"
CONTEXT_WINDOWS = {
    "v3": 16384,
    "v3-128k": 131072,
    "r1": 65536,
}

_tokenizer = None
def get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        from tokenizers import Tokenizer
        _tokenizer = Tokenizer.from_file(TOKENIZER_PATH)
    return _tokenizer

def count_tokens(text):
    t = get_tokenizer()
    enc = t.encode(text)
    return len(enc.ids), enc.ids, enc.tokens

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description="Token Counter (DeepSeek-V3 128K BPE)")
    parser.add_argument("text", nargs="?", help="Text to count, or '-' for stdin")
    parser.add_argument("-f", "--file", help="Read text from file")
    parser.add_argument("-c", "--context", type=int, default=0, help="Max context window size")
    parser.add_argument("--model", choices=CONTEXT_WINDOWS.keys(), default=None, help="Preset context window")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show token details")
    parser.add_argument("--cost", type=float, default=0, help="Price per 1M input tokens")
    parser.add_argument("--cost-out", type=float, default=0, help="Price per 1M output tokens (estimate same token count)")
    args = parser.parse_args()

    ctx = args.context or CONTEXT_WINDOWS.get(args.model, 16384)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text == "-":
        sys.stdin.reconfigure(encoding='utf-8', errors='replace')
        text = sys.stdin.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        return

    num_tokens, ids, tokens = count_tokens(text)
    char_count = len(text)

    print(f"=== Token Count ===")
    print(f"Characters : {char_count:,}")
    print(f"Tokens     : {num_tokens:,}")
    print(f"Ratio      : {char_count/max(num_tokens,1):.1f} chars/token")

    if ctx:
        pct = num_tokens / ctx * 100
        print(f"Context    : {ctx:,} ({pct:.1f}% used)")
        print(f"Remaining  : {ctx - num_tokens:,}")
        if num_tokens > ctx:
            print(f"OVERFLOW   : +{num_tokens - ctx:,} tokens over limit!")

    if args.cost:
        cost_in = num_tokens / 1_000_000 * args.cost
        print(f"Input cost : ${cost_in:.6f} (at ${args.cost}/1M)")
    if args.cost_out:
        cost_out = num_tokens / 1_000_000 * args.cost_out
        print(f"Output est : ${cost_out:.6f} (at ${args.cost_out}/1M, same token count)")

    if args.verbose:
        # 显示前50个token
        display = tokens[:50]
        print(f"Tokens     : {display}{'...' if len(tokens) > 50 else ''}")
        print(f"IDs        : {ids[:50]}{'...' if len(ids) > 50 else ''}")

if __name__ == "__main__":
    main()
