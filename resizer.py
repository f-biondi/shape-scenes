import glob
from PIL import Image

for file in glob.glob('./screenshots/*'):
    print(file)
    image = Image.open(file)
    image.thumbnail((400,300), Image.ANTIALIAS)
    image.save(f"resized/{file.split('/')[len(file.split('/'))-1]}", "JPEG")
