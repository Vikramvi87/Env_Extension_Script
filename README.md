# Automated HCL AppScan `.env` Extension Configurator

This repository contains a Python utility script designed to automate the discovery and configuration of environment (`.env`) file extensions for HCL AppScan Source. 

As per the standard HCL AppScan product design, defining the scanning scope for custom `.env` file variants (e.g., `.env.SIT`, `ee.env.uat.prod`) requires manual updates to configuration files. This script eliminates that manual effort by automatically scanning your source code, extracting unique extensions, and securely updating the necessary XML configurations.

## 🌟 Features

* **Automated Discovery:** Recursively scans your source code directories to find all `.env` related files and extracts the unique environment tags (e.g., `SIT`, `prod`, `txt`).
* **Secure Backups:** Automatically creates a timestamped backup of your AppScan XML configuration files (e.g., `file_extensions_backup_20261026_203000.xml`) before making any modifications, ensuring a safe rollback path.
* **Idempotent Updates (Unique Check):** Verifies existing configurations to prevent duplicate XML entries. It only adds extensions that are missing from the `<FileExtensionSet name="iac">` node.
* **Audit Logging:** Generates a detailed operational log (`appscan_extension_update_log.txt`) in the scanned directory and automatically opens it in Notepad for immediate review.

## ⚙️ Target Configuration Files

The script automatically locates and updates the following HCL AppScan configuration files:
1. `C:\ProgramData\HCL\AppScanSource\ltd\file_extensions.xml` (auto-detects singular `file_extension.xml` as well)
2. `C:\Program Files\HCL\AppScanSource\engine\config\file_extensions.xml`

## 📋 Prerequisites

* **Operating System:** Windows (due to hardcoded AppScan installation paths).
* **Python:** Python 3.x installed on your machine.
* **Permissions:** **Administrator privileges** are required to modify files in the `C:\Program Files` and `C:\ProgramData` directories.

## 🚀 How to Run

1. Clone this repository or download the `update_appscan.py` script.
2. Open your Windows Command Prompt **as Administrator**.
   *(Right-click Start > Command Prompt (Admin) OR search `cmd`, right-click, and select "Run as administrator")*
3. Navigate to the directory where you saved the script:
   ```cmd
   cd path\to\script\directory
   ```
4. Execute the script:
   ```cmd
   python update_appscan.py
   ```
5. When prompted, paste the full path to the source code folder you want to scan and press **Enter**.

## 📄 Logs and Output

Once the script finishes executing, it will automatically open a file named `appscan_extension_update_log.txt`. This audit log contains:
* The exact directories scanned.
* A list of all unique `.env` extensions discovered.
* Status of the automated backups (success/failure with file paths).
* A line-by-line status of which extensions were newly added and which were skipped to prevent duplicates.

## 🛠️ Workflow Diagram

*(Note: Add your workflow diagram image to the repository and update the image path below)*

![Workflow Diagram](path/to/your/diagram.png)

---
**Disclaimer:** This is a custom automation utility provided to assist with configuration management and is not an official HCL product offering.
