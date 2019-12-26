import json

FILE_NAME = "crafting_tracker.json"


def ceildiv(a, b):
    return -(-a // b)


def item_adder():
    # Loads the json object from the file
    file = open(FILE_NAME, "r")
    tracker = json.load(file)
    tracker = tracker.get("tracker")
    file.close()
    file = open(FILE_NAME, "w")

    # converts the list of items to a dict for ease of use
    converted_tracker = {}
    for item in tracker:
        converted_tracker[item.get("name")] = item

    while True:
        item = input("Enter the name of an item, or 0 to exit\n")
        if item == "0":
            tracker = {"tracker": tracker}
            output = json.dumps(tracker)
            file.write(output)
            exit()
        if item in converted_tracker:
            print("That item already exists")
            continue
        ingredients = []
        ingredient = ""

        while ingredient != "0":
            ingredient = input("Input an ingredient, or 0 if there are no more\n")
            ingredient.lower()
            if ingredient != "0":
                count = input("How many are there of that ingredient?\n")
                ingredients.append((ingredient, count))

        base = len(ingredients) == 0
        yields = 1
        if not base:
            yields = input("How many does the recipe make?\n")

        converted_ingredients = []
        for ingredient in ingredients:
            converted_ingredients.append({"name": ingredient[0], "count": ingredient[1]})
        if base:
            tracker.append({"name": item, "base": base})
        else:
            tracker.append({"name": item, "base": base, "yields": yields, "ingredients": converted_ingredients})

        #Prints the new json object to file
        tracker = {"tracker": tracker}

        #Prepares loop for next iteration
        tracker = tracker.get("tracker")


def ingredient_counter(item, count, converted_tracker):
    if item.get("base"):
        return {item.get("name"): count}

    count = ceildiv(count, int(item.get("yields")))

    counted_ingredients = {}

    for ingredient in item.get("ingredients"):
        item_name = ingredient.get("name")
        item_count = int(ingredient.get("count"))
        if item_name not in converted_tracker:
            print("Recipe for " + ingredient.get("name") + " not found")
            exit()
        counted_ingredients[item_name] = item_count * count

    base_ingredients = {}
    for ingredient in counted_ingredients.keys():
        subcount = ingredient_counter(converted_tracker.get(ingredient), int(counted_ingredients.get(ingredient)), converted_tracker)
        for base in subcount.keys():
            if base in base_ingredients:
                base_ingredients[base] = base_ingredients.get(base) + subcount.get(base)
            else:
                base_ingredients[base] = subcount.get(base)

    return base_ingredients

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

    item = ""
    craft_list = []
    while item != "0":
        item = input("Input an item you would like to craft, or 0 to see total cost\n")
        item.lower()
        if item != "0":
            if item not in converted_tracker:
                print("That item is not in the tracker")
            else:
                count = int(input("How many would you like to craft?\n"))
                if item in converted_tracker:
                    craft_list.append((converted_tracker.get(item), count))


    base_ingredients = {}
    for item in craft_list:
        ingredient_list = ingredient_counter(item[0], item[1], converted_tracker)
        for ingredient in ingredient_list.keys():
            if ingredient in base_ingredients:
                base_ingredients[ingredient] = base_ingredients.get(ingredient) + ingredient_list.get(ingredient)
            else:
                base_ingredients[ingredient] = ingredient_list.get(ingredient)

    for ingredient in base_ingredients.keys():
        print(ingredient + ": " + str(base_ingredients.get(ingredient)))

    exit(0)


if __name__ == "__main__":

    print("Enter 1 to add items, 2 to add item costs, or 0 to exit")
    num = int(input())
    while True:
        if num == 0:
            exit()

        if num == 1:
            item_adder()

        if num == 2:
            recipe_searcher()
