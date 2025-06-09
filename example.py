# from kanjivg.kanjivg import parse_kanji_svg, listSvgFiles
# from kanjivg import SVGHandler, isKanji, isGeneralKanji
from kanjivg import kanjivg, xmlhandler, utils

def main():
    check = kanjivg.isKanji(0x4E00)  # Example usage of the isGeneralKanji function
    print(f"Is 0x4E00 a kanji? {check}")

if __name__ == "__main__":
    main()