#!/usr/bin/env python3

MONGODB_EXIST = True
try:
    import pymongo
except ImportError:
    MONGODB_EXIST = False
    # Requires the PyMongo package.
    # https://api.mongodb.com/python/current
from datetime import timedelta
import datetime
from os import getenv
from update import read_json
import getpass


class myMongoDB(object):
    """MongoDB Connection context manager class"""

    def __init__(self, uri=None, db="Siv_burstwebapp", col="burst_2022"):
        self.db_name = db
        self.col_name = col
        uri_file = "/home/xppc/burst/latest_burst/db_file/db_meta.json"
        if uri:
            self.client_addr = uri
        else:
            data = read_json(uri_file)
            try:
                self.client_addr = data["uri"]
            except (KeyError, TypeError):
                print(
                    f"ERROR: db_meta.json missing uri! "
                    f"contact burst_script_team@xilinx.com with this error"
                )
                self.client_addr = None

    def __enter__(self):
        if (not MONGODB_EXIST) or (not self.client_addr):
            self.client = None
        else:
            try:
                self.client = pymongo.MongoClient(self.client_addr)
            except pymongo.errors.PyMongoError:
                self.client = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.client.close()
        except AttributeError:
            print(
                f"Database client not initilized: {self.client_addr}\n"
                f"PyMongo package / db_meta file missing"
            )
            return True
        if exc_type == pymongo.errors.PyMongoError:
            print(f"Database connection error: {self.db_name}:{self.col_name}")
            return True

    def check_collection(self):
        if self.db_name not in self.client.list_database_names():
            print(f"ERROR: Database name error: {self.db_name} does not exist!")
            return False
        collections_list = self.client[self.db_name].list_collection_names()
        if self.col_name not in collections_list:
            print(
                f"ERROR: Collection name error: {self.col_name} "
                f"does not exist in database {self.db_name}!"
            )
            return False
        return True

    def print_filtered_data(self, filter, projection, print_en=True):
        mycol = self.client[self.db_name][self.col_name]
        result = mycol.find(filter=filter, projection=projection)
        if print_en:
            print(f"Print results for filter: {filter}, proj: {projection}")
            for item in result:
                print(item)
            return True
        else:
            return result

    def upload_data(self, data):
        if not self.check_collection():
            return False
        mycol = self.client[self.db_name][self.col_name]
        if len(data) == 0:
            return False
        elif len(data) == 1:
            result = mycol.insert_one(data[0])
        elif len(data) > 1:
            result = mycol.insert_many(data)
        try:
            if result.acknowledged:
                print(f"Results uploaded to database {self.db_name}:{self.col_name}")
                return True
            else:
                print(f"ERROR: {self.db_name}:{self.col_name} upload, failed to Ack")
                return False
        except AttributeError:
            print(f"ERROR: {self.db_name}:{self.col_name} upload, AttributeError")
            return False
        return False


if __name__ == "__main__":
    try:
        if not MONGODB_EXIST:
            print("WARN: PyMongo package not found!")
            exit(0)
        # Setup filter and projections to get pervious day data for user
        day_before = datetime.datetime.utcnow() - timedelta(days=1)
        end_day = datetime.datetime.utcnow()
        user = getpass.getuser()
        proj = {"_id": 0}
        filt = {"$and":[ {"timestamp":{"$gt": day_before}}, {"timestamp":{"$lte": end_day}}], "jobid": {"$exists": True}}
        if user != "":
            filt["author"] = "burst-test"
        # Connect to datababse and display the results
        with myMongoDB() as db:
            if not db.check_collection():
                exit(0)
            data = db.print_filtered_data(filt, proj, False)
            run_time, count = 0, 0
            for run in data:
                    run_time +=  int(run["run_time"])
                    count +=1
                    last_run = run
            run_hrs = run_time/3600
            print(f"run time : {round(run_hrs, 1)} hours from {count} runs, average run time {round(run_hrs/count)} hrs")
            print(f"last run: {last_run}")
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        exit(0)
