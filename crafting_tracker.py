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
            ingredient = ingredient.lower()
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


def ingredient_counter(ingredients, converted_tracker):
    counted_ingredients = {}
    for item in ingredients:
        item_name = item.get("name")
        item_count = item.get("count")
        if item_name not in converted_tracker:
            return "The recipe for " + item_name + " is incomplete"
        item = converted_tracker.get(item_name)

        #base case, no nested ungredients
        if item.get("base"):
            counted_ingredients[item_name] = item_count
        else:

            #recursive step
            subcount = ingredient_counter(item.get("ingredients"), converted_tracker)
            for subitem in subcount.keys():
                #adds to current count
                if subitem in counted_ingredients:
                    counted_ingredients[subitem] = counted_ingredients.get(subitem) + (item_count * subcount.get(subitem))
                else:
                    counted_ingredients[subitem] = item_count * subcount.get(subitem)

    return counted_ingredients


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
        item.lower()
        if item == 0:
            exit()
        if item in converted_tracker:
            accepted = True
        if item not in converted_tracker:
            print("That item is not in the tracker")

    count = int(input("How many would you like to craft?\n"))

    if converted_tracker.get(item).get("base"):
        print(item + ": " + str(count))
        exit()

    ingredient_list = ingredient_counter(converted_tracker.get(item).get("ingredients"), converted_tracker)
    for ingredient in ingredient_list.keys():
        print(ingredient + ": " + str(count * ingredient_list.get(ingredient)))

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
