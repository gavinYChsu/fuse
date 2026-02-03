# Colab Linux Compilation Instructions

Use the following steps and code in a Google Colab notebook to compile `fuse` into a standalone Linux executable.

## Prerequisites

1.  Upload your project `fusion` folder to your Google Drive or zip it and upload it directly to the Colab session.
2.  If using Google Drive, mount it first.

## Compilation Script

Copy and paste the following code into a code cell in Google Colab and run it.

```python
import os
import shutil
import subprocess

# --- CONFIGURATION ---
# Path to your project folder in Colab
# If you uploaded a zip, unzip it first.
# Example: "/content/fusion/fuse"
PROJECT_DIR = "/content/fusion/fuse" 
# Name of the output executable
EXECUTABLE_NAME = "fuse_linux"
# Enable GPU support (adds size, requires CUDA on target)
USE_GPU = True
# ---------------------

def run_command(command):
    print(f"Running: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc

# 1. Install Dependencies
print("--- Installing Dependencies ---")
# Install build tools
run_command("pip install pyinstaller")
# Install project requirements
# Assuming requirements.txt is in the PROJECT_DIR
requirements_path = os.path.join(PROJECT_DIR, "requirements.txt")

# Install base requirements but handle onnxruntime specifically
if os.path.exists(requirements_path):
    run_command(f"pip install -r {requirements_path}")
    # Force uninstall onnxruntime if we want GPU, to ensure clean slate
    if USE_GPU:
        run_command("pip uninstall -y onnxruntime")
        run_command("pip install onnxruntime-gpu")
else:
    print(f"Warning: requirements.txt not found at {requirements_path}")
    # Fallback/Important deps
    onnx_pkg = "onnxruntime-gpu" if USE_GPU else "onnxruntime"
    run_command(f"pip install {onnx_pkg} onnx numpy opencv-python tqdm")

# 2. Run PyInstaller
print("\n--- Running PyInstaller ---")
os.chdir(PROJECT_DIR)

# Clean previous builds
if os.path.exists("build"): shutil.rmtree("build")
if os.path.exists("dist"): shutil.rmtree("dist")

# Build command
# --collect-all fuse: Collects all data and modules from the package
# --hidden-import onnxruntime: Explicitly include onnxruntime if needed
# --onefile: Create a single executable file
hidden_imports = "--hidden-import onnxruntime"
if USE_GPU:
    hidden_imports += " --hidden-import onnxruntime.providers.cuda"

pyinstaller_cmd = (
    f"pyinstaller --clean --noconfirm --onefile "
    f"--name {EXECUTABLE_NAME} "
    f"--collect-all fuse "
    f"{hidden_imports} "
    f"fuse.py"
)

exit_code = run_command(pyinstaller_cmd)

# 3. Verify and Package
if exit_code == 0:
    dist_path = os.path.join(PROJECT_DIR, "dist", EXECUTABLE_NAME)
    if os.path.exists(dist_path):
        print(f"\nSUCCESS: Executable created at: {dist_path}")
        print(f"File size: {os.path.getsize(dist_path) / (1024*1024):.2f} MB")
        
        # Optional: Zip it for easier download
        zip_path = os.path.join(PROJECT_DIR, f"{EXECUTABLE_NAME}.zip")
        # shutil.make_archive usage: base_name, format, root_dir, base_dir
        # We want to zip just the executable
        import zipfile
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(dist_path, arcname=EXECUTABLE_NAME)
        
        print(f"Zipped executable available at: {zip_path}")
        from google.colab import files
        files.download(zip_path)
    else:
        print("\nERROR: dist folder exists but executable not found.")
else:
    print("\nERROR: PyInstaller failed.")
```

## Manual Steps (if script fails)

1.  **Install**: `pip install pyinstaller -r requirements.txt`
2.  **Build**: `pyinstaller --onefile --collect-all fuse fuse.py`
3.  **Download**: Check the `dist/` folder.
