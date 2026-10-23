# AppScan Environment File Extension Discovery

A custom Python utility designed to automate the discovery of environment (`.env`) file extensions for AppScan configurations. 

While manual configuration is typically recommended for handling `.env` file extensions in AppScan, this script is provided as a supplementary tool to help streamline your workflow, save time, and ease the configuration process.

## ⚠️ Important Disclaimer
**Please note:** This script is entirely optional and is provided "as-is" as a personal courtesy to increase convenience. It is **not** an official part of the AppScan product offerings and is not officially supported by the product team. Use it at your own discretion.

## Prerequisites
* Python 3.x installed on your system.
* Basic understanding of your project's directory structure and AppScan configuration.

## What This Script Does
* Automatically scans the specified target directory.
* Identifies files functioning as environment files.
* Extracts the relevant extensions to easily integrate them into your AppScan configuration settings.

## Usage

1. Clone this repository or download the script directly.
2. Open your terminal or command prompt.
3. Run the script using Python, passing your target directory as an argument (modify based on your script's specific parameters):

```bash
python [script_name.py] /path/to/your/project/directory
