from xml.sax import handler
import torch
import torch.nn as nn
from kanjivg_utils import *
# from kanjivg import SVGHandler, KanjisHandler, Kanji, isKanji, isGeneralKanji
from kanjivg import SVGHandler, isKanji, isGeneralKanji
import xml
import xml.etree.ElementTree as etree
from pydiffvg.parse_svg import svg_to_scene
from svgpathtools import svg2paths
from natsort import natsorted
import numpy as np
import pathlib 
from copy import deepcopy
from cairosvg import svg2png
from PIL import Image

def path_to_simple_svg(path_data:list, attr:dict, style:str, filename:str):
    
    
    # stroke_list = kanji_data.getStrokes()
    # path_data = []
    # for s in stroke_list:
    #     path_data.append(s.svg)
        
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
    
def parse_kanji_svg(filename):

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
            if len(sub_path_data) == 1:
                break
            else:
                sub_path_data.pop(i-1)
        
        if kanji_flg:
            path = pathlib.Path('/home/rish/scratch/lines/StrokeRemover/kanji_path/kanji/svg/')
            path_png = pathlib.Path('/home/rish/scratch/lines/StrokeRemover/kanji_path/kanji/png/')
            path_png_w = pathlib.Path('/home/rish/scratch/lines/StrokeRemover/kanji_path/kanji/png_white/')
        else:
            path = pathlib.Path('/home/rish/scratch/lines/StrokeRemover/kanji_path/other/svg/')
            path_png = pathlib.Path('/home/rish/scratch/lines/StrokeRemover/kanji_path/other/png/')
            path_png_w = pathlib.Path('/home/rish/scratch/lines/StrokeRemover/kanji_path/other/png_white/')
        
        
        prefix = set_prefix(int(i)) 
        remake_svg, out_path = path_to_svg(sub_path_data, attr, style, path, key, prefix)
        path_png_ = path_png / out_path.relative_to(path).with_suffix(".png")
        path_png_w_ = path_png_w / out_path.relative_to(path).with_suffix(".png")
        
        make_dirs_recursive(path_png_)
        make_dirs_recursive(path_png_w_)
        
        assert attr["width"] == attr["height"] == str(109)
        
        w, h = 224, 224
        svg2png(url=str(out_path), write_to=str(path_png_), output_width=w, output_height=h)
        convert_to_white_background(path_png_, path_png_w_)
        
    return remake_svg, path_data, attr, kanji_flg



def args_parser():
    import argparse
    parser = argparse.ArgumentParser(description="Kanji SVG Parser")
    parser.add_argument('--path', type=str, default='./kanjivg/kanji', help='Path to the kanji SVG files')
    return parser.parse_args()


def main():
    arg = args_parser()    
    path = arg.path

    l = listSvgFiles(path)
    l = natsorted(l, key=lambda x: x.path)
    print("-> number of files: ", len(l))
    
    all_path_data = []
    number_of_path = []
    for k in l:
        # print(k.path)
        attr_svg, path_data, attr, kanji_flg = parse_kanji_svg(k.path)
        
        if kanji_flg == False:
            continue
        
        all_path_data.append(path_data)
        number_of_path.append(len(path_data))
        # print(path_data)
        # print(k.id)
        
    number_of_path = np.array(number_of_path)
    print("-> number of path: ", number_of_path)
    np.save("number_of_path.npy", number_of_path)
    
if __name__ == '__main__':
    main()