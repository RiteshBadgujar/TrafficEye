from django.http import JsonResponse
from pymongo import MongoClient
from collections import Counter
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["trafficeye_db"]

violations = db["violations"]


def chart_data(request):

    monthly = [0] * 12

    paid = 0
    pending = 0

    categories = Counter()

    yearly = Counter()

    for violation in violations.find():

        # Date
        date = violation.get("date")

        if date:

            try:

                d = datetime.strptime(date, "%Y-%m-%d")

                monthly[d.month - 1] += 1

                yearly[str(d.year)] += 1

            except:

                pass

        # Payment Status

        if violation.get("status") == "Paid":

            paid += 1

        else:

            pending += 1

        # Violation Type

        categories[
            violation.get(
                "violation_type",
                "Other"
            )
        ] += 1

    return JsonResponse({

        "monthly": monthly,

        "paid": paid,

        "pending": pending,

        "categories": {

            "labels": list(categories.keys()),

            "values": list(categories.values())

        },

        "yearly": {

            "labels": list(yearly.keys()),

            "values": list(yearly.values())

        }

    })