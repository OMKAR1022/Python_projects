import pyrebase

config = {
    "apiKey": "AIzaSyABcNZGpLCqSjsDPfZfmkI4tnf-2KkF3fY",
    "authDomain": "blind-403815.firebaseapp.com",
    "projectId": "blind-403815",
    "databaseURl": "https://blind-403815-default-rtdb.firebaseio.com",
    "storageBucket": "blind-403815.appspot.com",
    "messagingSenderId": "435559928243",
    "appId": "1:435559928243:web:782a8efaa45293ce2bfbc6",
    "measurementId": "G-X392F7KPPB"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
data = {"age": 20, "Name": "omakr"}

db.push(data)
