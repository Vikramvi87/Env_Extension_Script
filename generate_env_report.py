import os
import subprocess

def get_env_extensions(folder_path):
    """Scans for files containing '.env' and extracts the string after the last dot."""
    extensions = set()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if '.env' in file.lower():
                ext = file.split('.')[-1]
                if ext:
                    extensions.add(ext)
    return extensions

def main():
    target_directory = input("Enter the source code folder path to scan: ").strip()
    
    if target_directory.startswith('"') and target_directory.endswith('"'):
        target_directory = target_directory[1:-1]
        
    if not os.path.isdir(target_directory):
        print("Invalid directory path. Exiting.")
        return

    # 1. Scan for files containing .env
    exts = sorted(list(get_env_extensions(target_directory)))
    
    if not exts:
        print("No .env related files found in the specified directory. Exiting.")
        return

    # 2. Build the exact text format shown in the image
    ext_list_comma = ', '.join(exts)
    ext_list_quotes = '", "'.join(exts)
    
    xml_lines = []
    for ext in exts:
        xml_lines.append(f'        <FileExtension assess="true" exclude="false" extension="{ext}" web="false"/>')
    xml_block = "\n".join(xml_lines)
    
    report_content = f"""Found extensions in {target_directory} and its subfolders:
{ext_list_comma}

In C:\\programdata\\hcl\\appscanSource\\ltd\\file_extension.xml added "{ext_list_quotes}"


{xml_block}
"""

    output_file = os.path.join(target_directory, "appscan_extension_entry.txt")
    
    # 3. Write to the text file
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(report_content)
    except PermissionError:
        print(f"Permission denied: Cannot write to {target_directory}. Check folder permissions.")
        return

    print(f"\nSuccess! Notepad file generated at:\n{output_file}")

    # 4. Open the file in Notepad
    try:
        os.startfile(output_file)
    except AttributeError:
        subprocess.run(['notepad.exe', output_file])

if __name__ == "__main__":
    main()