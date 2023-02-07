import json

class CategoryHandler():
    merge_id = [7, 9]
    def __init__(self, path):
        self.path = path
        self.category_json = json.load(open(path))
        self.category = self.category_json['categories']
        
    def get_cat_id(self, cat_name):
        cat = next(item for item in self.category if item["name"] == cat_name)
        isignore = cat['ignore']
        if isignore:
            # print(1)
            cat = self.category[-1]
        cat_id = cat['id']

        # temp for merging 
        if cat_id == 7 or cat_id == 9:
            cat_id = 9

        return cat_id

    def get_cat_name(self, cat_id):
        cat = next(item for item in self.category if item["id"] == cat_id)
        cat_name = cat['name']
        return cat_name