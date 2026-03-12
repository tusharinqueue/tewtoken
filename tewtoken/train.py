import re
import os

#function for cleaning transcripts
def clean_transcript(text):
    text = re.sub(r'\[.*?\]', '', text)     # remove [Music], [Applause] etc.
    text = re.sub(r'\s+', ' ', text)         # normalize whitespace
    text = text.strip()
    return text

#making filepath variables for easier access
raw_dir = r"F:\RandomProjects/tewtoken\data/raw"
corpus_file = r"F:\RandomProjects/tewtoken\data\corpus.txt"

#real processing
with open(corpus_file, "w", encoding="utf-8") as out: #opened corpus file as out
    for filename in sorted(os.listdir(raw_dir)): #iterating in raw dir
        if filename.endswith(".txt"): #checking if file ends with .txt
            filepath = os.path.join(raw_dir, filename) #makes a path variable that joins raw dir path with .txt file path so we can operate on that .txt file
            with open(filepath, "r", encoding="utf-8") as f: #opened filepath i.e. .txt file
                text = f.read()
            cleaned = clean_transcript(text)  #used our cleaned function on txt file
            if cleaned:
                out.write(cleaned + "\n")  # we now add output(cleaned text into corpus file (out)) | one video = one line

print("Corpus saved to", corpus_file)

with open(r"F:\RandomProjects\tewtoken\data\corpus.txt", "r" , encoding="utf-8") as f:
    lines = f.readlines()

#just stats
print(f"Total videos: {len(lines)}")
print(f"Total characters: {sum(len(l) for l in lines)}")
print(f"Sample: {lines[0][:200]}")
