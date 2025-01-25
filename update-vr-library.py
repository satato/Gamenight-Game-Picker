import json

valid_ys = ['y','Y','yes','Yes','YES']
valid_ns = ['n','N','no','No','NO']

GAMES = {}
TITLES = []

def request_store_info(title):
    # in Meta store?
    valid_response = False
    while (not valid_response):
        print("\nIs " + title + " available in the Meta store? (y/n)")
        inMetaStore = input()
        if inMetaStore in valid_ys:
            inMetaStore = True
            valid_response = True
        elif inMetaStore in valid_ns:
            inMetaStore = False
            valid_response = True
        else:
            print("Invalid response. Please try again.\n")

    # in Steam store?
    valid_response = False
    while (not valid_response):
        print("\nIs " + title + " available in the Steam store? (y/n)")
        inSteamStore = input()
        if inSteamStore in valid_ys:
            inSteamStore = True
            valid_response = True
        elif inSteamStore in valid_ns:
            inSteamStore = False
            valid_response = True
        else:
            print("Invalid response. Please try again.\n")

    # stores owned on
    print("\nWhich store(s) do you own " + title + " on? Separate by comma.")
    ownedOn = input()
    # process comma separation
    ownedOn = ownedOn.split(",")

    # Meta store price
    MetaPrice = None
    if inMetaStore:
        valid_response = False
        while (not valid_response):
            print("\nWhat is the price of " + title + " in the Meta store? (Enter price without symbols, eg. 19.99)")
            MetaPrice = input()

            try:
                MetaPrice = float(MetaPrice)
                valid_response = True
            except ValueError:
                print("Invalid response. Please try again.\n")

    # Steam store price
    SteamPrice = None
    if inSteamStore:
        valid_response = False
        while (not valid_response):
            print("\nWhat is the price of " + title + " in the Steam store? (Enter price without symbols, eg. 19.99)")
            SteamPrice = input()

            try:
                SteamPrice = float(SteamPrice)
                valid_response = True
            except ValueError:
                print("Invalid response. Please try again.\n")


    return (inMetaStore, inSteamStore, ownedOn, MetaPrice, SteamPrice)


def request_gathering_info(title):
    Gathering_Min = None
    Gathering_Max = None

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

    # get the max
    valid_response = False
    while (not valid_response):
        print("\nWhat is the largest gathering that can play " + title + "? (if singleplayer, enter '1')")
        Gathering_Max = input()

        try:
            Gathering_Max = int(Gathering_Max)
            valid_response = True
        except ValueError:
            print("Invalid response. Please try again.\n")

    return (Gathering_Min, Gathering_Max)


def request_game_info():
    VR_Optional = None
    Seated = None
    Tabletop = None

    # title
    print("\n-------------------------------\nPlease enter the title of the game to be added:")
    title = input()

    if title in TITLES:
        print("That title is already in your library. To edit its information, please remove it and re-add it with the correct info.")
        return False

    # get info about stores & prices
    inMetaStore, inSteamStore, ownedOn, MetaPrice, SteamPrice = request_store_info(title)

    # VR optional?
    valid_response = False
    while (not valid_response):
        print("\nIs " + title + " VR optional (can it be played flatscreen on any platforms)?")
        VR_Optional = input()
        if VR_Optional in valid_ys:
            VR_Optional = True
            valid_response = True
        elif VR_Optional in valid_ns:
            VR_Optional = False
            valid_response = True
        else:
            print("Invalid response. Please try again.\n")

    # gathering size minimum and maximum
    Gathering_Min, Gathering_Max = request_gathering_info(title)

    # seated play?
    valid_response = False
    while (not valid_response):
        print("\nIs " + title + " a seated game?")
        Seated = input()
        if Seated in valid_ys:
            Seated = True
            valid_response = True
        elif Seated in valid_ns:
            Seated = False
            valid_response = True
        else:
            print("Invalid response. Please try again.\n")

    # tabletop game?
    valid_response = False
    while (not valid_response):
        print("\nIs " + title + " considered a 'tabletop' game?")
        Tabletop = input()
        if Tabletop in valid_ys:
            Tabletop = True
            valid_response = True
        elif Tabletop in valid_ns:
            Tabletop = False
            valid_response = True
        else:
            print("Invalid response. Please try again.\n")

    # all necessary data acquired! build dictionary of it
    return {
            "title": title,
            "inMetaStore": inMetaStore,
            "inSteamStore": inSteamStore,
            "ownedOn": ownedOn,
            "VR-Optional": VR_Optional,
            "Gathering-Min": Gathering_Min,
            "Gathering-Max": Gathering_Max,
            "Seated": Seated,
            "Tabletop": Tabletop,
            "MetaPrice": MetaPrice,
            "SteamPrice": SteamPrice
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
        with open("./exports/vr-games-list.txt", "w") as f:
            for i in range(1, len(GAMES) + 1):
                f.write(str(i) + ": " + GAMES[i]['title'] + "\n")

    print("\nYour games list has been exported to 'vr-games-list.txt'")
    print("\n\n")


def list_games():
    print("\n-------------------------------")
    for i in range(1, len(GAMES) + 1):
        print(str(i) + ": " + GAMES[i]['title'])

    print("-------------------------------")
    export_games_list


def pull_record():
    with open("./data/vr-games.json", "r") as f:
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
        "MetaStoreOnly": [], # only in the Meta store
        "bothStores": [], # in both Steam and Meta stores
        "free": [], # free games
        "<20": [], # cost $20 or less
        "2player": [], # 2-player games only
        "UpTo4": [], # supports up to 4 or more players
        "UpTo8": [], # supports up to 8 or more players
        "VR-Optional": [], # VR support and flatscreen
        "VR-Required": [], # VR ONLY (no flatscreen support)
        "coop": [], # has cooperative gameplay
        "comp": [], # has competitive gameplay
        "Tabletop": [], # tabletop type games
        "Seated": [] # supports or is exclusively seated gameplay
    }

    for i in range(1, len(GAMES) + 1):
        game = GAMES[i]
        # check stores
        if game["inMetaStore"] and game["inSteamStore"]:
            CATEGORIES["bothStores"].append(i)
        elif game["inMetaStore"]:
            CATEGORIES["MetaStoreOnly"].append(i)
        # check price
        if ((game['MetaPrice'] != None and game['MetaPrice'] == 0) or (game['SteamPrice'] != None and game['SteamPrice'] == 0)):
            CATEGORIES['free'].append(i)
        if ((game['MetaPrice'] != None and game['MetaPrice'] <= 20.00) or (game['SteamPrice'] != None and game['SteamPrice'] <= 20.00)):
            CATEGORIES['<20'].append(i)
        # check player count
        if game['Gathering-Max'] >= 2:
            CATEGORIES['2player'].append(i)
        if game['Gathering-Max'] >= 4:
            CATEGORIES['UpTo4'].append(i)
        if game['Gathering-Max'] >= 8:
            CATEGORIES['UpTo8'].append(i)
        # check if vr optional
        if game['VR-Optional']:
            CATEGORIES['VR-Optional'].append(i)
        else:
            CATEGORIES['VR-Required'].append(i)
        # check coop vs. comp
        if game['coop']:
            CATEGORIES['coop'].append(i)
        if game['comp']:
            CATEGORIES['comp'].append(i)
        # check if tabletop
        if game['Tabletop']:
            CATEGORIES['Tabletop'].append(i)
        # check if seated
        if game['Seated']:
            CATEGORIES['Seated'].append(i)

    return CATEGORIES


def save():
    # save games.json
    with open("./data/vr-games.json", "w") as f:
        json.dump(GAMES, f, indent=4)

    # save games_by_category.json
    categories = save_by_category()
    with open("./data/vr-games-by-category.json", "w") as f:
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