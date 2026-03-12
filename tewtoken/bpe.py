import re
import time
from collections import Counter, defaultdict

#just loading out corpus file
with open(r"F:\RandomProjects\tewtoken\data\corpus.txt", "r", encoding="utf-8") as f:
    text = f.read().lower()
#──────────────────────────────────────────

#cleaning our data (same as vocab.py)
text = text.replace('�', '')
text = re.sub(r'<[^>]+>', '', text)

#──────────────────────────────────────────

# WORD frequency counting (same as vocab.py)
def get_word_freqs(text):
    words = re.findall(r'\S+', text)
    return Counter(words)

word_freqs = get_word_freqs(text)
print(f"Unique words before filter: {len(word_freqs)}")

# filter out rare words — they slow down every iteration
word_freqs = {w: f for w, f in word_freqs.items() if f >= 3}
print(f"Unique words after filter: {len(word_freqs)}")

#──────────────────────────────────────────

#building vocab
"""This function transforms our word frequency dictionary into a character-level representation.
Before:
pythonword_freqs = {
    "machine": 450,
    "the": 39580,
    "है": 8426
}
After:
pythonvocab = {
    ('m','a','c','h','i','n','e','</w>'): 450,
    ('t','h','e','</w>'): 39580,
    ('ह','ै','</w>'): 8426
}
"""
def build_vocab(word_freqs):
    vocab = {}
    for word, freq in word_freqs.items(): #iterating in word , freq dict
        chars = tuple(list(word) + ['</w>']) #adding </w> after every char in word | converts list to tuple because tuples can be used as dictionary keys, lists cannot.
        vocab[chars] = freq
    return vocab

vocab = build_vocab(word_freqs) #calling our func from above

#─────────────────────────────

#counting all adjacent pairs
#This is the engine of BPE.
# For every word in vocab, look at every adjacent pair of tokens and count how often that pair appears across the entire corpus.
def get_pair_freqs(vocab):
    pairs = defaultdict(int) #Creates an empty dictionary that automatically starts any new key at 0. This will store every adjacent pair and its total frequency.
    for word_tuple, freq in vocab.items(): #loop thru every word in vocab
        for i in range(len(word_tuple) - 1): #Loop thru every position in the word tuple
            pairs[(word_tuple[i], word_tuple[i+1])] += freq #for each pair add word frequency to that pair count.
    return pairs

#─────────────────────────

#merge the most frequent pairs
def merge_pair(pair, vocab):
    new_vocab = {}
    bigram = pair[0] + pair[1]
    for word_tuple, freq in vocab.items():
        new_word = []
        i = 0
        while i < len(word_tuple):
            if i < len(word_tuple) - 1 and word_tuple[i] == pair[0] and word_tuple[i+1] == pair[1]:
                new_word.append(bigram)
                i += 2
            else:
                new_word.append(word_tuple[i])
                i += 1
        new_vocab[tuple(new_word)] = freq
    return new_vocab

#BPE training loop ────────────────────────────────────
NUM_MERGES = 8000
merges = []

print("\nRunning BPE merges...\n")
start = time.time()

for i in range(NUM_MERGES):
    pair_freqs = get_pair_freqs(vocab)

    if not pair_freqs:
        print("No more pairs found, stopping.")
        break

    best_pair = max(pair_freqs, key=pair_freqs.get)

    if pair_freqs[best_pair] < 2:
        print("No more frequent pairs, stopping early.")
        break

    vocab = merge_pair(best_pair, vocab)
    merges.append(best_pair)

    if i < 20 or i % 500 == 0:
        elapsed = time.time() - start
        print(f"Merge {i+1:4d}: {best_pair[0]} + {best_pair[1]} → '{best_pair[0]+best_pair[1]}' (freq: {pair_freqs[best_pair]}) | {elapsed:.1f}s")

print(f"\nDone! Total merges: {len(merges)}")
print(f"Total time: {time.time() - start:.1f}s")

import json

#Build final vocabulary ────────────────────────────────
# collect all unique tokens from the final vocab
all_tokens = set()
for word_tuple in vocab.keys():
    for token in word_tuple:
        all_tokens.add(token)

# assign an ID to each token
token_to_id = {token: idx for idx, token in enumerate(sorted(all_tokens))}
id_to_token = {idx: token for token, idx in token_to_id.items()}

print(f"\nFinal vocab size: {len(token_to_id)}")

#Save vocab ────────────────────────────────────────────
with open(r"F:\RandomProjects\tewtoken\data\vocab.json", "w", encoding="utf-8") as f:
    json.dump(token_to_id, f, ensure_ascii=False, indent=2)

print("Saved vocab.json")

#Save merges ───────────────────────────────────────────
with open(r"F:\RandomProjects\tewtoken\data\merges.txt", "w", encoding="utf-8") as f:
    for pair in merges:
        f.write(f"{pair[0]} {pair[1]}\n")

print("Saved merges.txt")
print("\nDone! These two files ARE your tokenizer.")
