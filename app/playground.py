from datetime import date
from app.db import SessionLocal
from app.services.player_service import create_player, get_player, delete_player, update_player_weight, get_all_players


session = SessionLocal()


first_name = "Vale"
last_name = "Denisov"
birth_date = date(2000, 6, 4)
team_id = 2
position = "forward"
weight = 90.5

first_name = "Ivan"
last_name = "Ivanov"
birth_date = date(2008, 5, 1)
team_id = 1
position = "forward"
weight = 60.5

first_name = "Vale"
last_name = "Denisov"
birth_date = date(2000, 6, 4)
team_id = 2
position = "forward"
weight = 90.5


player = create_player(session, first_name, last_name,
                       birth_date, team_id, position, weight)

if player:
    print(f"Player {player.first_name} {player.last_name} was created")

found_player = get_player(session, first_name, last_name, birth_date, team_id,)

if found_player:
    print(
        f"Player {found_player.first_name} {found_player.last_name} was founded")
else:
    print("Player not found")

deleted_player = delete_player(
    session, first_name, last_name, birth_date, team_id,)


if player:
    print(
        f"Player {deleted_player.first_name} {deleted_player.last_name} was deleted")
else:
    print("Player not found")

updated_player = update_player_weight(
    session, first_name, last_name, birth_date, team_id, weight)

if updated_player:
    print(
        f"Weight of player {updated_player.first_name} {updated_player.last_name} was updated to {weight}")

else:
    print("Cannot update weight: player not found")


list_players = get_all_players(session)
print(list_players)
