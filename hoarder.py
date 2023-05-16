import os
import time
import requests
import subprocess
import zipfile

url = "https://github.com/muteb/Hoarder/releases/download/4.0.0/hoarder.exe"
file_path = "./hoarder.exe"
zip_file_pattern = f"{os.environ['COMPUTERNAME']}.zip"

# Download hoarder.exe
print("Downloading hoarder.exe...")
response = requests.get(url, stream=True)
with open(file_path, "wb") as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
print("Download complete!")

# Execute hoarder.exe with PowerShell as administrator
powershell_command = f"Start-Process -FilePath .\\hoarder.exe -ArgumentList '-a' -Verb RunAs"
process = subprocess.Popen(["powershell", "-Command", powershell_command])

# Wait for hoarder.exe process to finish
print("Running hoarder.exe...")
process.wait()
print("hoarder.exe finished running!")

# Check if the zip file is generated and ready
print("Generating zip file...")
while True:
    zip_file = next((filename for filename in os.listdir(".") if filename.endswith(zip_file_pattern)), None)
    if zip_file:
        try:
            with zipfile.ZipFile(zip_file) as zip_obj:
                zip_test = zip_obj.testzip()
                if zip_test is None:
                    print(f"Success, the zip file is ready: {zip_file}")
                    break
        except zipfile.BadZipFile:
            pass

    time.sleep(1)
