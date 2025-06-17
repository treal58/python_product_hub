# Python Product Hub

Python project for creating and managing products and their topics.

Made purely for learning and entertainment purposes.

## Module: products.py

- Contains all the core logic of the project

### Products

- They have to be given a name, topic and base price when crated. The name will be automatically capitalized, and taxes will be automatically applied to the price

### Topics

- They are assigned to products when they are created
- If a product is created with an invalid topic, the topic will be 'default' (10% tax)
- A list of default topics is given, but you can create custom ones.

#### Default Topics

|  Topic Name | Tax Percentage |
| ------------- |:-------------:|
| default | 10% |
| consumables | 8% |
| digital | 14% |
| sports | 14% |
| health | 8% |
| plants | 18% |
| clothes | 20% |
| makeup | 20% |
| furniture | 15% |
| tech | 16% |


### Core Functions

|  Function | Functionality |
| ------------- |:-------------:|
| apply_taxes(topic_name, base)      |   Base function used to apply taxes.<br>Requires the topic and the base price, and returns the taxed price. |
| create_topic(name, tax)            |  Creates a new topic usable for new products |
| export_prd_to_json(filename="products.json") |  Exports all current products to a .json file<br>(If you added custom topics, make sure to also export and import them)   |
| import_prd_from_json(filename="products.json") | Imports all products in a .json file<br>(If you added custom topics, make sure to import them before, because 'default' will be assigned to your products instead) |
| chart(*args) | Basic function that returns all the current products and their prices in a list of strings | 

## Products Hub: main.py

It's a GUI for accessing the different product tools (Searcher, Topic Manager and Product Manager)

You can view Current Products and Current Topics from there

### Searcher

You can search products and it will tell you their stats

### Product Manager

From here you can create, import and export products.

Make sure to also import/export custom topics when dealing with products. 
Otherwise, products may fall back to the 'default' topic even if another topic was originally assigned.

### Topic Manager

From here you can create, import, and export custom topics.

## How to Use

1. Clone the repository
2. Run `main.py` for the Products Hub

You can also run:
- `topicmanager.py` to manage topics (limited functionality if alone)
- `productmanager.py` to manage products (limited functionality if alone)
- `searcher.py` to search existing products (does not work standalone — requires products to be created via code)

- You can also use `products.py` directly for scripting or core logic testing.