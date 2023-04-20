# Tree Data Structure

## tree.py
A tree data structure has been used to store the categories and subcategories information of all the “places to see” in a hierarchical manner. The “categories” information is accessed using an API key from the Yelp Fusion “categories” endpoint. The API data is cached and stored in a JSON file. The “categories” information contains various attributes regarding each category, but the two attributes used to create the tree are: __“parent_alias”__ (main category) and __“alias”__ (name of the category).

For example, under the parent category  “Active”, there are many subcategories such as “amusement parks”, “boating”, “flyboarding”, etc. In order to organize all the categories of “places to visit” in a tree data structure, I have created a “TreeNode” class with the following member functions: __init()__, __add_child()__: adds a child to a parent node, __get_level()__: gets the level of a specific node, and __print_tree()__: formats and prints the tree in a readable format. To begin, I set the root of the tree to be “categories”. The second level of the tree will be all the “parent aliases”, which are the parent categories. The third level of the tree is all the sub-categories within each parent alias. For example, the flow would be something like: Root: “Category” => Parent Alias: “Active” => Sub-Category: “Boating”.

## readTree.py

Holds the necessary functions to save the tree data structure into and JSON file and read the tree stored in a JSON file.

The readtree.py script outputs the tree, root & parent nodes of the tree, and the number of children nodes under each parent node.

Contains 3 functions: __tree_txt_to_dict()__: converts tree contents stored in a .txt file into a dictionary, __createTreeJSON()__: creates a .JSON file of the tree, __readTreeJSON()__: opens and reads the tree .JSON file

## tree.json

Contains the tree contents. Main key in the JSON file is "categories", which is the root node. The keys under "categories" are the parent nodes. The values corresponding to each parent node are the children nodes, which are the sub-categories within each parent node.
