document.addEventListener('DOMContentLoaded', () => {
    const mainContainer = document.querySelector(".page-main");
    const quizList = document.getElementById("quiz-list");
    const searchInput = document.getElementById("search");

    const SUBJECTS = {
        "ALGEBRA 1": "algebra1regents-june2025.json",
        "GEOMETRY": "geometryregents-june2025.json",
        "ALGEBRA 2": "algebra2regents-june2025.json"
    };

    // Create buttons
    Object.entries(SUBJECTS).forEach(([subjectName, fileName]) => {
        const btn = document.createElement("button");
        btn.textContent = subjectName;
        btn.classList.add("quiz-button");
        btn.style.width = "100%";
        btn.onclick = () => loadQuiz(fileName);
        mainContainer.appendChild(btn);
    });

    searchInput.addEventListener('input', () => {
        const term = searchInput.value.toLowerCase();
        mainContainer.querySelectorAll("button.quiz-button").forEach(btn => {
            btn.style.display = btn.textContent.toLowerCase().includes(term) ? "block" : "none";
        });
    });


    async function loadQuiz(fileName) {
        try {
            const res = await fetch(`/static/regents/${fileName}`);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            renderQuiz(data, fileName);
        } catch (err) {
            console.error(err);
            alert(`Failed to load ${fileName}`);
        }
    }

    function renderQuiz(data, fileName) {
        quizList.innerHTML = "";
        const a = document.createElement("a");
        a.href = `/quizzes/${fileName.replace('.json','')}`;
        // try a.href = `${window.location.origin}/quizzes/${fileName.replace('.json','')}`; instead on gh codespaces.
        a.textContent = data.exam;
        quizList.appendChild(a);
    }
});