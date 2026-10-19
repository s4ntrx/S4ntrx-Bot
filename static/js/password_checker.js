const COMMON_PASSWORDS = new Set([
  "password", "123456", "12345678", "qwerty", "abc123", "letmein", "monkey",
  "111111", "iloveyou", "admin", "welcome", "password1", "123456789",
  "football", "dragon", "master", "login", "princess", "qwerty123",
]);

function hasSequential(pw) {
  const seqs = ["abcdefghijklmnopqrstuvwxyz", "0123456789", "qwertyuiop"];
  const lower = pw.toLowerCase();
  for (const seq of seqs) {
    for (let i = 0; i <= seq.length - 3; i++) {
      const chunk = seq.slice(i, i + 3);
      if (lower.includes(chunk) || lower.includes(chunk.split("").reverse().join(""))) {
        return true;
      }
    }
  }
  return false;
}

function hasRepetition(pw) {
  return /(.)\1\1/.test(pw);
}

function analyzePassword(pw) {
  const weaknesses = [];
  let score = 0;

  if (pw.length >= 16) score += 3;
  else if (pw.length >= 12) score += 2;
  else if (pw.length >= 8) score += 1;
  else weaknesses.push("Too short — aim for at least 12 characters, ideally 16+.");

  const hasLower = /[a-z]/.test(pw);
  const hasUpper = /[A-Z]/.test(pw);
  const hasDigit = /[0-9]/.test(pw);
  const hasSymbol = /[^A-Za-z0-9]/.test(pw);
  const varietyCount = [hasLower, hasUpper, hasDigit, hasSymbol].filter(Boolean).length;
  score += varietyCount;
  if (varietyCount < 3) weaknesses.push("Uses limited character variety — mix upper/lowercase, numbers, and symbols.");

  if (hasRepetition(pw)) {
    weaknesses.push("Contains repeated characters (e.g. 'aaa').");
    score -= 1;
  }
  if (hasSequential(pw)) {
    weaknesses.push("Contains a sequential pattern (e.g. 'abc', '123', 'qwe').");
    score -= 1;
  }
  if (COMMON_PASSWORDS.has(pw.toLowerCase())) {
    weaknesses.push("This is one of the most commonly used passwords — extremely easy to guess.");
    score = 0;
  }

  score = Math.max(0, Math.min(score, 7));

  let rating, level;
  if (pw.length === 0) { rating = "—"; level = 0; }
  else if (score <= 2) { rating = "Weak"; level = 1; }
  else if (score <= 4) { rating = "Fair"; level = 2; }
  else if (score <= 6) { rating = "Strong"; level = 3; }
  else { rating = "Very strong"; level = 4; }

  return { rating, level, score, maxScore: 7, weaknesses };
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("pwInput");
  const toggle = document.getElementById("pwToggle");
  const bar = document.getElementById("pwBar");
  const ratingLabel = document.getElementById("pwRating");
  const weaknessList = document.getElementById("pwWeaknesses");

  const addNote = (text, ok) => {
    const li = document.createElement("li");
    li.innerHTML = '<svg class="i"><use href="' + (ok ? "#i-check" : "#i-alert") + '"/></svg>';
    const span = document.createElement("span");
    span.textContent = text;
    li.appendChild(span);
    weaknessList.appendChild(li);
  };

  input.addEventListener("input", () => {
    const result = analyzePassword(input.value);
    bar.dataset.level = result.level;
    ratingLabel.textContent = result.rating;
    weaknessList.className = "flags";
    weaknessList.innerHTML = "";
    if (input.value.length > 0 && result.weaknesses.length === 0) {
      weaknessList.className = "flags ok";
      addNote("No common weaknesses detected.", true);
    } else {
      result.weaknesses.forEach((w) => addNote(w, false));
    }
  });

  toggle.addEventListener("click", () => {
    input.type = input.type === "password" ? "text" : "password";
    toggle.textContent = input.type === "password" ? "Show" : "Hide";
  });
});
