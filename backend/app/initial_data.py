from app.crud.user import create_supuser, get_user_by_email
from app.schemas.user import UserCreate
from app.db.session import SessionLocal


def init_admin() -> None:
    db = SessionLocal()
    user = get_user_by_email(db, email="admin@sicsogt.com")
    if not user:
        create_supuser(
            db,
            UserCreate(
                email="admin@sicsogt.com",
                im = 1,
                username= "admin",
                is_active=True,
                is_superuser=True,
            ),
        )
        

if __name__ == "__main__":
    print("Creating superuser admin@sicsogt.com")
    init_admin()
    print("Superuser created")
