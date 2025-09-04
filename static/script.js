document.addEventListener('DOMContentLoaded', () => {
  const SUBJECTS = {
    algebra1: "algebra1regents-june2025.json",
    geometry: "geometryregents-june2025.json"
  };

  const mainContainer = document.querySelector(".page-main");
  const quizList = document.getElementById("quiz-list");
  const searchInput = document.getElementById("search");

  Object.keys(SUBJECTS).forEach(subject => {
    const btn = document.createElement("button");
    btn.textContent = subject.replace(/\d+/g," $&").toUpperCase();
    btn.classList.add("quiz-button");
    btn.style.width = "100%";

    // Only load the list of quizzes, do NOT try to render questions
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
    quizList.innerHTML = "";
    const a = document.createElement("a");
    a.href = `/quizzes/${data.exam}`;
    a.textContent = data.exam;
    quizList.appendChild(a);
  }
});

