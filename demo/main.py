import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tewtoken import (
    encode, decode, tokenize, count_tokens,
    encode_batch, decode_batch, truncate, encoding_info
)

def print_separator():
    print("\n" + "─" * 50 + "\n")

def demo_single(text):
    print(f"Input      : {text}")
    print(f"Tokens     : {tokenize(text)}")
    print(f"Token IDs  : {encode(text)}")
    print(f"Token count: {count_tokens(text)}")
    print(f"Decoded    : {decode(encode(text))}")

def main():
    # ── 1. Tokenizer info ────────────────────────────────
    print("═" * 50)
    print("       BPE TOKENIZER — DEMO")
    print("═" * 50)
    info = encoding_info()
    for k, v in info.items():
        print(f"  {k}: {v}")

    print_separator()

    # ── 2. English example ───────────────────────────────
    print("[ English ]")
    demo_single("machine learning is amazing")

    print_separator()

    # ── 3. Hindi example ─────────────────────────────────
    print("[ Hindi ]")
    demo_single("यह एक परीक्षण है")

    print_separator()

    # ── 4. Batch encode/decode ───────────────────────────
    print("[ Batch Encode ]")
    texts = ["transformers are powerful", "deep learning rocks", "नमस्ते दुनिया"]
    ids_list = encode_batch(texts)
    decoded_list = decode_batch(ids_list)
    for original, ids, decoded in zip(texts, ids_list, decoded_list):
        print(f"  {original} → {ids} → {decoded}")

    print_separator()

    # ── 5. Truncate example ──────────────────────────────
    print("[ Truncate ]")
    long_text = "machine learning is a subset of artificial intelligence"
    print(f"Original : {long_text}")
    print(f"Truncated to 4 tokens: {truncate(long_text, 4)}")

    print_separator()

    # ── 6. Interactive mode ──────────────────────────────
    print("[ Interactive Mode — type any text, q to quit ]\n")
    while True:
        text = input("Enter text: ").strip()
        if text.lower() == 'q':
            print("Bye!")
            break
        if not text:
            continue
        demo_single(text)
        print()

if __name__ == "__main__":
    main()