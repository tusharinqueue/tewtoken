import json
import re
import os

# ── 1. Dynamic paths ─────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB_PATH = os.path.join(BASE_DIR, "data", "vocab.json")
MERGES_PATH = os.path.join(BASE_DIR, "data", "merges.txt")

# ── 2. Load vocab and merges ─────────────────────────────────
with open(VOCAB_PATH, "r", encoding="utf-8") as f:
    token_to_id = json.load(f)

with open(MERGES_PATH, "r", encoding="utf-8") as f:
    merges = [tuple(line.strip().split(" ", 1)) for line in f.readlines()]

id_to_token_map = {idx: token for token, idx in token_to_id.items()}


# ── 3. Core: Encode ──────────────────────────────────────────
def encode(text):
    """Convert text to list of token IDs"""
    text = text.lower()
    words = re.findall(r'\S+', text)
    all_ids = []
    for word in words:
        tokens = list(word) + ['</w>']
        for pair in merges:
            bigram = pair[0] + pair[1]
            i = 0
            new_tokens = []
            while i < len(tokens):
                if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i + 1] == pair[1]:
                    new_tokens.append(bigram)
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            tokens = new_tokens
        for token in tokens:
            if token in token_to_id:
                all_ids.append(token_to_id[token])
            else:
                for ch in token:
                    if ch in token_to_id:
                        all_ids.append(token_to_id[ch])
    return all_ids


# ── 4. Core: Decode ──────────────────────────────────────────
def decode(ids):
    """Convert list of token IDs back to text"""
    tokens = [id_to_token_map.get(i, '') for i in ids]
    text = ''.join(tokens)
    text = text.replace('</w>', ' ')
    return text.strip()


# ── 5. tokenize: returns token strings instead of IDs ────────
def tokenize(text):
    """Returns list of token strings (not IDs)

    Example:
        tokenize("machine learning") → ['machine</w>', 'learning</w>']
    """
    ids = encode(text)
    return [id_to_token_map.get(i, '') for i in ids]


# ── 6. count_tokens ──────────────────────────────────────────
def count_tokens(text):
    """Returns number of tokens in a text string

    Example:
        count_tokens("machine learning is amazing") → 4
    """
    return len(encode(text))


# ── 7. encode_batch ──────────────────────────────────────────
def encode_batch(texts):
    """Encode a list of strings at once

    Example:
        encode_batch(["hello world", "machine learning"])
        → [[ids...], [ids...]]
    """
    return [encode(text) for text in texts]


# ── 8. decode_batch ──────────────────────────────────────────
def decode_batch(ids_list):
    """Decode a list of token ID lists at once

    Example:
        decode_batch([[id1, id2], [id3, id4]])
        → ["hello world", "machine learning"]
    """
    return [decode(ids) for ids in ids_list]


# ── 9. vocab_size ────────────────────────────────────────────
def vocab_size():
    """Returns total number of tokens in vocabulary"""
    return len(token_to_id)


# ── 10. get_vocab ────────────────────────────────────────────
def get_vocab():
    """Returns full vocabulary as dict {token: id}"""
    return token_to_id


# ── 11. token_to_id_single ───────────────────────────────────
def get_token_id(token):
    """Get ID for a single token string

    Example:
        get_token_id("machine</w>") → 2839
    """
    return token_to_id.get(token, None)


# ── 12. id_to_token_single ───────────────────────────────────
def get_id_token(id):
    """Get token string for a single ID

    Example:
        get_id_token(2839) → 'machine</w>'
    """
    return id_to_token_map.get(id, None)


# ── 13. is_known_token ───────────────────────────────────────
def is_known_token(token):
    """Check if a token exists in vocabulary

    Example:
        is_known_token("machine</w>") → True
        is_known_token("xyzabc</w>")  → False
    """
    return token in token_to_id


# ── 14. truncate ─────────────────────────────────────────────
def truncate(text, max_tokens):
    """Truncate text to a maximum number of tokens

    Example:
        truncate("machine learning is amazing", 2)
        → "machine learning"
    """
    ids = encode(text)[:max_tokens]
    return decode(ids)


# ── 15. encoding_info ────────────────────────────────────────
def encoding_info():
    """Returns a summary of this tokenizer"""
    return {
        "vocab_size": vocab_size(),
        "num_merges": len(merges),
        "type": "BPE",
        "language": "bilingual (English + Hindi)",
        "lowercase": True,
    }