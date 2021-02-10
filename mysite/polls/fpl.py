def get_player_picture(photo_id):
    photo_id = photo_id.replace(".jpg", "")
    return f"https://resources.premierleague.com/premierleague/photos/players/110x140/p{photo_id}.png"