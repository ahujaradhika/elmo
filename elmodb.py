from cloudant import cloudant_iam

# Authenticate using an IAM API key
ACCOUNT_NAME = '9f18399f-0e0a-4464-9cae-afcc09328dbe-bluemix'
API_KEY = 'j7H-txptJqOJ9G1PQ01hIHZYcs2oieznEkt6qWvGQBio'
DB_NAME = 'elmo_characters'

def put_character(db, c_id, data):
    db.create_document({'_id': c_id, 'personality': ' '.join(data)})

def get_character(db, c_id):
    return db[c_id]

def get_character_id(movie, character):
    return ":".join([movie.lower(), character.lower()])

if __name__ == "__main__":

    with cloudant_iam(ACCOUNT_NAME, API_KEY, connect=True) as client:
        db = None
        dblist = client.all_dbs()
        if not DB_NAME in dblist:
            db = client.create_database(DB_NAME)
        else:
            db = client[DB_NAME]

        c_id = get_character_id("Forest Gump", "Jenny")
        data = ["Open", "bold", "very sweet"]

        put_character(db, c_id, data)
        print(get_character(db, c_id))
