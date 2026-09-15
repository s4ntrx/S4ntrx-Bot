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

  let rating, ratingClass;
  if (pw.length === 0) {
    rating = "—"; ratingClass = "secondary";
  } else if (score <= 2) {
    rating = "Weak"; ratingClass = "danger";
  } else if (score <= 4) {
    rating = "Fair"; ratingClass = "warning";
  } else if (score <= 6) {
    rating = "Strong"; ratingClass = "info";
  } else {
    rating = "Very Strong"; ratingClass = "success";
  }

  return { rating, ratingClass, score, maxScore: 7, weaknesses };
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("pwInput");
  const toggle = document.getElementById("pwToggle");
  const bar = document.getElementById("pwBar");
  const ratingLabel = document.getElementById("pwRating");
  const weaknessList = document.getElementById("pwWeaknesses");

  input.addEventListener("input", () => {
    const result = analyzePassword(input.value);
    const pct = Math.round((result.score / result.maxScore) * 100);
    bar.style.width = pct + "%";
    bar.className = "progress-bar bg-" + result.ratingClass;
    ratingLabel.textContent = result.rating;
    ratingLabel.className = "badge bg-" + result.ratingClass;

    weaknessList.innerHTML = "";
    if (input.value.length > 0 && result.weaknesses.length === 0) {
      const li = document.createElement("li");
      li.className = "text-success";
      li.textContent = "No common weaknesses detected.";
      weaknessList.appendChild(li);
    } else {
      result.weaknesses.forEach((w) => {
        const li = document.createElement("li");
        li.textContent = w;
        weaknessList.appendChild(li);
      });
    }
  });

  toggle.addEventListener("click", () => {
    input.type = input.type === "password" ? "text" : "password";
    toggle.textContent = input.type === "password" ? "Show" : "Hide";
  });
});
