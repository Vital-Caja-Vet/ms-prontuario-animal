import os
from dotenv import load_dotenv
from app import app, db
from utils.db_utils import create_database_if_not_exists

if __name__ == '__main__':
    load_dotenv()

    create_database_if_not_exists()
    with app.app_context():
        db.create_all()

    port = int(os.getenv('PORT'))

    debug = os.getenv('FLASK_DEBUG', 'True').lower() in ('1', 'true', 't', 'yes', 'y')
    app.run(host='0.0.0.0', port=port, debug=debug)
