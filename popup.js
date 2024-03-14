document.addEventListener('DOMContentLoaded', function() {
    const summarizeBtn = document.getElementById('summarizeBtn');
    const summaryDiv = document.getElementById('summary');

    summarizeBtn.addEventListener('click', function() {
        // Notify contentScript.js to execute summary generation
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            const activeTab = tabs[0];
            chrome.tabs.sendMessage(activeTab.id, {action: 'generate'});
        });
    });

    // Listen for the result from contentScript.js
    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
        if (message.action === 'result') {
            // Display the summary in the div element
            summaryDiv.innerText = message.summary;
        }
    });
});
