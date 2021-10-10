from PIL import Image

# Test using a full essay
image = Image.open("/Users/rob/Downloads/starysquad-ground-truth-10-documents-summary/All_Data/Photo 3121.jpg")
width, height = image.size
# extract width and height from output tuple

print(width, height)

# Test using a sample snippet
image = Image.open("/Users/rob/GitHubProjects/scribble-stadium-ds/data/storysquad-ground-truth-51/5125/51-5125-1-0.png")

width, height = image.size
# extract width and height from output tuple

print(width, height)
