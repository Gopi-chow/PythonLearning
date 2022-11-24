import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from database import myMongoDB
from database import MONGODB_EXIST
from datetime import timedelta
from datetime import datetime
import getpass


def test_database_connection():
    # Setup filter and projections to get pervious day data for user
    day_before = datetime.utcnow() - timedelta(days=1)
    user = getpass.getuser()
    proj = {'_id' : 0}
    filt={'jobid': {'$exists': True}, 'timestamp' : { '$gt' : day_before}}
    assert user != ''
    filt['author'] = str(user)
    # Check if the user python has pymongo 
    assert MONGODB_EXIST == True
    # Test the database functions
    with myMongoDB() as db:
        assert db.col_name == 'burst_2022'
        assert db.db_name == 'Siv_burstwebapp'
        assert db.client_addr != None
        assert db.client != None
        assert db.check_collection() == True
        assert db.print_filtered_data(filt, proj) == True
