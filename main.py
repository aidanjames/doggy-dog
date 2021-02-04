from flask import Flask, render_template, request
from dog_manager import DogManager

app = Flask(__name__)

dog_manager = DogManager()
current_dog = None


@app.route('/', methods=["GET", "POST"])
def home():
    global current_dog
    dog = dog_manager.new_dog()
    current_dog = dog
    selections = dog_manager.random_breeds(2, dog.breed)
    return render_template('index.html', dog=dog, breed_selections=selections)


@app.route('/guess')
def guess():
    user_guess = request.args.get("guess")
    correct = False
    if user_guess == current_dog.breed:
        correct = True
    return render_template('guess.html', current_dog=current_dog, is_correct=correct, guessed=user_guess)


if __name__ == "__main__":
    app.run()
