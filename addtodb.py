import firebase_admin
from firebase_admin import credentials,db

cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://stuattend-default-rtdb.firebaseio.com/"}
)

ref=db.reference('student')


data = {
    "27033":
        {
            "name": "Anjalika Agarwal",
            "major": "ECE",
            "starting_year": 2021,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
        "321654":
        {
            "name": "Murtaza hassan",
            "major": "Robotics",
            "starting_year": 2008,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
         "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}


for key,values in data.items():
    ref.child(key).set(values)