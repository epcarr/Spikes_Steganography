import pathlib
import os

# Force us to be in the parent directory
if os.getcwd().endswith('tools'):
    os.chdir('..')
    
ALLOWED_EXTENSIONS = {'py', 'js', 'css', 'txt', 'json', 'csv', 'html', 'md'}
    
all_files = {}
for root, dirs, files in os.walk('website'):
    for file in files:
        path = pathlib.Path(os.path.join(root, file)).relative_to('website')
        if pathlib.Path(file).suffix[1:].lower() not in ALLOWED_EXTENSIONS:
            print("Skipping", os.path.join(root, file))
            continue
        with open(os.path.join(root, file), 'r') as f:
            content = f.read()
            all_files[str(path.as_posix())] = content
            print("Adding", os.path.join(root, file))
            
os.makedirs('tools/build', exist_ok=True)

with open('tools/build/website_files.js', 'w') as f:
    for filename, contents in all_files.items():
        f.write(f"Sk.builtinFiles.files[{filename!r}] = {contents!r};\n")

print("Bundled", len(all_files), "files into tools/build/website_files.js")
