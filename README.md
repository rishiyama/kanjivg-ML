# kanjivg-ML
> [!NOTE]
> These tools are based on the [KanjiVG](https://github.com/KanjiVG/kanjivg) project.

This is an unofficial implementation to generate datasets for Machine learning experiments from the Kanjivg project.


## Overview

- **Source Data:** [KanjiVG](https://github.com/KanjiVG/kanjivg) (Kanji Vector Graphics)
- **Status:** Unofficial, for research/personal use.


## Setup
- python 3.10>=
- ubuntu 

**1. Clone the KanjiVG-ML repository:**
```bash
git clone https://github.com/rishiyama/kanjivg-ML
cd kanjivg-ML
```

**2. Clone the KanjiVG repository and initialize it:**
```bash
git clone https://github.com/KanjiVG/kanjivg.git
# fix kanjivg/__init__.py to import kanjivg
bash scripts/init.sh 
```

**3. Install any required dependencies:**

cairo:
```bash
pip install CairoSVG 
apt install libcairo2
```

> **Optional:**
>
>if you can get the output like this, then you are ready to use the kanjivg and kanjivg-ML package.
>```
>$ python example.py 
>Is 0x4E00 a kanji? True
>```

## Usage
**Generate a dataset:**
```bash
python run.py
```
and also, you can customize the parameters of png-images, such as width, height, and save directory by using the following command:

```bash
# same as default
python run.py --path ./kanjivg/kanji --width 256 --height 256 --save_dir ./output
```
<!--
## Prerequisites

- Python 3.x
- A local clone of the [KanjiVG repository](https://github.com/KanjiVG/kanjivg).

## Quick Start

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/rishiyama/kanjivg-ML.git
    cd kanjivg-ML
    ```

2.  **Clone the KanjiVG repository:**
    ```bash
    git clone https://github.com/KanjiVG/kanjivg.git
    cd kanjivg
    pip install -e .
    ```
 
3.  **Install dependencies:**
    ```bash
    # # pip install -r requirements.txt
    ```

4.  **Run the script:**
    ```bash
    # python generate_dataset.py --kanjivg_path ./kanjivg --output_path ./kanji_dataset.csv
    ``` -->


## Acknowledgments

This project is heavily reliant on the fantastic work done by the [KanjiVG project](https://github.com/KanjiVG/kanjivg).  