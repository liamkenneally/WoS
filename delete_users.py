from db_calls.crud import delete_user_by_id



game_ids = [106904909,104971875,105217694,106708654,105315689,107036259,108772920, 108134024]

for game_id in game_ids:
    delete_user_by_id(game_id)