import json
import sys

valid_ys = ['y','Y','yes','Yes','YES']
valid_ns = ['n','N','no','No','NO']

GAMENIGHT = {
    "size": None, # should become an integer representing the number of people attending gamenight (including the host)
    "location": None, # should become an integer; 0 = online, 1 = in person
    "VR-Games": False, # whether or not VR games are on the list
    "FlatscreenGames": False, # whether or not flatscreen games are on the list
    "EveryoneVR": False, # whether or not EVERYONE is playing VR
    "EveryoneMeta": False, # whether or not EVERYONE has a Meta headset
    "Tabletop": None, # integer; 0 = only tabletop games, 1 = any games, 2 = NO tabletop games
    "Seated": None,  # integer; 0 = only seated games, 1 = any games, 2 = NO seated games
    "Coop": False, # if the group is interested in cooperative games
    "Comp": False, # if the group is interested in competitive games
    "FreeOnly": False # if the group is limited to only free games (negligible if in person)
}

# VR GAME INFORMATION KEY
'''
    VR Game categories:
        - "MetaStoreOnly" only in the Meta store (not on Steam or PCVR)
        - "bothStores" in both Steam and Meta stores
        - "free" free games
        - "<20" cost $20 or less
        - "2player" 2-player+ games
        - "UpTo8" supports up to 8 or more players
        - "VR-Optional" VR support and flatscreen
        - "VR-Required" VR ONLY (no flatscreen support)
        - "coop" has cooperative gameplay
        - "comp" has competitive gameplay

    VR Game attributes:
        - "title"
        - "inMetaStore": inMetaStore
        - "inSteamStore": inSteamStore
        - "ownedOn": which store I own it on
        - "VR-Optional": VR Optional (supports flatscreen)
        - "Gathering-Min": Smallest player group supported
        - "Gathering-Max": Largest player group supported
        - "Seated": Seated gameplay
        - "Tabletop": Tabletop type game
        - "MetaPrice": price in the Meta store
        - "SteamPrice": price in the Steam store
        - "coop" has cooperative gameplay
        - "comp" has competitive gameplay
'''

# NINTENDO GAME INFORMATION KEY
'''
    Nintendo Game categories:
        - "free" free games
        - "<20" cost $20 or less
        - "local2player" local 2-player+ games
        - "online2player" online 2-player+ games
        - "localUpTo4" supports up to 4 players locally
        - "OnlineUpTo4" supports up to 4 or more players online
        - "OnlineUpTo8" supports up to 8 or more players online
        - "coop" has cooperative gameplay
        - "comp" has competitive gameplay

    Nintendo Game attributes:
        - "title": title
        - "Price": Price
        - "Player-Min": smallest player group supported
        - "Local-Max": largest local (same device) player group supported
        - "Online-Max": largest online player group supported
        - "Coop": has cooperative gameplay
        - "Comp": has competitive gameplay
'''


def pull_Nintendo_records():
    with open("./data/nintendo-games.json", "r") as f:
        N_GAMES = json.load(f)

    with open("./data/nintendo-games-by-category.json", "r") as f:
        N_CATEGORIES = json.load(f)

    return N_CATEGORIES, N_GAMES


def pull_VR_records():
    with open("./data/vr-games.json", "r") as f:
        VR_GAMES = json.load(f)

    with open("./data/vr-games-by-category.json", "r") as f:
        VR_CATEGORIES = json.load(f)

    return VR_CATEGORIES, VR_GAMES


def pull_records():
    VR_CATEGORIES, VR_GAMES = pull_VR_records()
    N_CATEGORIES, N_GAMES = pull_Nintendo_records()

    return VR_CATEGORIES, N_CATEGORIES, VR_GAMES, N_GAMES


def query_size():
    # ask for size of game night party
    valid_response = False
    while (not valid_response):
        print("\nHow big is game night? (Enter one number representing the # of friends + yourself)")
        response = input()
        if response == 'q' or response == 'Q':
            return False # quit and return false to indicate such
        else:
            try:
                response = int(response)
                valid_response = True
                GAMENIGHT['size'] = response
                return True
            except ValueError:
                print("Invalid response. Please try again.\n\n")


def query_location():
    # ask if gamenight is in person or online
    valid_response = False
    while (not valid_response):
        print("\nIs game night:\n(1) Online\n(2) In Person")
        response = input()
        if response == '1':
            GAMENIGHT['location'] = 0
            valid_response = True
            return True
        elif response == '2':
            GAMENIGHT['location'] = 1
            valid_response = True
            return True
        elif response == 'q' or response == 'Q':
            return False
        else:
            print("Invalid response. Please try again.\n\n")


def query_gameplay_type():
    # ask if interested in coop
    valid_response = False
    while (not valid_response):
        print("\nIs the group interested in cooperative gameplay? (y/n)")
        response = input()
        if response in valid_ys:
            GAMENIGHT['Coop'] = True
            valid_response = True
        elif response in valid_ns:
            GAMENIGHT['Coop'] = False
            valid_response = True
        elif response == 'q' or response == 'Q':
            return False
        else:
            print("Invalid response. Please try again.\n\n")

    # ask if interested in comp
    valid_response = False
    while (not valid_response):
        print("\nIs the group interested in competitive gameplay? (y/n)")
        response = input()
        if response in valid_ys:
            GAMENIGHT['Comp'] = True
            valid_response = True
        elif response in valid_ns:
            GAMENIGHT['Comp'] = False
            valid_response = True
        elif response == 'q' or response == 'Q':
            break
        else:
            print("Invalid response. Please try again.\n\n")

    return True


def query_free_only():
    # ask if limited to free games
    valid_response = False
    while (not valid_response):
        print("\nIs the group limited to only free games? (y/n)")
        response = input()
        if response in valid_ys:
            GAMENIGHT['FreeOnly'] = True
            valid_response = True
            return True
        elif response in valid_ns:
            GAMENIGHT['FreeOnly'] = False
            valid_response = True
            return True
        elif response == 'q' or response == 'Q':
            return False
        else:
            print("Invalid response. Please try again.\n\n")


def query_VR_interest():
    # ask if interested in VR games
    valid_response = False
    while (not valid_response):
        print("\nIs the group interested in VR or VR optional games? (y/n)")
        response = input()
        if response in valid_ys:
            GAMENIGHT['VR-Games'] = True
            valid_response = True
        elif response in valid_ns:
            GAMENIGHT['VR-Games'] = False
            valid_response = True
        elif response == 'q' or response == 'Q':
            return False
        else:
            print("Invalid response. Please try again.\n\n")

    if GAMENIGHT['VR-Games']:
        # ask if everyone has a VR headset
        valid_response = False
        while (not valid_response):
            print("\nDoes everyone in the group have a VR headset? (y/n)")
            response = input()
            if response in valid_ys:
                GAMENIGHT['EveryoneVR'] = True
                valid_response = True
            elif response in valid_ns:
                GAMENIGHT['EveryoneVR'] = False
                valid_response = True
            elif response == 'q' or response == 'Q':
                return False
            else:
                print("Invalid response. Please try again.\n\n")
        
        if GAMENIGHT['EveryoneVR']:
            # ask if everyone has a Meta headset
            valid_response = False
            while (not valid_response):
                print("\nDoes everyone in the group have a Meta headset? (y/n)")
                response = input()
                if response in valid_ys:
                    GAMENIGHT['EveryoneMeta'] = True
                    valid_response = True
                elif response in valid_ns:
                    GAMENIGHT['EveryoneMeta'] = False
                    valid_response = True
                elif response == 'q' or response == 'Q':
                    return False
                else:
                    print("Invalid response. Please try again.\n\n")
        
        # ask if interested in tabletop games
        valid_response = False
        while (not valid_response):
            print("\nIs the group interested in VR games that are:\n(1) exlusively tabletop games\n(2) tabletop games and others\n(3) no tabletop games")
            response = input()
            if response == '1':
                GAMENIGHT['Tabletop'] = 0
                valid_response = True
            elif response == '2':
                GAMENIGHT['Tabletop'] = 1
                valid_response = True
            elif response == '3':
                GAMENIGHT['Tabletop'] = 2
                valid_response = True
            elif response == 'q' or response == 'Q':
                return False
            else:
                print("Invalid response. Please try again.\n\n")

        # ask if interested in seated games
        valid_response = False
        while (not valid_response):
            print("\nIs the group interested in VR games that are:\n(1) only games WITH seated gameplay\n(2) any games with or without seated gameplay\n(3) only games WITHOUT seated gameplay")
            response = input()
            if response == '1':
                GAMENIGHT['Seated'] = 0
                valid_response = True
            elif response == '2':
                GAMENIGHT['Seated'] = 1
                valid_response = True
            elif response == '3':
                GAMENIGHT['Seated'] = 2
                valid_response = True
            elif response == 'q' or response == 'Q':
                return False
            else:
                print("Invalid response. Please try again.\n\n")

    return True


def query_flatscreen_interest():
    # ask if interested in flatscreen (non-VR) games
    valid_response = False
    while (not valid_response):
        print("\nIs the group interested in flatscreen (non-VR) games? (y/n)")
        response = input()
        if response in valid_ys:
            GAMENIGHT['FlatscreenGames'] = True
            valid_response = True
        elif response in valid_ns:
            GAMENIGHT['FlatscreenGames'] = False
            valid_response = True
        elif response == 'q' or response == 'Q':
            return False
        else:
            print("Invalid response. Please try again.\n\n")

    return True


def compute_recommendations(VR_CATEGORIES, N_CATEGORIES, VR_GAMES, N_GAMES):
    # analyze VR games
    vr_game_ids = set()
    if GAMENIGHT['VR-Games']:
        if GAMENIGHT['EveryoneVR']: # include VR required games
            vg1 = set(VR_CATEGORIES['VR-Optional'])
            vg2 = set(VR_CATEGORIES['VR-Required'])
            vr_game_ids = vr_game_ids.union((vg1.union(vg2)))
        else: # exclude VR required games
            vg = set(VR_CATEGORIES['VR-Optional'])
            vr_game_ids = vr_game_ids.union(vg)
        
        # if not everyone has a Meta headset
        if not GAMENIGHT['EveryoneMeta']: # exclude games that are only in the Meta store
            vg = set(VR_CATEGORIES['MetaStoreOnly'])
            vr_game_ids = vr_game_ids - vg

        # tabletop limit
        tvg = set(VR_CATEGORIES['Tabletop'])
        if GAMENIGHT['Tabletop'] == 0: # if only interested in tabletop vr games
            vr_game_ids = vr_game_ids.intersection(tvg)
        elif GAMENIGHT['Tabletop'] == 2: # if only interested in NON tabletop vr games
            vr_game_ids = vr_game_ids - tvg
        # otherwise no need to change (no narrowing)

        # seated limit
        svg = set(VR_CATEGORIES['Seated'])
        if GAMENIGHT['Seated'] == 0: # if only interested in SEATED vr games
            vr_game_ids = vr_game_ids.intersection(svg)
        elif GAMENIGHT['Seated'] == 2: # if only interested in NON seated vr games
            vr_game_ids = vr_game_ids - svg
        # otherwise no need to change (no narrowing)

        # limit by size
        if GAMENIGHT['size'] >= 8:
            bvg = set(VR_CATEGORIES['UpTo8'])
            vr_game_ids = vr_game_ids.intersection(bvg)
        elif GAMENIGHT['size'] >= 4:
            mvg = set(VR_CATEGORIES['UpTo4'])
            vr_game_ids = vr_game_ids.intersection(mvg)
        elif GAMENIGHT['size'] >= 2:
            svg = set(VR_CATEGORIES['2player'])
            vr_game_ids = vr_game_ids.intersection(svg)

        # limit by coop
        if not GAMENIGHT['Coop']: # no interest in coop games -> remove them
            coop = set(VR_CATEGORIES['coop'])
            vr_game_ids = vr_game_ids - coop
            if GAMENIGHT['Comp']: # but interested in competitive games! make sure to add any back that are also coop
                comp = set(VR_CATEGORIES['comp'])
                double = comp.intersection(coop)
                vr_game_ids.union(double)
        
        # limit by comp
        if not GAMENIGHT['Comp']: # no interest in comp games -> remove them
            comp = set(VR_CATEGORIES['comp'])
            vr_game_ids = vr_game_ids - comp
            if GAMENIGHT['Coop']: # but interested in cooperative games! make sure to add any back that are also comp
                coop = set(VR_CATEGORIES['coop'])
                double = comp.intersection(coop)
                vr_game_ids.union(double)

        # limit by free
        if GAMENIGHT['FreeOnly']:
            fovg = set(VR_CATEGORIES['free'])
            vr_game_ids = vr_game_ids.intersection(fovg)

    # analyze flatscreen games
    flat_game_ids = set()
    if GAMENIGHT['FlatscreenGames']:
        # limit by coop
        if GAMENIGHT['Coop']: # interested in coop games. add them.
            coop = set(N_CATEGORIES['coop'])
            flat_game_ids = flat_game_ids.union(coop)

        # limit by comp
        if GAMENIGHT['Comp']: # interested in comp games. add them.
            comp = set(N_CATEGORIES['comp'])
            flat_game_ids = flat_game_ids.union(comp)

        # limit by size & location
        if GAMENIGHT['location'] == 0: # online
            if GAMENIGHT['size'] >= 8:
                bfg = set(N_CATEGORIES['OnlineUpTo8'])
                flat_game_ids = flat_game_ids.intersection(bfg)
            elif GAMENIGHT['size'] >= 4:
                mfg = set(N_CATEGORIES['OnlineUpTo4'])
                flat_game_ids = flat_game_ids.intersection(mfg)
            elif GAMENIGHT['size'] >= 2:
                sfg = set(N_CATEGORIES['online2player'])
                flat_game_ids = flat_game_ids.intersection(sfg)

            # limit by free if online
            if GAMENIGHT['FreeOnly']:
                ffg = set(N_CATEGORIES['free'])
                flat_game_ids = flat_game_ids.intersection(ffg)
        else: # in person
            if GAMENIGHT['size'] >= 4:
                bfg = set(N_CATEGORIES['localUpTo4'])
                flat_game_ids = flat_game_ids.intersection(bfg)
            elif GAMENIGHT['size'] >= 2:
                sfg = set(N_CATEGORIES['local2player'])
                flat_game_ids = flat_game_ids.intersection(sfg)

    # output results
    display_recommendations(VR_CATEGORIES, N_CATEGORIES, VR_GAMES, N_GAMES, vr_game_ids, flat_game_ids)


def display_recommendations(VR_CATEGORIES, N_CATEGORIES, VR_GAMES, N_GAMES, vr_game_ids, flat_game_ids):
    if vr_game_ids != set():
        print("\n=======================\nVR GAME RECOMMENDATIONS\n=======================")
        index = 1
        for vr_game in vr_game_ids:
            game = VR_GAMES[str(vr_game)]
            print("(" + str(index) + ") " + game['title'] + ":")
            print("    - Max. Group Size: " + str(game['Gathering-Max']))
            if game['VR-Optional']:
                print("    - VR Optional")
            else:
                print("    - VR Required")

            aboutStr = ""
            if game['Seated'] and game['Tabletop']:
                aboutStr = "    - Seated, Tabletop"
            elif game['Seated']:
                aboutStr = "    - Seated"
            elif game['Tabletop']:
                aboutStr = "    - Tabletop"
            
            typeStr = ""

            if game['coop'] and game['comp']:
                typeStr = "cooperative and competitive gameplay"
            elif game['coop']:
                typeStr = "cooperative gameplay"
            elif game['comp']:
                typeStr = "competitive gameplay"

            if aboutStr == "":
                aboutStr = "    - " + typeStr
            else:
                aboutStr = aboutStr + " | " + typeStr

            print(aboutStr)

            if game['MetaPrice'] != None:
                print("    - Price in Meta Store: " + str(game['MetaPrice']))
            if game['SteamPrice'] != None:
                print("    - Price in Steam Store: " + str(game['SteamPrice']))

            index += 1
            print("")
    
    if flat_game_ids != set():
        print("\n=============================\nNINTENDO GAME RECOMMENDATIONS\n=============================")
        index = 1
        for flat_game in flat_game_ids:
            game = N_GAMES[str(flat_game)]
            print("(" + str(index) + ") " + game['title'] + ":")
            print("    - Max. Local Group Size: " + str(game['Local-Max']))
            print("    - Max. Online Group Size: " + str(game['Online-Max']))

            typeStr = ""

            if game['Coop'] and game['Comp']:
                typeStr = "cooperative and competitive gameplay"
            elif game['Coop']:
                typeStr = "cooperative gameplay"
            elif game['Comp']:
                typeStr = "competitive gameplay"

            print("    - " + typeStr)
            print("    - Price in Nintendo Store: " + str(game['Price']))
            print("")

            index += 1


    if vr_game_ids == set() and flat_game_ids == set():
        print("\n--------------------------\nThere are no recommendations to display!\n")
        print("Your library might be too small or your requirements might be too strict.")
        print("\n--------------------------")
    else:
        print("\n\nWould you like to export these results to a file? (y/n)")
        if input() in valid_ys:
            output_recommendations_to_file(VR_CATEGORIES, N_CATEGORIES, VR_GAMES, N_GAMES, vr_game_ids, flat_game_ids)

    
def output_recommendations_to_file(VR_CATEGORIES, N_CATEGORIES, VR_GAMES, N_GAMES, vr_game_ids, flat_game_ids):
    print("\n\nExporting...")
    filepath = identify_next_file_name()

    original_stdout = sys.stdout
    f = open(filepath, "w")
    sys.stdout = f
    
    if vr_game_ids != set():
        print("\n=======================\nVR GAME RECOMMENDATIONS\n=======================")
        index = 1
        for vr_game in vr_game_ids:
            game = VR_GAMES[str(vr_game)]
            print("(" + str(index) + ") " + game['title'] + ":")
            print("    - Max. Group Size: " + str(game['Gathering-Max']))
            if game['VR-Optional']:
                print("    - VR Optional")
            else:
                print("    - VR Required")

            aboutStr = ""
            if game['Seated'] and game['Tabletop']:
                aboutStr = "    - Seated, Tabletop"
            elif game['Seated']:
                aboutStr = "    - Seated"
            elif game['Tabletop']:
                aboutStr = "    - Tabletop"
            
            typeStr = ""

            if game['coop'] and game['comp']:
                typeStr = "cooperative and competitive gameplay"
            elif game['coop']:
                typeStr = "cooperative gameplay"
            elif game['comp']:
                typeStr = "competitive gameplay"

            if aboutStr == "":
                aboutStr = "    - " + typeStr
            else:
                aboutStr = aboutStr + " | " + typeStr

            print(aboutStr)

            if game['MetaPrice'] != None:
                print("    - Price in Meta Store: " + str(game['MetaPrice']))
            if game['SteamPrice'] != None:
                print("    - Price in Steam Store: " + str(game['SteamPrice']))

            index += 1
            print("")

    if flat_game_ids != set():
        print("\n=============================\nNINTENDO GAME RECOMMENDATIONS\n=============================")
        index = 1
        for flat_game in flat_game_ids:
            game = N_GAMES[str(flat_game)]
            print("(" + str(index) + ") " + game['title'] + ":")
            print("    - Max. Local Group Size: " + str(game['Local-Max']))
            print("    - Max. Online Group Size: " + str(game['Online-Max']))

            typeStr = ""

            if game['Coop'] and game['Comp']:
                typeStr = "cooperative and competitive gameplay"
            elif game['Coop']:
                typeStr = "cooperative gameplay"
            elif game['Comp']:
                typeStr = "competitive gameplay"

            print("    - " + typeStr)
            print("    - Price in Nintendo Store: " + str(game['Price']))
            print("")

            index += 1

    f.close()
    sys.stdout = original_stdout

    print("\nYour results have been exported to " + filepath)


def identify_next_file_name():
    index = 0
    found = False

    while (not found):
        filepath = "./exports/output" + str(index) + ".txt"
        try:
            with open(filepath, "r") as file:
                content = file.read()
            index += 1
        except FileNotFoundError:
            found = True

    return filepath


if __name__ == "__main__":
    # pull existing games records
    VR_CATEGORIES, N_CATEGORIES, VR_GAMES, N_GAMES = pull_records()

    # greet and prompt user for action
    print("Welcome to your personal Gamenight game picker application!")
    print("If you would like to edit any information about your games libraries, please run the corresponding application. This application is only for helping you narrow down which games to consider for your upcoming game night!")

    print("\n----------------------------------\nYou can press 'Q' at any time to quit.")

    if query_size():
        if query_location():
            if query_gameplay_type():
                if query_VR_interest():
                    if query_flatscreen_interest():
                        if GAMENIGHT['location'] == 0:
                            if query_free_only():
                                compute_recommendations(VR_CATEGORIES, N_CATEGORIES, VR_GAMES, N_GAMES)
                        else:
                            compute_recommendations(VR_CATEGORIES, N_CATEGORIES, VR_GAMES, N_GAMES)