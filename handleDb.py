from tinydb import TinyDB
db = TinyDB('db.json')

def save_score(score,hit_accuracy,date):
    db.insert({"score":score, "accuracy": int(hit_accuracy*100), "date": str(date.day)+"."+str(date.month)+"."+str(date.year)})

def search_all():
    return db.all()
    

