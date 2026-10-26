# AppScan Source .env Extension Configurator

An automated Python utility designed to discover and register environment (`.env`) file extensions for HCL AppScan Source. This script streamlines the configuration required to perform Infrastructure-as-Code (IaC) scanning on `.env` files by eliminating manual XML updates.

## 🚀 Features

* **Automated Discovery:** Scans target source code directories and nested subfolders to find all `.env` variations (e.g., `.env`, `.env.SIT`, `ee.env.uat.prod`).
* **Dynamic Extraction:** Isolates the unique environment tags (e.g., `SIT`, `prod`, `txt`) for accurate configuration.
* **Dual Configuration Update:** Simultaneously targets and updates the required `file_extensions.xml` files in both `C:\ProgramData\...` and `C:\Program Files\...`.
* **Idempotency (Safe Execution):** Checks existing `<FileExtension>` entries to prevent duplicate XML tags and maintain clean configuration files.
* **Pre-flight Backups:** Automatically generates timestamped backups of your XML files before making any modifications, ensuring a safe rollback path.
* **Comprehensive Audit Logging:** Creates a detailed execution log (`appscan_extension_update_log.txt`) outlining discovered files, backup statuses, and updated entries.

## 📋 Prerequisites

* **Python 3.x** installed on your Windows machine.
* **Administrator Privileges:** Required to modify configuration files located in system directories (`C:\ProgramData` and `C:\Program Files`).

## 🛠️ How to Run

1. Clone this repository or download the `update_appscan.py` script.
2. Open your Windows Command Prompt as **Administrator**. *(Right-click Start > Command Prompt (Admin) OR search `cmd`, right-click, and select "Run as administrator")*
3. Navigate to the directory where you saved the script:
   ```cmd
   cd path\to\script\directory
