import json

'''
THIS APPLICATION COMPLETELY WIPES YOUR GAME LIBRARIES.
USE WITH CAUTION.
'''

if __name__ == "__main__":
    # wipe vr-games.json
    with open("./data/vr-games.json", "w") as f:
        json.dump({}, f, indent=4)

    # wipe vr-games_by_category.json
    with open("./data/vr-games-by-category.json", "w") as f:
        json.dump({}, f, indent=4)

    # wipe nintendo-games.json
    with open("./data/nintendo-games.json", "w") as f:
        json.dump({}, f, indent=4)

    # wipe nintendo-games-by-category.json
    with open("./data/nintendo-games-by-category.json", "w") as f:
        json.dump({}, f, indent=4)