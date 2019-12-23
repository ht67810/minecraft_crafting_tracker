import json

FILE_NAME = "crafting_tracker.json"


def item_adder():
    # Loads the json object from the file
    file = open(FILE_NAME, "r")
    tracker = json.load(file)
    tracker = tracker.get("tracker")
    file.close()

    item = input("Enter the name of an item\n")
    ingredients = []
    ingredient = ""

    while ingredient != "0":
        ingredient = input("Input an ingredient, or 0 if there are no more\n")
        ingredient = ingredient.lower()
        if ingredient != "0":
            count = input("How many are there of that ingredient?\n")
            ingredients.append((ingredient, count))

    base = len(ingredients) == 0
    converted_ingredients = []
    for ingredient in ingredients:
        converted_ingredients.append({"name": ingredient[0], "count": ingredient[1]})
    if base:
        tracker.append({"name": item, "base": base})
    else:
        tracker.append({"name": item, "base": base, "ingredients": converted_ingredients})

    #Prints the new json object to file
    tracker = {"tracker": tracker}
    file = open(FILE_NAME, "w")
    output = json.dumps(tracker)
    file.write(output)

def ingredient_counter(ingredients, converted_tracker):
    counted_ingredients = {}
    for item in ingredients:
        if item not in converted_tracker:
            return "The recipe for " + item + " is incomplete"
        



def recipe_searcher():
    # Loads the json object from the file
    file = open(FILE_NAME, "r")
    tracker = json.load(file)
    tracker = tracker.get("tracker")
    file.close()

    #converts the list of items to a dict for ease of use
    converted_tracker = {}
    for item in tracker:
        converted_tracker[item.get("name")] = item

    accepted = False
    while not accepted:
        item = input("Input an item you would like to craft, or 0 to exit\n")
        if item == 0:
            exit()
        if item in converted_tracker:
            accepted = True

    num = int(input("How many would you like to craft?"))

if __name__ == "__main__":

    print("Enter 0 to add items or 1 to add item costs")
    num = int(input())

    if num == 0:
        item_adder()

    if num == 1:
        recipe_searcher()
