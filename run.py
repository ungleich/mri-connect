DEV_HOST = '0.0.0.0'
DEV_PORT = 5000

if __name__ == '__main__':

    import os
    from app import app, db, models, views

    db.create_all()

    app.run(host=DEV_HOST, port=DEV_PORT)
