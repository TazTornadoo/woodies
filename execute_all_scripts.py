import os


if os.path.isdir('database') is False:
    for file in os.listdir("Python"):
        if file[-2:] == "py" and file[0].isnumeric() == True:
            os.system(f"chmod +x {file}")
            os.system(f"python Python/{file}")
            
            