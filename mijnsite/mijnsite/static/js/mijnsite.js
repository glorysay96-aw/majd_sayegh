
const questions = document.querySelectorAll(".question");
let current = 0;
let score = 0;

function answer(button, choice) {

    let question = button.parentElement;

    if (question.dataset.done === "1")
        return;

    question.dataset.done = "1";

    let correct = question.dataset.correct;

    let feedback = question.querySelector(".feedback");

    if (choice === correct) {

        score++;

        feedback.innerHTML = "✅ Goed!";
        feedback.style.color = "green";

    } else {

        feedback.innerHTML = "❌ Fout!";
        feedback.style.color = "red";

    }

    let explanation = question.querySelector(".explanation");

    if (explanation)
        explanation.style.display = "block";

    setTimeout(function () {

        question.style.display = "none";

        current++;

        if (current < questions.length) {

            questions[current].style.display = "block";

        } else {

            document.getElementById("quiz").innerHTML =
                "<h2>Klaar!</h2>" +
                "<h3>Score: " + score + " / " + questions.length + "</h3>";

        }

    }, 2000);

}