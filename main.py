import subprocess
import shlex
import os

def get_user_input(prompt):
    return input(prompt)

def create_temp_directory():
    temp_dir = os.path.join(os.getcwd(), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def split_pdf(file_path, temp_dir):
    split_command = f'pdftk {file_path} burst output {temp_dir}/page_%02d.pdf'
    subprocess.call(shlex.split(split_command))

def rename_pages(temp_dir):
    for file in os.listdir(temp_dir):
        if file.startswith('page_'):
            page_num = file.split('_')[1].split('.')[0]
            if int(page_num) < 10:
                new_name = f'page_{page_num[1]}.pdf'
                os.rename(os.path.join(temp_dir, file), os.path.join(temp_dir, new_name))

def convert_to_grayscale(temp_dir, pages):
    for page in pages:
        input_file = os.path.join(temp_dir, f'page_{page}.pdf')
        output_file = os.path.join(temp_dir, f'op_{page}.pdf')
        gs_command = f'gs -sOutputFile={output_file} -sDEVICE=pdfwrite -sColorConversionStrategy=Gray -dProcessColorModel=/DeviceGray -dAutoRotatePages=/None -dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH {input_file}'
        subprocess.call(shlex.split(gs_command))

def rename_grayscale_pages(temp_dir):
    for file in os.listdir(temp_dir):
        if file.startswith('op_'):
            page_num = file.split('_')[1]
            new_name = f'page_{page_num}'
            os.rename(os.path.join(temp_dir, file), os.path.join(temp_dir, new_name))

def merge_pages(temp_dir, output_file):
    pages = sorted([f for f in os.listdir(temp_dir) if f.startswith('page_')])
    merge_command = f'pdftk {" ".join([os.path.join(temp_dir, page) for page in pages])} cat output {output_file}'
    subprocess.call(shlex.split(merge_command))

def main():
    file_path = get_user_input("Enter the file name: ")
    pages = list(map(int, get_user_input("Enter the page numbers. to be printed in grayscale separated by spaces: ").split()))

    temp_dir = create_temp_directory()
    split_pdf(file_path, temp_dir)
    rename_pages(temp_dir)
    convert_to_grayscale(temp_dir, pages)
    rename_grayscale_pages(temp_dir)

    output_file = os.path.join(os.getcwd(), 'new.pdf')
    merge_pages(temp_dir, output_file)

    flatten_command = f'pdftk {output_file} output output.pdf flatten'
    subprocess.call(shlex.split(flatten_command))

    os.remove(output_file)
    os.rmdir(temp_dir)

if __name__ == "__main__":
    main()
