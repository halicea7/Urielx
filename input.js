document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('myForm');
    const inputBox = document.getElementById('user-input');
    const container = document.getElementById('input-container');
  
    // Prevent the form from submitting (and thus refreshing the page)
    form.addEventListener('submit', function(event) {
      event.preventDefault();
    });
  
    // Use the keydown event on the input box to trigger on Enter
    inputBox.addEventListener('keydown', function(event) {
      if (event.key === 'Enter') {
        event.preventDefault();  // Prevent default behavior (this is a safeguard)
  
        const topic = inputBox.value.trim();
        if (topic === "") return;  // Do nothing if empty
  
        console.log("Submitting topic:", topic);
  
        // Add the "active" class if not already present
        if (!container.classList.contains('active')) {
          container.classList.add('active');
          console.log("Added active class - rainbow border should appear for 60 seconds.");
          // Keep the rainbow border active for 1 minute (60000 ms)
          setTimeout(() => {
            container.classList.remove('active');
            console.log("Removed active class after 60 seconds.");
          }, 60000);
        }
  
        // Send the input to the Flask backend via a POST request
        fetch('http://127.0.0.1:5000/run_research', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ topic: topic })
        })
        .then(response => response.json())
        .then(data => {
          console.log("Response from backend:", data);
          // Clear the input box after submission
          inputBox.value = "";
        })
        .catch(error => {
          console.error("Error:", error);
          //container.classList.remove('active');
          if (container.classList.contains('active')){
            console.log("Keeping the animation active despite error")
          }
        });
      }
    });
  });
  