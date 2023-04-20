import json
import tree

def tree_txt_to_dict():
    ''' opens the tree.txt file, reads the file, then formats
    data in into a dictionary, where the keys are the parent nodes
    and each key's values are the children nodes of each parent

    Parameters
    ----------
    None

    Returns
    -------
    dict: keys are the parent nodes and each key's values are the children nodes of each parent
    '''
    # opens tree file
    tree = open("tree.txt", "r")
    categories_info = tree.read()
    categories_list = (categories_info.split("\n"))
    for i in categories_list:
        i = i.replace("_", " ").title()

    # formats tree into dictionary to be readable
    test = []
    keys = []
    for i in categories_list:
        if "  |--" == i[0:5]:
            test.append(i.replace("  |--", ""))
            keys.append(i.replace("  |--", ""))
        if "    |--" == i[0:7]:
            test.append([i.replace("    |--", "")])

    categories_dict = {}
    for i in test:
        for key in keys:
            if i == key:
                categories_dict.update({key:[]})

    for i in test:
        if i in keys:
            currentKey = i
        if isinstance(i, list) == True:
            val = i[0]
            categories_dict[currentKey].append(val)

    return categories_dict

def createTreeJSON(treeFilename):
    ''' writes the tree dictionary into a JSON file

    Parameters
    ----------
    treeFilename: str
        name of file to save the tree

    Returns
    -------
    None
    '''
    treedict = {"categories": tree_txt_to_dict()}
    with open(treeFilename, 'w') as f:
        json.dump(treedict, f, indent=4)

def readTreeJSON(treeFilename):
    ''' opens and returns the tree json file if it exists
    if the tree file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened tree JSON file
    '''
    try:
        tree_file = open(treeFilename, 'r')
        tree_contents = tree_file.read()
        tree_data = json.loads(tree_contents)
        tree_file.close()
        return tree_data
    except:
        print("Tree file does not exist")

# set name to save tree as a JSON file
treeFilename = 'tree.json'

# save tree as a JSON
createTreeJSON(treeFilename)

# print the tree
print(f"Tree Created for Categories: {tree.run()}")

# read tree stored in JSON file
treeCreated = readTreeJSON(treeFilename)

# print root and parent nodes
print(f'\nCategories and Subcategories Info Extracted from Tree')
print("-------------------------------------------------------")
print(f"\nRoot of tree: {list(treeCreated.keys())[0].upper()}")
for key in treeCreated["categories"].keys():
    print(f'Parent node (Category): {key.upper()} ==> Number of children nodes (Sub-categories): {len(treeCreated["categories"][key])}')