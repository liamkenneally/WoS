from models.user import User
from config import session



def add_user(userID, user, furnace, state):
    exists = bool(session.query(User).filter_by(id=userID).limit(1).first())
    if exists: 
        print(f'{userID}, : {user} exists in the DB')
        return "User exists in DB"
    else:
        add_user = User()
        add_user.id = userID
        add_user.username = user
        add_user.furnace = furnace
        add_user.state = state
        session.add(add_user)
        session.commit()
        print(f'{userID}, : {user} added to the DB')
        return "User added to DB"

def get_users():
    return User.query.count()

def get_all_users():
    print(User.query.all())
    return User.query.all()

def get_all_ids(): 
    return [id[0] for id in User.query.with_entities(User.id).all()]

# WIP 
def update_furnace(userID, new_furnacelvl):
    furnace_lvl = User.query.filter(User.id == userID).limit(1).first()
    new_furnace = new_furnacelvl
    furnace_lvl.furnace = new_furnace
    session.commit()
    return f'Furnace lvl updated to {new_furnace}'


def delete_user_by_id(user_id):
    # Fetch the user by id
    user = session.query(User).get(user_id)
    if user:
        # Delete the user
        session.delete(user)
        session.commit()
        print(" ")
        print("============================= DELETED =================")
        print(f'{user} deleted from the DB')
        print("============================= DELETED =================")
        print(" ")
        return f"User with id {user_id} has been deleted."
    else:
        return f"User with id {user_id} does not exist."

if __name__ == "__main__":
    user_id_to_delete = input("Enter the user ID to delete: ")
    try:
        user_id_to_delete = int(user_id_to_delete)
        delete_user_by_id(user_id_to_delete)
    except ValueError:
        print("Please enter a valid integer ID.")