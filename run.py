from app import app, db
from utils.db_utils import create_database_if_not_exists

if __name__ == '__main__':
    create_database_if_not_exists()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8001, debug=True)
