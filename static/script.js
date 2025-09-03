document.addEventListener('DOMContentLoaded', () => {

  const SUBJECTS = {
    algebra1: "algebra1june2025.json",
    geometry: "geometryjune2025.json"
  };

  const mainContainer = document.querySelector(".page-main");
  const quizList = document.getElementById("quiz-list");
  const searchInput = document.getElementById("search");


  Object.keys(SUBJECTS).forEach(subject => {
    const btn = document.createElement("button");
    btn.textContent = subject.replace(/\d+/g," $&").toUpperCase();
    btn.classList = "quiz-button";
    btn.style.width = "100%";
    btn.onclick = () => loadQuiz(SUBJECTS[subject]);
    mainContainer.appendChild(btn);
  });

  searchInput.addEventListener('input', () => {
    const term = searchInput.value.toLowerCase();
    mainContainer.querySelectorAll("button").forEach(btn => {
      btn.style.display = btn.textContent.toLowerCase().includes(term) ? 'block' : 'none';
    });
  });

  async function loadQuiz(fileName) {
    try {
      const res = await fetch(`/static/regents/${fileName}`);
      if (!res.ok) throw new Error("HTTP " + res.status);
      const data = await res.json();
      renderQuiz(data);
    } catch (err) {
      console.error(err);
      alert(`Failed to load ${fileName}`);
    }
  }

function renderQuiz(data) {
    const quizList = document.getElementById("quiz-list");
    quizList.innerHTML = ""; // clear old content
    const a = document.createElement("a");
    a.href = `/quizzes/${data.exam}`;
    const li = document.createElement("li");
    li.textContent = data.exam;
    a.appendChild(li);
    quizList.appendChild(a);
}
});


function loadQuiz(filename) {
    fetch(filename)
        .then(response => response.json())
        .then(data => {
            const quizContainer = document.getElementById('quiz-container');
            quizContainer.innerHTML = '';

            data.questions.forEach((question, index) => {
                const questionDiv = document.createElement('div');
                questionDiv.classList.add('question');

                const questionText = document.createElement('h3');
                questionText.textContent = `${index + 1}. ${question.question}`;
                questionDiv.appendChild(questionText);

                question.options.forEach(option => {
                    const optionLabel = document.createElement('label');
                    const optionInput = document.createElement('input');
                    optionInput.type = 'radio';
                    optionInput.name = `question${index}`;
                    optionInput.value = option;
                    optionLabel.appendChild(optionInput);
                    optionLabel.appendChild(document.createTextNode(option));
                    questionDiv.appendChild(optionLabel);
                    questionDiv.appendChild(document.createElement('br'));
                });

                quizContainer.appendChild(questionDiv);
            });

            const submitButton = document.createElement('button');
            submitButton.textContent = 'Submit';
            submitButton.onclick = () => checkAnswers(data);
            quizContainer.appendChild(submitButton);
        })
        .catch(error => console.error('Error loading quiz:', error));
}