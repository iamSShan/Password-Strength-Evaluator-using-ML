import pickle
from flask import Flask, render_template, request

app = Flask(__name__)


# We have to declare this function as it was used while creating vectorizer
# So if this function is not defined loading vectorizer will give error
def words_to_char(password):
    characters = []
    for letter in password:
        characters.append(letter)
    return characters


import __main__
__main__.words_to_char = words_to_char


def check_probability_strength(prediction, probability):
    """
    Return whether password in weak, average or strong, based on probability
    """
    if(prediction == 0):
        return "Weak Password"

    elif(prediction == 1):
        return "Average Password"

    elif prediction == 2:
        if probability[0][2] > 0.90:
            return "Very Strong Password"
        else:
            return "Strong Password"


@app.route('/')
def home():
    """
    Render home page
    """
    return render_template("index.html", data={})


@app.route('/', methods=['POST'])
def check_password():
    """
    When user enters password to check its strength
    """

    # Get password from front end
    password = request.form["password"]

    # If no password is entered display message to enter password first
    if not password:
        return render_template("index.html", data={"strength": "Please enter the password first"})

    # print("Model loading")
    # Load models
    vectorizer = pickle.load(open("vectorizer.pkl", 'rb'))
    model = pickle.load(open("xgb_classifier.pkl", 'rb'))
    # print("Model loaded")

    # Now we have to convert password into list else it will give error while we are trying to predict using models
    password = [password]

    # Predict for the given password
    password_vector = vectorizer.transform(password)
    prediction = model.predict(password_vector)

    # predict_proba gives probability estimates
    probability = model.predict_proba(password_vector)
    password_strength = check_probability_strength(prediction, probability)

    # Return response
    # print(password_strength)
    return render_template("index.html", data={"strength": password_strength})
    

if __name__ == "__main__":
    app.run(debug=True)
