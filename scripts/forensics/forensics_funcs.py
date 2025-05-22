import os
import scripts.system.log_format as lf
import webbrowser
from rich.table import Table
from PIL.ExifTags import TAGS
from PIL import Image
from scripts.system.general_funcs import *

from zlib import crc32
import struct

#* Forensics ###
def hex_reader(file_names,target_folder):
    target_file_name = multi_prompt(file_names,"Choose File")
    file_path = os.path.join(target_folder, target_file_name)
    data = read_from_file(file_path,"rb")

    hex_table = Table(title="")
    hex_table.add_column("Hex Dump",style="green",justify="left")
    hex_table.add_column("Content",style="blue",justify="center")

    def print_hex(data):
        bytes = 0
        line = []
        line_string = ""
        for b in data:
            bytes += 1
            line.append(b)
            line_string += "{0:0{1}x}".format(b,2) + " " 
            if bytes % 16 == 0:
                line_content = ""
                for b2 in line:
                    if (b2 >= 32) and (b2 <= 126):
                        line_content += chr(b2)
                    else:
                        line_content += "*"
                temp = [line_string,line_content]
                hex_table.add_row(*temp)
                line_string=""
                line=[]
        lf.print(hex_table)
    def preview_file(data):
        lf.processing("File Preview")
        print_hex(data[:500])
    preview_file(data)
    lf.warning("Open file in HexEdit for better viewing.")

def exif_tool(file_names,target_folder):
    target_file_name = multi_prompt(file_names,"Choose File")
    file_path = os.path.join(target_folder, target_file_name)
    if is_valid_image_pil(file_path):
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data:
            lf.processing("Retrieving EXIF Data...")
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                sleep(0.1)
                lf.print(f"{tag_name}: {value}")
            lf.warning("End of EXIF Data")
        else:
            lf.fatal("No EXIF Metadata!")
    else:
        lf.failure(f"{file_path} is NOT a valid image.")

def extract_text_from_image():
    webbrowser.open("https://www.imagetotext.info/")

def png_dimensions_bruteforcer(file_names,target_folder):
    target_file_name = multi_prompt(file_names,"Choose File")
    file_path = os.path.join(target_folder, target_file_name)

    MAX_WIDTH = 3200
    MAX_HEIGHT = 3200

    lf.progress('='*51)
    lf.warning('PNG Image Dimension Bruteforcer')
    lf.comment('Brute force the image dimensions of a PNG image.')
    lf.progress('='*51 + '\n')

    png = bytearray(open(file_path, 'rb').read())

    # Pull crc
    crcStart = 29
    crcTarget = (bytearray(png[crcStart:crcStart+4])).hex()
    crcFound = False
    lf.processing("Attempting values...")
    for width in range(MAX_WIDTH):
        for height in range(MAX_HEIGHT):

            png[0x10:0x14] = struct.pack(">I",width)
            png[0x14:0x18] = struct.pack(">I",height)

            calculatedCrc = crc32(png[12:29])
            if calculatedCrc == int(crcTarget, 16):
                crcFound = True
                lf.success('Found Correct Dimensions...\nWidth: {}\nHeight: {}'.format(width, height))
                lf.warning('Remember to pad this with leading 0\'s as required.')
                with open('fixed.png','wb') as file:
                    file.write(png)
                    lf.finalok('\nSuccessfully wrote to: fixed.png')
                break
        else:
            continue
        break

    if (not crcFound):
        lf.failure('Exhausted all dimensions up to (Width, Height): ({}, {})'.format(MAX_WIDTH, MAX_HEIGHT))








def handle_forensics(file_names, target_folder):
    choice = multi_prompt(["Hex Viewer", "EXIF Image", "Text Image Extract","PNG Dimensions Bruteforcer","Back"], "Options")
    if choice == "Hex Viewer":
        hex_reader(file_names, target_folder)
    elif choice == "EXIF Image":
        exif_tool(file_names, target_folder)
    elif choice == "Text Image Extract":
        extract_text_from_image()
    elif choice == "PNG Dimensions Bruteforcer":
        png_dimensions_bruteforcer(file_names, target_folder)
