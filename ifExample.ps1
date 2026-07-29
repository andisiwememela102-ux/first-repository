# Check if new_folder exists
# If exists, create if_folder
if (Test-Path "new_folder") {
    New-Item -ItemType Directory -Name "if_folder" -Force
}

# Check if if_folder exists
# If it exists, create hyperionDev
# Or else, create new-projects
if (Test-Path "if_folder") {
    New-Item -ItemType Directory -Name "hyperionDev" -Force
} else {
    New-Item -ItemType Directory -Name "new-project" -Force
}