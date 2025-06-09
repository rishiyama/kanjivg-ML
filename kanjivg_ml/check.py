
GEN_KANJI_START = 0x4E00
GEN_KANJI_END = 0x9FA5

def getGenralKanjiRange():
    return (GEN_KANJI_START, GEN_KANJI_END)
def isGeneralKanji(v):
	return (v >= GEN_KANJI_START and v <= GEN_KANJI_END)
    # return (v >= 0x4E00 and v <= 0x9FC3)
	# return (v >= 0x4E00 and v <= 0x9FC3) or (v >= 0x3400 and v <= 0x4DBF) or (v >= 0xF900 and v <= 0xFAD9) or (v >= 0x2E80 and v <= 0x2EFF) or (v >= 0x20000 and v <= 0x2A6DF)
