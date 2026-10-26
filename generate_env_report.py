import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime

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

def backup_file(file_path, log_lines):
    """Creates a timestamped backup of the target file before any modifications."""
    if not os.path.exists(file_path):
        log_lines.append(f"[-] Target file not found, skipping backup: {file_path}")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_name = os.path.dirname(file_path)
    base_name, ext = os.path.splitext(os.path.basename(file_path))
    backup_path = os.path.join(dir_name, f"{base_name}_backup_{timestamp}{ext}")
    
    try:
        shutil.copy2(file_path, backup_path)
        log_lines.append(f"[+] Backup successfully created: {backup_path}")
        return True
    except PermissionError:
        log_lines.append(f"[-] Permission denied creating backup for: {file_path}. Please run as Administrator.")
        return False
    except Exception as e:
        log_lines.append(f"[-] Failed to create backup for {file_path}. Error: {str(e)}")
        return False

def update_xml_file(file_path, new_extensions, log_lines):
    """Safely updates the XML file with unique extensions and correct 4-space line breaks."""
    if not backup_file(file_path, log_lines):
        log_lines.append(f"[-] Aborting updates for {file_path} due to backup failure.")
        return False

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Target the specific 'iac' node
        iac_set = root.find(".//FileExtensionSet[@name='iac']")
        
        if iac_set is None:
            log_lines.append(f"[-] Error: Could not find <FileExtensionSet name='iac'> in {file_path}")
            return False
            
        changes_made = False
        
        for ext in new_extensions:
            existing = iac_set.find(f"FileExtension[@extension='{ext}']")
            
            if existing is None:
                # Format fix: Correctly align with 4 spaces and preserve the closing tag
                if len(iac_set) > 0:
                    closing_tail = iac_set[-1].tail
                    iac_set[-1].tail = "\n    "
                else:
                    closing_tail = "\n"
                    iac_set.text = "\n    "
                
                # Add the new unique extension safely
                new_elem = ET.SubElement(iac_set, "FileExtension", {
                    "extension": ext,
                    "assess": "true",
                    "web": "false"
                })
                
                new_elem.tail = closing_tail
                
                log_lines.append(f"    [+] Successfully added new extension '{ext}'")
                changes_made = True
            else:
                log_lines.append(f"    [*] Extension '{ext}' already exists. Skipped to maintain unique entries.")
                
        if changes_made:
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
            log_lines.append(f"[+] Successfully wrote formatted updates to XML file: {file_path}")
            return True
        else:
            log_lines.append(f"[*] No new updates were required for {file_path}. File remains unchanged.")
            return False
            
    except ET.ParseError:
        log_lines.append(f"[-] Error: The file {file_path} is corrupted or not a valid XML format.")
        return False
    except PermissionError:
        log_lines.append(f"[-] Permission denied writing to {file_path}. Please run Command Prompt as Administrator.")
        return False
    except Exception as e:
        log_lines.append(f"[-] Unexpected error updating {file_path}: {str(e)}")
        return False

def main():
    # Auto-detect whether the file in ProgramData is singular or plural
    ltd_path = r"C:\ProgramData\HCL\AppScanSource\ltd\file_extension.xml"
    if not os.path.exists(ltd_path):
        ltd_path = r"C:\ProgramData\HCL\AppScanSource\ltd\file_extensions.xml"

    # Target configurations to update securely
    target_xml_files = [
        ltd_path,
        r"C:\Program Files\HCL\AppScanSource\engine\config\file_extensions.xml"
    ]
    
    target_directory = input("Enter the source code folder path to scan: ").strip()
    if target_directory.startswith('"') and target_directory.endswith('"'):
        target_directory = target_directory[1:-1]
        
    if not os.path.isdir(target_directory):
        print("Invalid directory path. Exiting.")
        return

    # Initialize execution logging
    log_lines = []
    log_lines.append(f"AppScan Extension Update Execution Log")
    log_lines.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append(f"Target Scan Directory: {target_directory}")
    log_lines.append("-" * 70)

    # 1. Scan for unique .env extensions
    exts = sorted(list(get_env_extensions(target_directory)))
    
    if not exts:
        log_lines.append("No .env related files found in the specified directory.")
        print("No .env related files found. Exiting.")
        return
        
    log_lines.append(f"Found {len(exts)} unique extensions to process: {', '.join(exts)}")
    
    # 2. Iterate through both AppScan XML files and update them
    for xml_file in target_xml_files:
        log_lines.append("\n" + "=" * 70)
        if not os.path.exists(xml_file):
            log_lines.append(f"[-] File not found: {xml_file}")
        else:
            log_lines.append(f"Processing File: {xml_file}")
            log_lines.append("=" * 70)
            update_xml_file(xml_file, exts, log_lines)
        
    log_lines.append("\n" + "=" * 70)
    log_lines.append("Execution Complete. Please review the logs above for any skipped items or permission errors.")
    
    # 3. Write comprehensive logs to a notepad file
    report_content = "\n".join(log_lines)
    output_file = os.path.join(target_directory, "appscan_extension_update_log.txt")
    
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(report_content)
    except PermissionError:
        print(f"Permission denied: Cannot write log to {target_directory}. Check folder permissions.")
        return

    print(f"\nExecution finished! A detailed operational log has been generated at:\n{output_file}")

    # 4. Automatically open the audit log in Notepad for review
    try:
        os.startfile(output_file)
    except AttributeError:
        subprocess.run(['notepad.exe', output_file])

if __name__ == "__main__":
    main()
