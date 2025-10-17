"""
The game plan:
1. Iterate through every year of the archive, scraping each date, and fetching the title & link
2. Assemble an array with links and titles
3. Search all titles in search bar, put the keywords in the array
4. Check if the title is in sequence with the previous one OR if it shares a keyword with the previous.
   If it does, assign it to the previous folder. If not, create a new one
5. Scrape the website for images and put them in the assigned folder.
"""

import numpy as np
from datetime import date
from bs4 import BeautifulSoup
import requests
import re

archive = "https://sinfest.xyz/archive.php?year="
def since(year, month, day):
    return (date(year,month,day)-date(2000,1,1)).days

#year, month, day, title, link, keywords, folder
arr = np.zeros((since(2025,10,16)+1,7),dtype=object)
#array of lists
keys = np.empty((since(2025,10,16)+1),dtype=object)

for l in range(2000,2026):
    arcSoup = BeautifulSoup(requests.get(archive + str(l)).text, "html.parser")
    with open("Backcode.txt", "w", encoding="utf-8") as file:
        file.write(str(arcSoup))

    with open("Backcode.txt", "r") as file:
        line = file.readline()
        toPrint = False
        while not toPrint:
            if "January" in line:
                toPrint = True
            line = file.readline()
        while toPrint:
            if "href" in line:
                temp = line[line.find("href") + 6:]
                while "view" in temp:
                    i = since(int(temp[14:18]), int(temp[19:21]), int(temp[22:24]))
                    arr[i][4] = "sinfest.xyz/" + temp[:24]
                    arr[i][0] = temp[14:18]
                    arr[i][1] = temp[19:21]
                    arr[i][2] = temp[22:24]
                    temp = temp[33:]
                    arr[i][3] = temp[:temp.find(">") - 1]
                    temp = temp[temp.find("href") + 6:]
            if "<head>" in line:
                break
            line = file.readline()

    #This section finds all the keys

    for k in range(16, since(2025,10,16)+1):
        if arr[k][3] == 0 or arr[k][5] != 0:
            continue
        out = []
        print(arr[k][3])
        print(k)
        url = "https://sinfest.xyz/comicdb.php?query="+arr[k][3]
        page = requests.get(url)
        soup = BeautifulSoup(page.text, features="html.parser")
        #Finds number of pages of search results
        try:
            count = int(soup.find_all('p')[2].get_text(separator="\n", strip=True)[-6])
        except IndexError:
            count = 1
        for j in range(1, count+1):
            page = requests.get(url+"&page="+str(j))
            soup = BeautifulSoup(page.text, features="html.parser")
            temp1 = soup.find_all('td')
            for i in range(1, len(temp1)):
                lines = soup.find_all('td')[i].get_text(separator="\n", strip=True)
                out.append(lines)
        for item in out:
            if not("Score:" in item): continue
            cut = item[item.find("[") + 1:]
            code = since(int(cut[0:4]),int(cut[5:7]),int(cut[8:10]))
            arr[code][5] = cut[12:]
            keys[code] = re.split(r'[ ,]', cut[12:])
    np.savetxt('ComicList.txt', arr, delimiter='|', fmt='%s')