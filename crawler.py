import requests
from bs4 import BeautifulSoup
from os import mkdir
import re

forumURL = "https://bbs.nyasama.com/forum.php"
class Crawler:

    def download(self, id, page = 1, begin = 1):

        content = requests.get(forumURL, params={"mod":"viewthread", "tid":id, "page":str(page)}).text
        soup = BeautifulSoup(content, "lxml")

        titleText = soup.title.text
        titleText = titleText[titleText.find("】") + 1:titleText.find(" - ")]

        imgList = soup.find_all("img", class_ = "zoom")

        pageNum = 1
        if page == 1:
            try:
                pageNum = int(re.match(" / (.*) 页", soup.find("span", title=re.compile("共 .* 页")).text).group(1))
                print (str(pageNum) + " page(s) found.")
            except AttributeError:
                pass

        if len(imgList) == 0:
            print("Nothing found.")
            return 0

        c = input("Download " + titleText + " with " + str(len(imgList)) + " pictures ?")
        if c == "n": return 0

        try:
            mkdir(titleText.encode())
        except FileExistsError:
            print("Directory already created.")

        for index, item in enumerate(imgList):
            pic = item.attrs["file"]
            picType = pic[-3:]
            f = requests.get(pic)
            filename = titleText + "/" + str(index + begin).zfill(4) + "." + picType
            print("Downloading " + filename + "...")
            with open(filename, "wb") as code:
                code.write(f.content)
        print(str(len(imgList)) + " item(s) downloaded.")

        if pageNum != 1:
            sum = len(imgList)
            for p in range(2, pageNum + 1):
                print("Now processing page " + str(p) + "...")
                sum += self.download(id, p, begin + sum)
        return len(imgList)

    def view(self, page = 1):
        content = requests.get(forumURL, params = {"mod":"forumdisplay", "fid":"3", "page":page}).text
        soup = BeautifulSoup(content, "lxml")
        title = soup.find_all("a", class_="s xst", text=re.compile("【喵玉.*"))
        for index, item in enumerate(title):
            print(str(index) + " :" + item.text)
        x = input("Which to download?")
        if x == 'n': return
        try:
            n = int(x)
            print(title[n].text, title[n].attrs["href"])
            id = re.match(".*&tid=(.*)&.*", title[n].attrs["href"]).group(1)
            self.download(id = id)
        except (ValueError, IndexError):
            print("Invalid input.")
            return

if __name__ == "__main__":
    c = Crawler()
    cmd = input("View Page:")
    while (cmd != "n"):
        try:
            p = int(cmd)
        except ValueError:
            print("Invalid input.")
        else:
            c.view(p)
        cmd = input("View Page:")