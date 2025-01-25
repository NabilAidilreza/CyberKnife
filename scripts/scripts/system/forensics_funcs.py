import os
import scripts.system.log_format as lf
from rich.table import Table
from PIL.ExifTags import TAGS
from scripts.system.general_funcs import *


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
    lf.warning("Open file in HexEdit for better viewing.\n")

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

# def run_binwalk(file_names,target_folder):
#     target_file_name = multi_prompt(file_names,"Choose File")
#     file_path = os.path.join(target_folder, target_file_name)
#     for module in binwalk.scan(file_path, signature=True, quiet=True):
#         for result in module.results:
#             lf.dataout(f"Offset: {result.offset}, Description: {result.description}")