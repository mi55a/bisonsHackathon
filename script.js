// script.js — activate API only on Send, curriculum-aware
const API  = "http://127.0.0.1:5055";   // change if you run Flask on another port
const UNIT = "u1";                      // "u1" = Unit 1, "u2" = Unit 2

const TITLES = {
  u1: "Unit 1: What is AI?",
  u2: "Unit 2: Using Basic LLMs & API Calls",
};

let lessonLoaded = false;

document.addEventListener("DOMContentLoaded", () => {
  const u = localStorage.getItem("profai_username");
  if (!u) { location.href = "login.html"; return; }
  const nameEl = document.querySelector(".learn-sidebar .username");
  if (nameEl) nameEl.textContent = `Welcome back, ${u}!`;

  document.getElementById("sendBtn").addEventListener("click", onSend);
  document.getElementById("userInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter") { e.preventDefault(); onSend(); }
  });
});

async function onSend() {
  const input = document.getElementById("userInput");
  const text  = input.value.trim();

  // First click: start the lesson (even with empty input)
  if (!lessonLoaded) {
    await startLesson(UNIT);
    lessonLoaded = true;
    if (!text) return;
  }

  // Chat
  if (!text) return;
  addMessage(text, "user");
  input.value = "";

  try {
    const res  = await fetch(`${API}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ unit: UNIT, message: text })
    });
    const data = await res.json();
    addMessage(data.reply || "…", "ai");
  } catch {
    addMessage("Can't connect to AI", "ai");
  }
}

async function startLesson(unit) {
  const topicEl  = document.querySelector(".content h1");  // [Topic Here]
  const lessonEl = document.querySelector(".content h3");  // [Lesson Text]
  try {
    const res  = await fetch(`${API}/lesson/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ unit })
    });
    const data = await res.json();
    if (topicEl)  topicEl.textContent  = data.title || TITLES[unit] || "Lesson";
    if (lessonEl) lessonEl.innerHTML = formatLesson(data.lesson || "");
    addMessage("👋 Lesson posted above. Ask me anything about it.", "ai");
  } catch {
    if (lessonEl) lessonEl.textContent = "Could not load the lesson.";
  }
}

function addMessage(text, sender) {
  const chat = document.getElementById("chatMessages");
  const el   = document.createElement("div");
  el.classList.add("message", sender); // style via CSS
  el.textContent = text;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

function formatLesson(raw) {
    // escape HTML
    const esc = (s) => s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
    const lines = (raw || "").split(/\r?\n/);

    let html = [];
    let inList = false;

    for (let line of lines) {
      line = line.trim();
      if (!line) { continue; }

      // bold text
      const withBold = esc(line).replace(/**(.+?)**/g, "<strong>$1</strong>");

      if (line.startsWith("* ")) {
        if (!inList) { html.push("<ul>"); inList = true; }
        html.push(<li>${withBold.slice(2)}</li>);
      } else {
        if (inList) { html.push("</ul>"); inList = false; }
        html.push(<p>${withBold}</p>);
      }
    }
    if (inList) html.push("</ul>");

    return html.join("");
}