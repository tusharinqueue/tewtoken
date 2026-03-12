from setuptools import setup, find_packages

setup(
    name="tewtoken",
    version="1.0",
    author="Tushar Singla",
    description="A bilingual BPE tokenizer trained on English + Hindi transcripts",
    packages=find_packages(),
    package_data={
        "tokenizer": [
            "../data/vocab.json",
            "../data/merges.txt",
        ]
    },
    python_requires=">=3.7",
)
