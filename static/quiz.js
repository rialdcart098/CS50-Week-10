let quiz = null;

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
      console.log('Quiz JSON loaded:', data);
      quiz = data;
      showQuiz();
    })
    .catch(err => {
      console.error('Failed to load quiz JSON:', err);
      alert('Failed to load quiz JSON. Check file name and path.');
    });

});

function showQuiz() {
    let quizTitle = document.getElementsByClassName('title');
    if (quizTitle.length > 0) {
        quizTitle[0].textContent = quiz.exam;
    }
    let question = document.getElementsByClassName('quiz-question');
    if (question.length > 0) {
        question[0].textContent = quiz.questions[1].question;
    }
    let imageDiv = document.getElementsByClassName('quiz-stimulus');
    if (imageDiv.length > 0 && quiz.questions[1].image) {
        let img = document.createElement('img');
        img.src = `/static/regents/${quiz.questions[1].image}`;
        img.alt = 'Question Image';
        imageDiv[0].appendChild(img);
    }
}