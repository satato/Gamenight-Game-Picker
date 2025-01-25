import json

valid_ys = ['y','Y','yes','Yes','YES']
valid_ns = ['n','N','no','No','NO']

GAMES = {}
TITLES = []

def request_price(title):
    # price
    Price = None
    valid_response = False
    while (not valid_response):
        print("\nWhat is the price of " + title + "? (Enter price without symbols, eg. 19.99)")
        Price = input()

        try:
            Price = float(Price)
            valid_response = True
        except ValueError:
            print("Invalid response. Please try again.\n")

    return (Price)


def request_gathering_info(title):
    Gathering_Min = None
    Local_Gathering_Max = None
    Online_Gathering_Max = None

    # get the min
    valid_response = False
    while (not valid_response):
        print("\nWhat is the smallest gathering that can play " + title + "? (if singleplayer, enter '1')")
        Gathering_Min = input()

        try:
            Gathering_Min = int(Gathering_Min)
            valid_response = True
        except ValueError:
            print("Invalid response. Please try again.\n")

    # get the local max
    valid_response = False
    while (not valid_response):
        print("\nWhat is the largest gathering that can play " + title + " LOCALLY? (if singleplayer, enter '1')")
        Local_Gathering_Max = input()

        try:
            Local_Gathering_Max = int(Local_Gathering_Max)
            valid_response = True
        except ValueError:
            print("Invalid response. Please try again.\n")
    
    # get the online max
    valid_response = False
    while (not valid_response):
        print("\nWhat is the largest gathering that can play " + title + " ONLINE? (if singleplayer, enter '1')")
        Online_Gathering_Max = input()

        try:
            Online_Gathering_Max = int(Online_Gathering_Max)
            valid_response = True
        except ValueError:
            print("Invalid response. Please try again.\n")

    return (Gathering_Min, Local_Gathering_Max, Online_Gathering_Max)


def request_game_info():
    cooperative = None
    competitive = None

    # title
    print("\n-------------------------------\nPlease enter the title of the game to be added:")
    title = input()

    if title in TITLES:
        print("That title is already in your library. To edit its information, please remove it and re-add it with the correct info.")
        return False

    # get info about stores & prices
    Price = request_price(title)

    # gathering size minimum and maximum
    Gathering_Min, Local_Gathering_Max, Online_Gathering_Max = request_gathering_info(title)

    # cooperative gameplay?
    valid_response = False
    while (not valid_response):
        print("\nDoes " + title + " have cooperative gameplay? (y/n)")
        cooperative = input()
        if cooperative in valid_ys:
            cooperative = True
            valid_response = True
        elif cooperative in valid_ns:
            cooperative = False
            valid_response = True
        else:
            print("Invalid response. Please try again.\n")
        
    # competitive gameplay?
    valid_response = False
    while (not valid_response):
        print("\nDoes " + title + " have competitive gameplay? (y/n)")
        competitive = input()
        if competitive in valid_ys:
            competitive = True
            valid_response = True
        elif competitive in valid_ns:
            competitive = False
            valid_response = True
        else:
            print("Invalid response. Please try again.\n")

    # all necessary data acquired! build dictionary of it
    return {
            "title": title,
            "Price": Price,
            "Player-Min": Gathering_Min,
            "Local-Max": Local_Gathering_Max,
            "Online-Max": Online_Gathering_Max,
            "Coop": cooperative,
            "Comp": competitive
        }


def add_game():
    game = request_game_info()
    if game == False:
        return False # no game added
    else:
        # add the game!
        count = len(GAMES)
        GAMES[count + 1] = game
        return True


def delete_game(ID):
    id_passed = False
    orig_len = len(GAMES)

    for i in range(1, len(GAMES) + 1):
        if i == ID:
            GAMES.pop(i)
            id_passed = True
        elif id_passed:
            GAMES[i - 1] = GAMES[i]
        else:
            pass

    # potential extra value at the end, pop it
    if len(GAMES) == orig_len:
        GAMES.pop(orig_len)


def del_game():
    quit = False

    while (not quit):
        print("Please enter the ID of the game you would like to remove from your library.")
        print("Enter '0' to have your library listed out for reference.")
        print("Or press Q to quit.")

        response = input()
        if response == '0':
            list_games()
        elif (response == 'q' or response == 'Q'):
            quit = True
        else:
            try:
                ID = int(response)
                title = GAMES[ID]['title']
                print("\nTo confirm: you would like to delete " + title + " from your library? (y/n)")
                if input() in valid_ys:
                    delete_game(ID)
                    list_games()
                else:
                    print("\n\n")
            except ValueError:
                print("Invalid response. Please try again.\n\n")


def export_games_list():
    print("Would you like this list exported to a file? (y/n)")
    if input() in valid_ys: # print to file
        with open("./exports/nintendo-games-list.txt", "w") as f:
            for i in range(1, len(GAMES) + 1):
                f.write(str(i) + ": " + GAMES[i]['title'] + "\n")

    print("\nYour games list has been exported to 'nintendo-games-list.txt'")
    print("\n\n")


def list_games():
    print("\n-------------------------------")
    for i in range(1, len(GAMES) + 1):
        print(str(i) + ": " + GAMES[i]['title'])

    print("-------------------------------")
    export_games_list


def pull_record():
    with open("./data/nintendo-games.json", "r") as f:
        data = json.load(f)

    games = {}
    titles = []

    for i in range(1, len(data) + 1): # number of games = len(data)
        game = data[str(i)]
        games[i] = game
        titles.append(game['title'])

    return (games, titles)


def save_by_category():
    CATEGORIES = {
        "free": [], # free games
        "<20": [], # cost $20 or less
        "local2player": [], # local 2-player games only
        "online2player": [], # online 2-player games only
        "localUpTo4": [], # supports up to 4 players locally
        "OnlineUpTo4": [], # supports up to 4 or more players online
        "OnlineUpTo8": [], # supports up to 8 or more players online
        "coop": [], # cooperative gameplay
        "comp": [] # competitive gameplay
    }

    for i in range(1, len(GAMES) + 1):
        game = GAMES[i]
        # check price
        if game['Price'] == 0:
            CATEGORIES['free'].append(i)
        if game['Price'] <= 20.00:
            CATEGORIES['<20'].append(i)
        # check player count
        if game['Local-Max'] >= 2:
            CATEGORIES['local2player'].append(i)
        if (game['Online-Max'] != None and game['Online-Max'] >= 2):
            CATEGORIES['online2player'].append(i)
        if game['Local-Max'] >= 4:
            CATEGORIES['localUpTo4'].append(i)
        if (game['Online-Max'] != None and game['Online-Max'] >= 4):
            CATEGORIES['OnlineUpTo4'].append(i)
            if game['Online-Max'] >= 8:
                CATEGORIES['OnlineUpTo8'].append(i)
        if game['Coop']:
            CATEGORIES['coop'].append(i)
        if game['Comp']:
            CATEGORIES['comp'].append(i)

    return CATEGORIES


def save():
    # save games.json
    with open("./data/nintendo-games.json", "w") as f:
        json.dump(GAMES, f, indent=4)

    # save games_by_category.json
    categories = save_by_category()
    with open("./data/nintendo-games-by-category.json", "w") as f:
        json.dump(categories, f, indent=4)


if __name__ == "__main__":
    # pull existing record of games
    GAMES, TITLES = pull_record()

    # ask user for action
    quit = False
    while (not quit):
        print("Enter 1 to add a game to your library")
        if len(GAMES) != 0:
            print("Enter 2 to remove a game from your library")
        print("Enter 3 to list your entire games library")
        print("Enter Q to quit")

        response = input()
        if (response == 'q' or response == 'Q'):
            quit = True
            print("Would you like to save changes made during this session before quitting? (y/n)")
            if input() in valid_ys:
                save()
        elif (response == '1'):
            if add_game():
                print("-------------------------------\nSave changes? (y/n)")
                if input() in valid_ys:
                    save()
        elif (response == '2'):
            if len(GAMES) == 0:
                print("Your library is empty!")
            else:
                del_game()
        elif (response == '3'):
            list_games()
            export_games_list()
        else:
            print("Not a valid response. Please try again\n\n")