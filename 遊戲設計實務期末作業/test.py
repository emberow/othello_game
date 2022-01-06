from tkinter.constants import X
import db
import json
records = db.get_10_record()
message = ""
for record in records:
    for item in record:
        message += str(item)
        #item不是最後一筆資料時
        if item != record[-1]:
            message += ","
    if record != records[-1]:
        message += "/"
print(message)
