@echo off
echo Opening Ubuntu app...
wsl.exe -d Ubuntu

echo Navigating to mnt directory...
wsl.exe -d Ubuntu bash -c "cd /mnt"

echo Done.