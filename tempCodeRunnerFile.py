cred = credentials.Certificate("servicekey.json")
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://stuattend-default-rtdb.firebaseio.com/"}
)