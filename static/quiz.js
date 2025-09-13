let quiz = null;
let i = 0;
let userScore = 0;
let units = [];
let unitCorrect = [];
buttonPressed = false;
document.addEventListener('DOMContentLoaded', () => {
  const pathParts = window.location.pathname.split('/');
  const quizName = pathParts[pathParts.length - 1];

  const fileName = quizName
    .toLowerCase()
    .replace(/ /g, '')
    .replace(/%20/g, '')
    + '.json';

  const filePath = `/static/regents/${fileName}`;


  fetch(filePath)
    .then(res => {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.json();
    })
    .then(data => {
      quiz = data;
      showQuiz();
    })
    .catch(err => {
      console.error('Failed to load quiz JSON:', err);
      alert('Failed to load quiz JSON. Check file name and path.');
    });

});

function showQuiz() {
    if (!quiz || i >= quiz.questions.length) {
        const res = {
            totalQuestions: quiz.questions.length,
            questionsCorrect: userScore,
            subject: quiz.subject_id,
            exam: quiz.exam,
            units: units,
            unitsCorrect: unitCorrect
        };
        fetch('/results', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(res)
        })
        .then(response => response.json())
          .then(response => {
              if (response.status === 'ok') {
                    window.location.href = `/results`;
                } else {
                    alert('Error saving results.');
              }
        })
    }

    let title = document.querySelector('.title');
    if (title){
        title.textContent = quiz.exam;
    }

    let questionDiv = document.querySelector('.quiz-question');
    if (questionDiv) {
        questionDiv.textContent = quiz.questions[i].question;
    }
    let optionsDiv = document.querySelector('.quiz-options');
    optionsDiv.innerHTML = '';
    units[quiz.questions[i].unit] = (units[quiz.questions[i].unit] || 0) + 1;
    buttonPressed = false;

    const choices = quiz.questions[i].choices;
    Object.entries(choices).forEach(([key, value]) => {
        const button = document.createElement('button');
        button.textContent = value
        button.classList.add('quiz-option');
        button.onclick = () => {
            if (!buttonPressed) {
                answerCheck(key, button);
                buttonPressed = true;
            }

        }
        optionsDiv.appendChild(button);
    });

    let imageDiv = document.querySelector('.quiz-stimulus');
    imageDiv.innerHTML = '';
    if (quiz.questions[i].image) {
        const img = document.createElement('img');
        img.src = `/static/regents/${quiz.questions[i].image}`;
        img.alt = 'Question Image';
        img.style.maxWidth = '100%';
        imageDiv.appendChild(img);
    }

}
function answerCheck(selected, button) {
    const footer = document.querySelector('.quiz-footer');
    const explanation = document.createElement('h5')
    explanation.textContent = quiz.questions[i].explanation;
    explanation.classList.add('quiz-explanation');
    const next = document.createElement('button');
    if (i === quiz.questions.length - 1 ){
        next.textContent = 'Finish';
    } else{
        next.textContent = 'Next';
    }

    next.classList.add('quiz-submit');
    const correct = quiz.questions[i].answer;

    if (selected === correct) {
        button.classList.replace('quiz-option', 'right');
        unitCorrect[quiz.questions[i].unit] = (unitCorrect[quiz.questions[i].unit] || 0) + 1;
        userScore++;
    } else {
        button.classList.replace('quiz-option', 'wrong');
    }
    if (!footer.querySelector('.quiz-submit')) {
        footer.appendChild(explanation);
        footer.appendChild(next);
    }

    const optionDiv = document.querySelector('.quiz-options');
    const buttons = optionDiv.querySelectorAll('.quiz-option');
    buttons.forEach(btn => {
        if (btn.textContent === quiz.questions[i].choices[correct]) {
            btn.classList.replace('quiz-option', 'right');
        }
    })


    next.addEventListener('click', () => {
        explanation.remove();
        next.remove();
        i++;
        showQuiz();
    });
}