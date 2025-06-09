import xml
import xml.etree.ElementTree as etree

import numpy as np
from natsort import natsorted
import pathlib 

from copy import deepcopy
from cairosvg import svg2png
from PIL import Image
import tqdm
import json

from kanjivg.utils import *
from kanjivg.kanjivg import SVGHandler, isKanji
from kanjivg_ml.check import isGeneralKanji, getGenralKanjiRange


def path_to_simple_svg(path_data:list, attr:dict, style:str, filename:str):
        
    assert len(path_data) > 0
    
    svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{attr["width"]}" height="{attr["height"]}" viewBox="{attr["viewBox"]}">\n'
    
    # assert style == "fill:none;stroke:#000000;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;"
    for path in path_data:
        svg_content += f'<path d="{path}" style="{style}" />\n'
    svg_content += '</svg>'
    
    with open(filename, "w") as file:
        file.write(svg_content)
    
    return svg_content
    
def path_to_svg(path_data:list, attr:dict, style:str, dirname:str, key:str, prefix:str):
    
    path = pathlib.Path(dirname)
    
    os.makedirs(path , exist_ok=True)
    path = path / key
    os.makedirs(path , exist_ok=True)
    path = path / f'{prefix}.svg'
        
    remake_svg = path_to_simple_svg(path_data, attr, style, path)
    return remake_svg, path

def convert_to_white_background(input_file, output_file):
    with Image.open(input_file) as img:
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            white_bg = Image.new("RGB", img.size, "white")
            white_bg.paste(img, mask=img.getchannel("A"))
            white_bg.save(output_file)

def make_dirs_recursive(path: pathlib.Path):
    for p in path.parents:
        if p.exists():
            break
        os.makedirs(p, exist_ok=True)

def set_prefix(index:int):
    initial = "0000" * 10
    l_linitial = list(initial)
    if index != 0:
        l_linitial[-index] = "1"
    res = "".join(l_linitial)
    
    return res
    
def parse_kanji_svg(filename, width, height, save_dir='./output'):
    save_dir = pathlib.Path(save_dir)


    handler = SVGHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    
    root = etree.parse(filename).getroot()
    attr = root.attrib
    
    styles = [
        element.attrib['style']
        for element in root.findall(".//*[@id]")
        if "kvg:StrokePaths" in element.attrib['id'] and 'style' in element.attrib
    ]
    style = styles[0]
    
    with open(filename, "r", encoding="utf-8") as svg_file:
        parser.parse(svg_file)
    
    keys = list(handler.kanjis.keys())
    assert len(keys) == 1
    key = keys[0]
    
    # kanji_flg = isKanji(int(key, 16))
    kanji_flg = isGeneralKanji(int(key, 16))
    
    
    kanji_data = handler.kanjis[key]
    stroke_list = kanji_data.getStrokes()
    
    path_data = []
    
    for s in stroke_list:
        path_data.append(s.svg)
 
    for i in range(len(path_data) + 1):
        sub_path_data = deepcopy(path_data)

        if i > 0:
            break
        
        save_dir_child = 'other'
        if kanji_flg:
            save_dir_child = 'kanji'
        
        path = save_dir / save_dir_child / 'svg'
        path_png = save_dir / save_dir_child / 'png'
        path_png_w = save_dir / save_dir_child / 'png_white'
        
        # prefix = set_prefix(int(i)) 
        prefix = key
        key = ''
        remake_svg, out_path = path_to_svg(sub_path_data, attr, style, path, key, prefix)
        path_png_ = path_png / out_path.relative_to(path).with_suffix(".png")
        path_png_w_ = path_png_w / out_path.relative_to(path).with_suffix(".png")
        
        make_dirs_recursive(path_png_)
        make_dirs_recursive(path_png_w_)
        
        assert attr["width"] == attr["height"] == str(109)
        
        # w, h = 224, 224
        w, h = width, height
        svg2png(url=str(out_path), write_to=str(path_png_), output_width=w, output_height=h)
        convert_to_white_background(path_png_, path_png_w_)
        
    return remake_svg, path_data, attr, kanji_flg

def args_parser():
    import argparse
    parser = argparse.ArgumentParser(description="Kanji SVG Parser")
    parser.add_argument('--path', type=str, default='./kanjivg/kanji', help='Path to the kanji SVG files')
    parser.add_argument('--width', type=int, default=256, help='Width of the output images')
    parser.add_argument('--height', type=int, default=256, help='Height of the output images')
    parser.add_argument('--save_dir', type=str, default='./output', help='Directory to save the output files')
    return parser.parse_args()

def main(path, width, height, save_dir):

    l = listSvgFiles(path)
    l = natsorted(l, key=lambda x: x.path)
    print("-> number of files: ", len(l))
    
    # width, height = 256, 256
    # width, height = 16, 16

    for k in tqdm.tqdm(l, desc="Processing SVG files", unit="file"):
        attr_svg, path_data, attr, kanji_flg = parse_kanji_svg(k.path, width, height, save_dir)
        
    
    start, end = getGenralKanjiRange()
    # save config
    config = {
        "width": width,
        "height": height,
        "isGeneralKanji": {
            "start": start,
            "end": end,
        }
    }

    # save as json
    
    with open(save_dir + '/config.json', 'w') as f:
        json.dump(config, f, indent=4)


if __name__ == '__main__':
    arg = args_parser()    
    path = arg.path
    width = arg.width
    height = arg.height
    save_dir = arg.save_dir

    main(path, width, height, save_dir)