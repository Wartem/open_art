from pprint import pprint

import wikipedia as wiki


# Prevents having Author objects with uninitialized members
class Author_Factory:

    def __init__(self):
        pass

    def build(self, author_search):
        search_res = wiki.search(author_search)
        for res in search_res:
            temp = self.Author(res)
            if temp.is_artist:
                return temp
        return None

    class Author:
        def __init__(self, name):
            self.author = wiki.page(name)
            self.name = self.author.title
            self.categories = self.author.categories
            self.images = self.author.images
            self.summery = self.author.summary
            self.all = self.author, self.name, self.categories, self.images, self.summery
            self.is_artist = self.is_artist_in_category(self.categories)

        @staticmethod
        def is_artist_in_category(categories: list):
            for category in categories:
                if "artist" in category:
                    return True
            return False


def test():
    author = Author_Factory().build("Tito Lessi")

    if author:

        if author.is_artist:
            print("Artist found!")
        else:
            print("Artist keyword not found in this wikipedia page's category section")
    else:
        print("Author init failed")

    print(author.name)
    print(author.summery)


if __name__ == "__main__":
    test()