(function() {
    const API_ENDPOINT = 'http://localhost:8000/api/feedback'; // Your backend endpoint
    const USER_ID = 'user123'; // From your auth system
    const REPO_URL = 'https://github.com/user/repo'; // The selected repo

    const widgetContainer = document.createElement('div');
    widgetContainer.id = 'ape-feedback-widget';
    widgetContainer.innerHTML = `
        <style>
            #ape-feedback-widget { position: fixed; bottom: 20px; right: 20px; z-index: 1000; }
            #ape-feedback-button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
            #ape-feedback-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1001; }
            #ape-feedback-form { background: white; padding: 20px; border-radius: 5px; max-width: 500px; margin: 100px auto; }
            #ape-feedback-form input, #ape-feedback-form textarea, #ape-feedback-form select { width: 100%; margin: 10px 0; padding: 8px; }
            #ape-feedback-form button { margin: 5px; padding: 10px 20px; }
        </style>
        <button id="ape-feedback-button">Feedback</button>
        <div id="ape-feedback-modal">
            <div id="ape-feedback-form">
                <h3>Submit Feedback</h3>
                <input type="text" id="ape-name" placeholder="Your Name" required>
                <input type="email" id="ape-email" placeholder="Your Email" required>
                <select id="ape-type">
                    <option value="bug">Bug Report</option>
                    <option value="feature">Feature Request</option>
                    <option value="improvement">Improvement</option>
                </select>
                <textarea id="ape-message" placeholder="Describe the issue or suggestion..." rows="5" required></textarea>
                <button id="ape-submit">Submit</button>
                <button id="ape-cancel">Cancel</button>
            </div>
        </div>
    `;
    document.body.appendChild(widgetContainer);

    // Event listeners
    const button = document.getElementById('ape-feedback-button');
    const modal = document.getElementById('ape-feedback-modal');
    const submitBtn = document.getElementById('ape-submit');
    const cancelBtn = document.getElementById('ape-cancel');

    button.onclick = () => modal.style.display = 'block';
    cancelBtn.onclick = () => modal.style.display = 'none';

    submitBtn.onclick = async () => {
        const name = document.getElementById('ape-name').value;
        const email = document.getElementById('ape-email').value;
        const feedbackType = document.getElementById('ape-type').value;
        const message = document.getElementById('ape-message').value;

        if (!name || !email || !message) {
            alert('Please fill all fields');
            return;
        }

        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: USER_ID,
                    repo_url: REPO_URL,
                    name,
                    email,
                    message,
                    feedback_type: feedbackType
                })
            });

            if (response.ok) {
                alert('Feedback submitted successfully!');
                modal.style.display = 'none';
                // Clear form
                document.getElementById('ape-name').value = '';
                document.getElementById('ape-email').value = '';
                document.getElementById('ape-message').value = '';
            } else {
                alert('Failed to submit feedback');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error submitting feedback');
        }
    };
})();