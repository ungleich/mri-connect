if __name__ == '__main__':

    from app import app, db
    from app.models import *

    p = Person(
        source_id = 1,
        last_name = "Test"
    )
    db.session.add(p)
    db.session.commit()
