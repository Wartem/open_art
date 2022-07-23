


class Object:

    def __init__(self, source, objectid, title,
                 attribution, beginyear, endyear, displaydate,
                 classification, medium, width, height, iiifurl):
        self.source = source
        self.objectid = objectid
        self.title = title
        self.attribution = attribution
        self.beginyear = beginyear
        self.endyear = endyear
        self.displaydate = displaydate
        self.classification = classification
        self.medium = medium
        self.width = width
        self.height = height
        
        self.iiifurl = iiifurl

        self.imgurl_full = ""
        self.imgurl_downsized = ""
        self.imgurl_thumb = ""

        self.fix_image_properties()

    def fix_image_properties(self):

        if self.width > 4096 or self.height > 4096:
            if self.width > 4096:
                self.width = 4096

            if self.height > 4096:
                self.height = 4096

            self.imgurl_full = self.iiifurl + "/full/!" + self.width + "," + self.height + "/0/default.jpg"
        else:
            self.imgurl_full = self.iiifurl + "/full/" + self.width + "," + self.height + "/0/default.jpg"

        if self.height > 1500 or self.width > 1500:
            self.imgurl_downsized = self.iiifurl + "/full/!" + 1500 + "," + 1500 + "/0/default.jpg"
        else:
            self.imgurl_downsized = self.iiifurl + "/full/!" + self.width + "," + self.height + "/0/default.jpg"
            self.imgurl_thumb = self.iiifurl + "/full/!200,200/0/default.jpg"
            
        
"""         def addImageUrls(df):
         
        for index, row in df.iterrows():
            print(row["iiifurl"][index])
         

        if(row["width"][index] > 4096 or row["height"][index] > 4096):

            if (row["width"][index] > 4096):
                row["width"][index] = 4096
            

            if (row["height"][index] > 4096):
                row["height"][index] = 4096
            

            imgurl_full = Iiifurl + "/full/!" + row["width"][index] + "," + row["height"][index] + "/0/default.jpg"
        
        else:
            imgurl_full = Iiifurl + "/full/" + row["width"][index] + "," + row["height"][index] + "/0/default.jpg"
        

        if (row["height"][index] > 1500 or row["width"][index] > 1500):
            imgurl_fulldownsized = Iiifurl + "/full/!" + 1500 + "," + 1500 + "/0/default.jpg"
        
        else:
            imgurl_fulldownsized = Iiifurl + "/full/!" + row["width"][index] + "," + row["height"][index] + "/0/default.jpg"
        


        imgurl_fullthumb = Iiifurl + "/full/!200,200/0/default.jpg"
        
        return df """