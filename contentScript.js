console.log('Making request to:', backendUrl);


// contentScript.js
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'generate') {
        // Extract the URL of the current tab
        const videoUrl = window.location.href;

        // Make a GET HTTP request to the backend
        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Send an action message 'result' with the summary payload
                    chrome.runtime.sendMessage({action: 'result', summary: xhr.responseText});
                } else {
                    // Handle error
                    console.error('Error fetching summarized text:', xhr.statusText);
                }
            }
        };

        // Replace 'your_backend_url' with the actual URL of your backend endpoint
        const backendUrl = 'http://127.0.0.1:5000/api/summarize?youtube_url=' + encodeURIComponent(videoUrl);
        xhr.open('GET', backendUrl, true);
        xhr.send();
    }
});
