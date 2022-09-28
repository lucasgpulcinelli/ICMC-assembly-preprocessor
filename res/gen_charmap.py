#!/usr/bin/env python3
from PIL import Image, UnidentifiedImageError

CHAR_SIZE = 8
CHARS_COL = 32
CHARS_ROW = 32

STD_IMG_W = CHARS_COL * CHAR_SIZE
STD_IMG_H = CHARS_ROW * CHAR_SIZE

HEADER = f"""
-- File defining the character to pixel mapping

WIDTH={CHAR_SIZE};
DEPTH={CHARS_COL * CHARS_ROW * CHAR_SIZE};

ADDRESS_RADIX=UNS;
DATA_RADIX=BIN;

CONTENT BEGIN

"""

def generate_from_img(f_name):
    '''
    Main routine for the program's function flow, taking in a file name 
    corresponding to a 256x256 image as input (32x32 characters of 8x8 each)

    The standard dimensions can be customized via the constants above
    '''

    try:
        bit_img = Image.open(f_name)
    except FileNotFoundError as e:
        print(e)
        return 1
    except UnidentifiedImageError as e:
        print(f"The file {f_name} does not correspond to an image!")
        return 1
    
    img_h, img_w = bit_img.size

    if img_h < STD_IMG_W or img_w < STD_IMG_H:
        print(f"Image dimensions are too small (min {img_h}x{img_w})")
        return 1
    
    bit_img = bit_img.crop((0, 0, STD_IMG_W, STD_IMG_H))
    
    if bit_img.mode != '1':
        bit_img = bit_img.convert('1')
    
    full_matrix = []

    last_distinct_line = -1
    last_line_bits = 'xxxxxxxx'

    for char_y in range(CHARS_ROW):
        full_matrix.append([])

        for char_x in range(CHARS_COL):
            full_matrix[-1].append("")

            for bit_y in range(8):
                line_bits = ""

                py = char_y * 8 + bit_y
                
                line_n = char_y * CHARS_COL * 8 + char_x * 8 + bit_y

                for bit_x in range(8):
                    px = char_x * 8 + bit_x
                    line_bits += str(bit_img.getpixel((px, py)) // 255)
                
                distinct = last_line_bits != line_bits

                if distinct:
                    if last_distinct_line != -1:
                        if last_distinct_line == line_n - 1:
                            full_matrix[-1][-1] += (
                                f"\t{line_n - 1}  :   {last_line_bits}\n")
                        
                        else:
                            c_range = f"[{last_distinct_line}..{line_n-1}]"
                            full_matrix[-1][-1] += (
                                f"\t{c_range}  :   {last_line_bits}\n")
                    
                    last_line_bits = line_bits
                    last_distinct_line = line_n
                
                if bit_y == 7:
                    if distinct:
                        full_matrix[-1][-1] += (
                            f"\t{line_n}  :   {last_line_bits}\n")

                    else:
                        c_range = f"[{last_distinct_line}..{line_n}]"
                        full_matrix[-1][-1] += (
                            f"\t{c_range}  :   {last_line_bits}\n")
                    
                    last_distinct_line = -1
                    last_line_bits = 'xxxxxxxx'
    
    full_matrix = "\n".join(["\n".join(row) for row in full_matrix])

    with open('res/charmap.mif', 'w') as f:
        f.write(HEADER + full_matrix + "\nEND")
    
    return 0


if __name__ == '__main__':
    f_name = input("File name for the image to use for charmap generation: ")

    error_code = generate_from_img(f_name)

    if error_code:
        quit()
    
    print(f"Saved a charmap with {CHARS_COL * CHARS_ROW} characters")