from flask import Flask, render_template, request
import requests
import mysql.connector

# Replace sensitive information with placeholders
mydb = mysql.connector.connect(
    host="YOUR_DB_HOST",
    user="YOUR_DB_USER",
    passwd="YOUR_DB_PASSWORD",
    database="YOUR_DB_NAME"
)
mycursor = mydb.cursor()

app = Flask(__name__)

# Replace sensitive information with placeholders
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"

messages = ["Hii Doctor"]
responses = ["Hii!, This is your Doctor."]
med = []
price = []
items = []
total = 0

# Query to fetch medicines
l = "SELECT * FROM medicines;"
mycursor.execute(l)
for i in mycursor:
    med.append(i)

@app.route('/chatinterface', methods=['GET', 'POST'])
def chatinterface():
    l = "INSERT INTO hos_ai.chat (sender, message) VALUES ('', '')"
    mycursor.execute(l)
    mydb.commit()
    l = "SELECT id FROM hos_ai.chat"
    mycursor.execute(l)
    for i in mycursor:
        a = (i)
    id = (a[0])
    return render_template('chat.html', id=id, response=responses, user=messages)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    id = request.form['id']
    message = request.form['user']
    if messages[-1] != message:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        requests.get(url).json()
        messages.append(message)
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    a = (requests.get(url).json())
    try:
        response = (a['result'][-1]['message']['text'])
        if responses[-1] != response:
            responses.append(response)
    except:
        response = "Waiting for message...."
    l = "UPDATE Hos_AI.chat SET sender = CONCAT(sender, %s), message = CONCAT(message, %s) WHERE id = %s"
    mycursor.execute(l, ("->" + str(response), "->" + str(message), str(id)))
    mydb.commit()
    return render_template('chat.html', response=responses, user=messages)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    name = request.form['name']
    message = "Your Doctor: " + str(name)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()
    return render_template('appointment.html')

@app.route('/selectdoctor', methods=['GET', 'POST'])
def selectdoctor():
    name = request.form['name']
    email = request.form['mobile']
    date = request.form['date']
    hospital = request.form['hospital']
    if hospital == "Hospital A":
        lst = ["Dr. Smith", "Dr. Johnson", "Dr. Patel", "Dr. Nguyen", "Dr. García"]
    elif hospital == "Hospital B":
        lst = ["Dr. Kim", "Dr. Müller", "Dr. Chen", "Dr. Khan", "Dr. Lopez"]
    elif hospital == "Hospital C":
        lst = ["Dr. Martinez", "Dr. Lee", "Dr. González", "Dr. Brown", "Dr. Wilson"]
    elif hospital == "Hospital D":
        lst = ["Dr. Anderson", "Dr. Taylor", "Dr. Thomas", "Dr. Rodriguez", "Dr. Lewis"]
    elif hospital == "Hospital E":
        lst = ["Dr. Harris", "Dr. Robinson", "Dr. Clark", "Dr. Walker", "Dr. Hall"]
    message1 = "Appointment Booked Successfully."
    message2 = "Your Details are Listed below:"
    message3 = "Name: " + str(name)
    message4 = "Email: " + email
    message5 = "Date: " + date
    message = message1 + "\n" + message2 + "\n" + message3 + "\n" + message4 + "\n" + message5 + "\n"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()
    return render_template('doctorselection.html', lst=lst)

@app.route('/ambulance', methods=['GET', 'POST'])
def ambulance():
    message = "Ambulance Booked Successfully."
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()
    message = "The ambulance is on its way."
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()
    return render_template('confirm.html')

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    price = 0
    items = ["NO ITEM ADDED TO CART"]
    return render_template('shop.html', med=med, items=items, total=price)

@app.route('/addtocart', methods=['GET', 'POST'])
def addtocart():
    id = request.form['item']
    l = "SELECT * FROM medicines WHERE id=%s"
    mycursor.execute(l, (id,))
    for i in mycursor:
        items.append(i[1])
        price.append(i[3])
        total = sum(price)
    return render_template('shop.html', med=med, items=items, total=total)

@app.route('/order', methods=['GET', 'POST'])
def order():
    message = "Medicine have been ordered successfully."
    message = message + '\n' + "The medicine on its way are:\n\n"
    message = message + '\n'.join(items)
    message = message + "\n\nPrice: Rs. " + str(sum(price))
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()    
    return render_template('medicine.html')

@app.route('/')
def index():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(debug=True)
