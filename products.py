# products.py
# Core module for defining and handling product-related logic.
# Includes tax calculation, product management, topic creation, and JSON I/O functions.

import json
import logging

def tax_help():
    info = (
        "\n- TAX HELP -"
        "\n    Tax function:   "
        "\napply_taxes(TOPIC, PRICE)\n"

        "\n--"
        "\n'create_topic(name, tax_percentage)' function available for new topics"
        "\n--"
        "\n'Product(name, topic, price)' class available for new topics (auto-taxes)"

        "--------------------\n"
        "   Default Topics:  \n"
        "--------------------"
        "\n10% - default"
        "\n08% - consumables"
        "\n14% - digital"
        "\n14% - sports"
        "\n08% - health"
        "\n18% - tourism"
        "\n20% - clothes"
        "\n20% - makeup"
        "\n15% - furniture"
        "\n16% - tech\n"
        "--------------------\n\n"
        
        "--------------------\n"
        "   Custom Topics:  \n"
        "--------------------"
    )
    for key, value in list(topics.items())[10:]:
        info += f"\n{value}% - {key}"
    info += "\n--------------------"

    return info

# ------ TOPICS ------
topics = {
    "default": 10,
    "consumables": 8,
    "digital": 14,
    "sports": 14,
    "health": 8,
    "plants": 18,
    "clothes": 20,
    "makeup": 20,
    "furniture": 15,
    "tech": 16
}
# ---------------------

logging.basicConfig(
    filename="error-log.txt",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def create_topic(name: str, tax: int) -> None:
    # Adds a new custom topics to the topics dictionary
    if not name.isalpha():
        raise ValueError("Topic name must be only letters (a-z)")
    if name in topics:
        raise ValueError(f"Topic '{name}' already exists")
    topics[name] = tax

def apply_taxes(topic_name: str, base: float) -> float:
    tax = topics.get(topic_name)
    return base * (1 + tax / 100)

class Product:
    _instances = []

    def __init__(self, name, topic, price):
        # Capitalized name is used to mantain visual consistency
        self.name = name.capitalize()
        # But topic is always lowercase for easier reference
        topic = topic.lower()

        if any(p.name == self.name for p in Product._instances):
            raise ValueError(f"Product '{self.name}' already exists.")

        if topic not in topics:
            print(f"Topic '{topic}' not found. Using default.")
            self.topic = "default"
        else:
            self.topic = topic

        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        else:
            self.notax_price = price

        # Calculates final taxed price, rounded to 2 decimals
        self.price = round(apply_taxes(self.topic, self.notax_price), 2)
        # Adds a reference for the object for further use
        self._instances.append(self)

    # The list 'instances' will contain references to all the products
    @classmethod
    def get_instances(cls):
        return cls._instances

def delete_products(name: str) -> bool:
    product_list = Product.get_instances()
    # Deletes the reference of the product in the 'instances' list
    for product in product_list:
        if name.capitalize() == product.name:
            product_list.remove(product)
            return True
    # If the product isn't found False will be returned
    return False


def export_prd_to_json(filename="products.json"):
    data = []

    # Takes all the current products and exports them to a .json
    for product in Product.get_instances():
        data.append({
            "name": product.name,
            "topic": product.topic,
            "price": product.notax_price
        })
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def import_prd_from_json(filename="products.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            broken = 0
            names = {product.name for product in Product.get_instances()}
            # The set 'names' is used to check if the product being imported already exists.
            for idx, item in enumerate(data):
                # First it checks if there's something missing in the product
                if not all(k in item for k in ("name", "topic", "price")):
                    logging.warning(f"[!] Some items of the product '{item.get('name', '?')}' were missing")
                    print(f"[!] Some items of the product '{item.get('name', '?')}' were missing")
                    broken += 1
                else:
                    try:
                        # Then it checks if it already exists with the set 'names'
                        if item["name"] in names:
                            print(f"Product '{item['name']}' skipped; It already exists")
                        else:
                            price = float(item["price"])
                            Product(item["name"], item["topic"], price)

                    # If the product doesn't have the correct type on its parameters it won't be imported
                    except (ValueError, TypeError):
                        print(f"[!] Make sure the product was correctly exported '{item.get('name', '?')}'")
                        logging.warning(f"[!] Make sure the product was correctly exported '{item.get('name', '?')}'")
                        broken += 1
            if broken > 0:
                print(f"{broken} broken product/s found while importing {filename}")
                logging.warning(f"{broken} broken product/s found while importing {filename}")
        return True

    # File problem exceptions
    except FileNotFoundError:
        logging.error("Couldn't find the file: %s", filename)
        return False
    except json.JSONDecodeError:
        logging.error("Couldn't read the file (Make sure it's an exported JSON): %s", filename)
        return False

def export_topics_json(filename="topics.json", topics_to_export=None):
    # First, a list for the topics to export is created
    data = []

    topics_items = list(topics.items())[10:]  # 10: Will omit the first 10 topics, which are the default ones.

    # 'topics_to_export' has to be used only if you want to export SOME items
    # if you don't fill topics_to_export with anything, then all topics will be exported
    for name, percentage in topics_items:
        if not topics_to_export or name in topics_to_export:
            data.append({name: percentage})

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def import_topics_json(filename="topics.json", preview=False):
    try:
        with open(filename, "r") as f:
            data = json.load(f)

            # If preview = True ONLY the data will be returned, but no topics will be created
            # This is useful if you want the user to select which topics it has to import
            if preview:
                return data
            for topic in data:
                for name, percentage in topic.items():
                    create_topic(name, percentage)
            return True
    except FileNotFoundError:
        logging.error("Couldn't find the file: %s", filename)
        return [] if preview else False
    except json.JSONDecodeError:
        logging.error("Couldn't read the file (Make sure it's an exported JSON): %s", filename)
        return [] if preview else False


def chart(*args):

    # This is a simple chart for showing all the products in Args
    lines = list()
    lines.append(f"{'Product':<15}{'Price':>10}")
    lines.append("-" * 25)
    for arg in args:
        lines.append(f"{arg.name:<15}{arg.price:>10.2f}")
    return "\n".join(lines)