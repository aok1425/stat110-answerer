from flask import Flask, render_template_string
from backend import AnswerScreenshotter

TEMP_FILEPATH = 'selected_solutions_blitzstein_hwang_probability_2.pdf'

app = Flask(__name__)

@app.route('/<int:chapter>/<int:question>')
def show_answer(chapter, question):
    imgs = AnswerScreenshotter(TEMP_FILEPATH, chapter, question)
    snaps = imgs.make_snapshots()
    return render_template_string("""<img src="data:image/png;base64,{{ image }}"/>""", image=snaps[0])

@app.route("/")
def hello():
    return 'hi'

if __name__ == "__main__":
    app.run(debug=True)