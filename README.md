# 🔤 BPE Tokeniser

A **Byte Pair Encoding (BPE) tokeniser built from scratch in pure Python** — no HuggingFace, no PyTorch, no magic. Trained on real YouTube transcripts in **English + Hindi**, making it one of the few open-source bilingual BPE tokenisers built entirely from the ground up.

> Built as a learning project to deeply understand how tokenisation works under the hood in LLMs like GPT, LLaMA, and Gemini.

---

## 📸 Demo

<!-- Add a screenshot or GIF of the CLI demo here -->
> _Screenshot coming soon_

---

## ✨ Features

- ✅ Built from scratch — zero ML libraries used
- ✅ Bilingual — trained on English + Hindi text
- ✅ 8,000 BPE merge rules learned from real YouTube transcripts
- ✅ Vocabulary of ~7,900 tokens
- ✅ Importable as a Python package
- ✅ 13 utility functions (encode, decode, batch, truncate and more)
- ✅ Interactive CLI demo

---

## 📦 Installation

**Option 1 — Install directly from GitHub (recommended):**
```bash
pip install git+https://github.com/yourusername/tokeniser-project.git
```

**Option 2 — Clone and use locally:**
```bash
git clone https://github.com/yourusername/tokeniser-project.git
cd tewtoken-project
```

---

## 🚀 Quick Start

```python
from tewtoken import encode, decode, tokenize, count_tokens

# Encode text to token IDs
ids = encode("machine learning is amazing")
print(ids)
# → [2839, 2700, 2506, 368]

# Decode back to text
text = decode(ids)
print(text)
# → "machine learning is amazing"

# See the actual token strings
tokens = tokenize("machine learning is amazing")
print(tokens)
# → ['machine</w>', 'learning</w>', 'is</w>', 'amazing</w>']

# Count tokens
print(count_tokens("machine learning is amazing"))
# → 4
```

---

## 🌐 Bilingual Support (English + Hindi)

```python
from tewtoken import encode, decode

# Hindi works too!
ids = encode("यह एक परीक्षण है")
print(decode(ids))
# → "यह एक परीक्षण है"
```

<!-- Add a screenshot showing Hindi tokenisation here -->
> _Screenshot coming soon_

---

## 📚 Full API Reference

| Function | Description |
|----------|-------------|
| `encode(text)` | Convert text → list of token IDs |
| `decode(ids)` | Convert token IDs → text |
| `tokenize(text)` | Convert text → list of token strings |
| `count_tokens(text)` | Count number of tokens in text |
| `encode_batch(texts)` | Encode a list of texts at once |
| `decode_batch(ids_list)` | Decode a list of token ID lists at once |
| `truncate(text, max_tokens)` | Truncate text to a max token count |
| `vocab_size()` | Returns total vocabulary size |
| `get_vocab()` | Returns full vocabulary as dict |
| `get_token_id(token)` | Get ID for a single token string |
| `get_id_token(id)` | Get token string for a single ID |
| `is_known_token(token)` | Check if a token exists in vocabulary |
| `encoding_info()` | Returns a summary of the tokeniser |

---

## 🧠 How BPE Works

BPE starts with individual characters and iteratively merges the most frequent adjacent pairs:

```
Step 0 (characters):  ['m', 'a', 'c', 'h', 'i', 'n', 'e', '</w>']
Step 1 (merge t+h):   ['t', 'h'] → 'th'
Step 2 (merge th+e):  ['th', 'e'] → 'the'
...
Step N:               'machine' is now a single token
```

After 8,000 merges, common words become single tokens and rare words are split into meaningful subwords. This is the exact same algorithm used by GPT-2, LLaMA, and most modern LLMs.

---

## 📁 Project Structure

```
tokeniser-project/
├── data/
│   ├── raw/              ← raw YouTube transcripts (.txt)
│   ├── corpus.txt        ← cleaned + merged training corpus
│   ├── vocab.json        ← learned vocabulary {token: id}
│   └── merges.txt        ← 8,000 BPE merge rules
├── tokeniser/
│   ├── __init__.py       ← package exports
│   ├── train.py          ← cleans + builds corpus
│   ├── vocab.py          ← character vocab + word frequencies
│   ├── bpe.py            ← BPE training loop
│   └── tokeniser.py      ← encode / decode + all utility functions
├── demo/
│   └── main.py           ← interactive CLI demo
├── setup.py
├── LICENSE
└── README.md
```

---

## 🏃 Run the Demo

```bash
python demo/main.py
```

<!-- Add a screenshot of the CLI demo output here -->
> _Screenshot coming soon_

---

## 📊 Training Details

| Property | Value |
|----------|-------|
| Training data | YouTube transcripts |
| Languages | English + Hindi |
| Total transcripts | ~100 videos |
| BPE merges | 8,000 |
| Final vocab size | ~7,900 tokens |
| Training time | ~320s (pure Python) |
| Library dependencies | None (stdlib only) |

---

## 🔍 Interesting Observations

- By merge **#3**, `t + h → 'th'` was learned
- By merge **#17**, `'the'` became a single token
- By merge **#101**, the Hindi virama `स + ् → 'स्'` was learned — BPE correctly identified the most frequent Hindi character combination
- Common English words like `you`, `the`, `is`, `and` all became single tokens early
- Hindi subwords like `है`, `तो`, `में` emerged naturally from frequency

---

## ⚡ Why is it slow?

Pure Python BPE takes ~320 seconds for 8,000 merges. Production tokenisers like HuggingFace `tokenizers` (Rust) or Google `SentencePiece` (C++) do it in ~2 seconds. The algorithm is identical — the difference is the language. This is intentional: the goal of this project is understanding, not speed.

---

## 🗺️ Roadmap

- [ ] Add Streamlit web demo
- [ ] Expand corpus (Wikipedia dump for English + Hindi)
- [ ] Scale to 30k+ merges with larger dataset
- [ ] Add special tokens (`[PAD]`, `[UNK]`, `[BOS]`, `[EOS]`)
- [ ] Publish blog post walkthrough

---

## 📝 Blog Post

<!-- Add link to your blog post here once published -->
> _Blog post coming soon_

---

## 🪪 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙋 Author

**Tushar** — BTech CSE (AI/ML) student building in public.

[![GitHub](https://img.shields.io/badge/GitHub-tusharinqueue-black?logo=github)](https://github.com/tusharinqueue)
[![Twitter](https://img.shields.io/badge/Twitter-@tusharinqueue-blue?logo=twitter)](https://twitter.com/tusharinqueue)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-tusharinqueue-blue?logo=linkedin)](https://linkedin.com/in/tusharinqueue)
