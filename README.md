# System Information Script

This script gathers various system information and saves it to JSON and TXT files. It retrieves data related to the operating system, CPU, memory, disk, GPU, network, environment variables, system paths, Python version, installed packages, running processes, hardware information, system events, and browser history.

## Prerequisites
- Python 3
- Required Python packages: `customtkinter`, `psutil`, `cpuinfo`, `GPUtil` (these will be installed by `requirements.txt`)

## Usage
1. Run the script using Python 3.
2. The script will generate JSON and TXT files in the `output` directory containing system information.

## Installation
1. Clone this repository:
    ```
    git clone https://github.com/samuel-lab/Data_getter.git
    ```
2. Navigate to the project directory:
    ```
    cd Data_getter
    ```
3. Install requirements:
    ```
    pip install -r requirements.txt
    ```
4. Run the main code:
    ```
    python3 Main.py
    ```

## ⚠ Warnings
- Running the script may gather sensitive information about your system. Make sure to review the code and understand what data is being collected before running it.
- Be cautious when sharing or storing the generated JSON and TXT files as they may contain sensitive system information.
- Some operations performed by the script may require elevated privileges, especially on certain operating systems. Make sure to run the script with appropriate permissions.

## Additional Notes
- This script imports various libraries such as `customtkinter`, `psutil`, `cpuinfo`, `GPUtil`, and others to gather system information.
- The gathered data includes information about the operating system, CPU, memory, disk, GPU, network, environment variables, system paths, Python version, installed packages, running processes, hardware information, system events, and browser history.
- The script saves the gathered information to both JSON and TXT files for further analysis or processing.

## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues if you encounter any problems or have suggestions for improvement.

## License
This project is licensed under the [MIT License](LICENSE).
