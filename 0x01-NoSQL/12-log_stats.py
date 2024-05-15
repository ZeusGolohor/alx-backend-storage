#!/usr/bin/env python3
"""
Write a Python script that provides some stats
about Nginx logs stored in MongoDB:
"""


def analyze_nginx_logs(mongo_uri="mongodb://localhost:27017",
        database_name="logs", collection_name="nginx"):
    """
    Write a Python script that provides some stats about
    Nginx logs stored in MongoDB:
    """
    mongo_client = pymongo.MongoClient(mongo_uri)
    database = mongo_client[database_name]
    logs = database[collection_name]
    total_logs = logs.count_documents({})
    method_counts = {
            "GET": logs.count_documents({"method": "GET"}),
            "POST": logs.count_documents({"method": "POST"}),
            "PUT": logs.count_documents({"method": "PUT"}),
            "PATCH": logs.count_documents({"method": "PATCH"}),
            "DELETE": logs.count_documents({"method": "DELETE"}),
            }
    status_checks = logs.count_documents({"method": "GET", "path": "/status"})
    print(total_logs, "logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(status_checks, "status check")


if __name__ == "__main__":
    analyze_nginx_logs()
