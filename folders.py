import requests
import re
import os

def clean(name): #Removes any characters that aren't allowed in a file name
    out = re.sub(r'[<>:"/\\|?*]', "", name)
    while out[-1] == "." or out[-1] == " ":
        out = out[:-1]
    return out
def strip(name): #Removes the " 3" in "Come Back 3" for example
    out = name
    while out[-1].isdigit() or out[-1] == " ":
        out = out[:-1]
    return clean(out)

#Storyline dictionary: {Name:Folder}
arc = {}
base = "https://sinfest.xyz/btphp/comics/"
year = "2000"
file = open('ComicList - Copy.txt', 'r')

line = file.readline().split('|')
while line[0] == "0": #gets to first comic
    line = file.readline().split('|')
folder = year + "/" + strip(line[3])
arc[strip(line[3])] = folder
keywords = re.split(r'[, ]+', line[5])
os.makedirs("Output/"+folder, exist_ok=True)
#Save comic to folder
date = line[0]+"-"+line[1]+"-"+line[2]
comic = requests.get(base+date+".gif")
with open("Output/"+folder+"/"+date+"_"+clean(line[3])+".gif", "wb") as f:
    f.write(comic.content)

#iterate through remaining lines
for i in range(9409):
    line = file.readline().split('|')
    if line[0] == "0": continue
    if strip(line[3]) in arc: #If the comic is in a numbered arc, it gets assigned to it
        folder = arc[strip(line[3])]
    elif set(re.split(r'[, ]+', line[5])).intersection(set(keywords)) and folder.count('-')<5:
        #Merges multiple arcs. To prevent file names from getting too long, a max of 5 arcs can be grouped
        folder0 = folder
        folder = folder0 + "-" + strip(line[3])
        os.rename("Output/"+folder0,"Output/"+folder)
        for name in folder[5:].split('-'):
            arc[name] = folder
    else: #Generates a new arc folder
        year = line[0]
        folder = year + "/" + strip(line[3])
        os.makedirs("Output/"+folder, exist_ok=True)
    keywords = re.split(r'[, ]+', line[5])
    # Save comic to folder
    date = line[0] + "-" + line[1] + "-" + line[2]
    comic = requests.get(base + date + ".gif")
    with open("Output/"+folder + "/" + date + "_" + clean(line[3]) + ".gif", "wb") as f:
        f.write(comic.content)
    print(date)

file.close()