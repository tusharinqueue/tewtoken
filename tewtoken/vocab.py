import re
from collections import Counter

# Load corpus
with open(r"F:\RandomProjects\tewtoken\data\corpus.txt", "r", encoding="utf-8") as f:
    text = f.read().lower()

# Clean only the bad characters
text = text.replace('�', '')           # corrupted byte
text = re.sub(r'<[^>]+>', '', text)    # remove any <html> tags

# Step 1 — Character Vocabulary
#Why do we need this?
#BPE starts from individual characters and builds up. So before any merges happen, every unique character in your corpus is a token. This is our base vocabulary

chars = sorted(set(text))
char_to_id = {ch: idx for idx, ch in enumerate(chars)}
id_to_char = {idx: ch for idx, ch in enumerate(chars)}

#stats
print(f"Total unique characters: {len(chars)}")
print(f"Vocab: {chars}")

# Step 2 — Word Frequency Count
words = re.findall(r'\S+', text)       # split on whitespace, keep punctuation attached
word_freq = Counter(words)

#just a quality check
print(f"\nTotal unique words: {len(word_freq)}")
print(f"\nTop 20 most frequent words:")
for word, count in word_freq.most_common(100):
    print(f"  {word}: {count}")