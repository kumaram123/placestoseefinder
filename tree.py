import cache
import json

class TreeNode:
    def __init__(self,data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self,child):
        self.child = child
        child.parent = self
        self.children.append(child)

    def get_level(self):
        level = 0
        p = self.parent
        while p :
            p = p.parent
            level += 1
        return level

    def print_tree(self):
        print('  '*self.get_level() + '|--', end = '')
        print(self.data)
        if self.children:
            for each in self.children:
                each.print_tree()

    def saveTree(self):
        with open('savedTree.txt', 'a') as f:
            f.write('  '*self.get_level() + '|--')
            f.write(f"{self.data}\n")
            if self.children:
                for each in self.children:
                    each.saveTree()

def run():
    categories = cache.checkCacheExistence("yelp_API_cache_Novi.json")
    key = list(categories.keys())[0]

    parent_aliases = []
    for i in categories[key]["categories"]:
        for j in i["parent_aliases"]:
            if j not in parent_aliases:
                parent_aliases.append(j)

    parent_aliases = sorted(parent_aliases)

    root = TreeNode('Categories')
    for parents in parent_aliases:
        category = TreeNode(parents)
        root.add_child(category)
        for i in categories[key]["categories"]:
            for j in i["parent_aliases"]:
                if j == parents:
                    category.add_child(TreeNode(i["alias"]))

    #root.saveTree()
    root.print_tree()

#if __name__ == '__main__':
#    run()
#    pass