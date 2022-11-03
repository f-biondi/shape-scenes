import pandas as pd
import requests
import glob
from PIL import Image
import datasets
import copy
from random import shuffle

features = datasets.Features({
    'image': datasets.Image(decode=True),
    'text': datasets.Value(dtype='string'),
})

text = []
image = []

files = glob.glob("./resized/*")
shuffle(files)
for i,n in enumerate(files):
    print(i)
    for i in range(4):
        fn = n.split("/")[-1].split(".")[0]
        f = open(f"./prompts2/{fn}_{i}.txt", "r")
        t = f.read()
        print(t)
        text.append(t)
        img = Image.open(n)
        image.append(features["image"].encode_example(copy.deepcopy(Image.open(n))))
        img.close()
        f.close()

print("done")
df = pd.DataFrame({"image": image,"text": text})
dataset = datasets.Dataset.from_pandas(df, features=features)
dataset.push_to_hub("f-biondi/shape-scenes-medium-2")
