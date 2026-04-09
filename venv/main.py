import urllib.request
import os
import pathlib
from urllib.request import urlopen
from datetime import date
from pathlib import Path

class Main:
    def __init__(self):
        self.urlForBingImage = 'https://www.bing.com/'
        self.localFileName = ""
        self.localImageName = ""
        self.finalURL = ""
        self.myResourceDirectory = str(pathlib.Path(__file__).parent.absolute()) + "/" + "Resources/"
        self.todayDate = date.today().strftime('%Y%m%d')  # YYYYMMDD

    def check_internet_connection(self, check):    #This function is to check the internet connection.
        try:
            urllib.request.urlopen(check)
            return True
        except ValueError:
            return False

    def check_If_Directory_Exists(self):     # This function is to check if the Directory exists for the purpose of storing the data.
        if Path(self.myResourceDirectory).is_dir():
            print("Directory exists :)\n", self.myResourceDirectory)
        else:
            print("Directory doesn't exist, making one now")
            os.mkdir(self.myResourceDirectory)
        return True

    # Below function is Downloading the entire bing.com webpage, and saving it as a text file to later find the image url.
    def save_HTML_into_file(self):
        print("Connected to Internet :)")
        self.localFileName = "BingWebpage_" + self.todayDate + ".txt"
        urllib.request.urlretrieve(self.urlForBingImage, self.myResourceDirectory + self.localFileName)

        tempFile = open(self.myResourceDirectory + self.localFileName, "r")
        # Below string was observed after doing inspect elements in bing.com that loads the image of the day.
        string1 = "<meta property=\"og:image\" content=\"https://www.bing.com/"     
        string2 = ".jpg"

        # Loop the file line by line
        flag = 0
        index1 = 0
        index2 = 1
        line = ""
        
        # try matching the observed URL string with the new bing.com file.
        for line in tempFile:
            index1 = line.index(string1)
            index2 = line.index(string2)
            if string1 in line:
                flag = 1
                break
            else:
                flag = 0
                print("Substring not Found :(")

        if flag == 0:
            print("URL Not Found :(")
        else:
            for i in range(index1 + len(string1), index2):
                self.finalURL = self.finalURL + line[i]
            self.finalURL = "https://www.bing.com/" + self.finalURL + string2
        tempFile.close()
        return self.finalURL

    def download_image_from_URL(self, link):
        self.localImageName = "BingWallpaper__" + self.todayDate + ".jpg"
        urllib.request.urlretrieve(link, self.myResourceDirectory + self.localImageName)
        print("Image Downloaded")
        return self.localImageName

    def set_Image_As_Wallpaper(self, localImageName):
        imgPath = self.myResourceDirectory + localImageName
        print(imgPath)
        # below is command line implementation of the wallpaper
        os.system('gsettings set org.gnome.desktop.background picture-uri file:' + imgPath)

    # Below function will delete the previous day image if the new image is downloaded.
    def delete_Old_Files(self):
        for x in os.listdir(self.myResourceDirectory):
            if str(x) != self.localImageName:
                os.system('cd ' + self.myResourceDirectory + ' && rm ' + str(x))
                # print('cd ' + self.myResourceDirectory + ' && rm ' + str(x))
        # os.system('cd ' + self.myResourceDirectory + ' && ls')


# Program begins execution from down under !
mainObj = Main()
if mainObj.check_internet_connection(mainObj.urlForBingImage):
    print("Date: ", mainObj.todayDate)
    if mainObj.check_If_Directory_Exists():
        mainObj.set_Image_As_Wallpaper(mainObj.download_image_from_URL(mainObj.save_HTML_into_file()))
        mainObj.delete_Old_Files()
        print("Wallpaper Updated")
    else:
        print("Check the Program")
else:
    print("No Internet :(")
