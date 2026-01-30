
const urlParams = new URLSearchParams(window.location.search);
let token = urlParams.get('token');

if (token) {
    // Save to local storage for persistence on refresh
    localStorage.setItem('supabase_token', token);
    // Clean URL
    if (window.history.replaceState) {
        const url = new URL(window.location);
        url.searchParams.delete('token');
        window.history.replaceState({}, '', url);
    }
} else {
    // Try to get from local storage
    token = localStorage.getItem('supabase_token');
}

const sendToken = () => {
    // Wait for Chainlit to be ready
    if (window.chainlit && window.chainlit.sendWindowMessage) {
        if (token) {
            console.log("Sending token to backend...");
            window.chainlit.sendWindowMessage({
                type: "SUPABASE_TOKEN",
                token: token
            });
        } else {
            console.log("No token found.");
            window.chainlit.sendWindowMessage({
                type: "NO_TOKEN"
            });
        }
    } else {
        setTimeout(sendToken, 500);
    }
};

sendToken();
