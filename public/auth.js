// public/auth.js
console.log("[auth.js] loaded");

function initAuth() {
  if (!window.chainlit) {
    setTimeout(initAuth, 100);
    return;
  }

  const token = localStorage.getItem("supabase_token");

  if (!token) {
    console.log("[auth.js] no token → load login.js");

    const s = document.createElement("script");
    s.src = "/login.js";
    document.body.appendChild(s);

    window.chainlit.sendWindowMessage({ type: "NO_TOKEN" });
    return;
  }

  console.log("[auth.js] token found → send to backend");

  window.chainlit.sendWindowMessage({
    type: "SUPABASE_TOKEN",
    token,
  });
}

initAuth();
