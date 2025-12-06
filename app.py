from flask import Flask, render_template, request, session, redirect, url_for
from quiz_logic import load_questions, load_microbes, get_best_microbe_match
import string

app = Flask(__name__)
app.secret_key = "super-secret-key"  # required for sessions

questions = load_questions()
microbes = load_microbes()

traits = list(questions.keys())
all_questions = []

# Flatten questions into a list for step-by-step display
for trait, qs in questions.items():
    for question, options in qs.items():
        all_questions.append({"trait": trait, "question": question, "options": options})


@app.route("/")
def home():
    return render_template("start.html")


@app.route("/start-quiz")
def start_quiz():
    session["index"] = 0
    session["answers"] = {trait: 0 for trait in traits}
    return redirect(url_for("question"))


@app.route("/question", methods=["GET", "POST"])
def question():
    index = session.get("index", 0)
    answers = session.get("answers", {})

    if request.method == "POST":
        selected = int(request.form["answer"])
        trait = all_questions[index]["trait"]
        answers[trait] += selected

        session["answers"] = answers
        session["index"] = index + 1

        if session["index"] >= len(all_questions):
            return redirect(url_for("result"))

        return redirect(url_for("question"))

    q = all_questions[index]
    answer_options = list(string.ascii_uppercase[: len(q["options"])])

    return render_template(
        "question.html",
        question_number=index + 1,
        total=len(all_questions),
        question=q["question"],
        options=zip(answer_options, q["options"]),
    )


@app.route("/result")
def result():
    answers = session.get("answers")
    microbe, microbe_dict = get_best_microbe_match(microbes, answers)

    return render_template(
        "result.html",
        microbe=microbe,
        data=microbe_dict,
        bg_color=microbe_dict.get("color", "#6dd5ed"),  # fallback color
    )


@app.route("/preview")
def preview_microbes():
    """Preview all microbes on the result page one by one."""
    # Load microbes
    microbes = load_microbes()

    # Optionally, you can pick a microbe by query parameter ?microbe=…
    microbe_names = list(microbes.keys())
    microbe_index = int(request.args.get("index", 0)) % len(microbe_names)
    microbe = microbe_names[microbe_index]
    microbe_dict = microbes[microbe]

    # Background color or gradient
    bg_color = microbe_dict.get("color", "#ffffff")

    # Links to next/prev microbe
    next_index = (microbe_index + 1) % len(microbe_names)
    prev_index = (microbe_index - 1) % len(microbe_names)

    return render_template(
        "result.html",
        microbe=microbe,
        data=microbe_dict,
        bg_color=bg_color,
        next_url=url_for("preview_microbes", index=next_index),
        prev_url=url_for("preview_microbes", index=prev_index),
    )


if __name__ == "__main__":
    app.run(debug=True)
