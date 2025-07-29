from backend.database.database import SessionLocal
from backend.models.user import User

def test_get_all_user_ids():
    db = SessionLocal()
    ids = db.query(User.id).all()
    db.close()
    ids_list = [id[0] for id in ids]
    print("IDs en base :", ids_list)
    assert len(ids_list) > 0  # vérifie qu'il y a au moins un utilisateur
