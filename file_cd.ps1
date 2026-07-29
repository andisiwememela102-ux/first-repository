# Create three new folders
New-item -ItemType Directory -Name "folder1" 
New-item -ItemType Directory -Name "folder2"
New-item -ItemType Directory -Name "folder3"

# Navigate into folder1
Set-Location -Path "folder1"

# Create three new folders inside folder1
New-item -ItemType Directory -Name "subFolder1"
New-item -ItemType Directory -Name "subFolder2"
New-item -ItemType Directory -Name "subFolder3"

# Remove two of the folders created
Remove-Item -Path "subfolder1"
Remove-Item -Path "subfolder2"