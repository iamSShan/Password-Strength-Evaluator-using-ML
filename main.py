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


def check_probability_strength(prediction, probability):
    """
    Return whether password in weak, average or strong, based on prediction
    """
    if(prediction == 0):
        return "Weak Password"
        return templates.TemplateResponse("index.html", context={"request": request, "strength": ""})

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
    return render_template("index.html")


@app.route('/', methods=['POST'])
def check_password():
    # Get password from front end
    password = request.form["password"]
    # If no password is entered
    if not password:
        print("Please enter password")

    # Load models
    vectorizer = pickle.load(open("vectorizer.pkl", 'rb'))
    model = pickle.load(open("xgb_classifier.pkl", 'rb'))

    # Now we have to convert password into list else it will give error while we are trying to predict
    password = [password]

    # Predicted for the given password
    password_vector = vectorizer.transform(password)
    prediction = model.predict(password_vector)

    # predict_proba gives probability estimates
    probability = model.predict_proba(password_vector)
    
    password_strength = check_probability_strength(prediction, probability)
    # Return response
    print(password_strength)
    return render_template("index.html", data={"strength": password_strength})
    

if __name__ == "__main__":
    app.run(debug=True) 