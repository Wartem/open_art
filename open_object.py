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

        self.full_url = ""
        self.full_url_downsized = ""
        self.full_url_thumb = ""

        self.fix_image_properties()

    def fix_image_properties(self):

        if self.width > 4096 or self.height > 4096:
            if self.width > 4096:
                self.width = 4096

            if self.height > 4096:
                self.height = 4096

            self.full_url = self.iiifurl + "/full/!" + self.width + "," + self.height + "/0/default.jpg"
        else:
            self.full_url = self.iiifurl + "/full/" + self.width + "," + self.height + "/0/default.jpg"

        if self.height > 1500 or self.width > 1500:
            self.full_url_downsized = self.iiifurl + "/full/!" + 1500 + "," + 1500 + "/0/default.jpg"
        else:
            self.full_url_downsized = self.iiifurl + "/full/!" + self.width + "," + self.height + "/0/default.jpg"
            self.full_url_thumb = self.iiifurl + "/full/!200,200/0/default.jpg"