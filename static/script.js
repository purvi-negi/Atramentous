document.addEventListener('DOMContentLoaded', () => {
    const habitabilityForm = document.getElementById('habitability-form');
    const resultContainer = document.getElementById('result-container');
    const statusText = document.getElementById('status-text');
    const probabilityFill = document.getElementById('probability-fill');
    const probabilityText = document.getElementById('probability-text');
    const submitBtn = document.getElementById('submit-btn');

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Offset for fixed navbar
                    behavior: 'smooth'
                });
            }
        });
    });

    // Form Submission
    habitabilityForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // UI Feedback
        submitBtn.disabled = true;
        submitBtn.textContent = 'Analyzing...';
        
        // Collect form data
        const formData = new FormData(habitabilityForm);
        const data = Object.fromEntries(formData.entries());

        // Prepare request body (convert types if necessary)
        const payload = {
            radius: parseFloat(data.radius),
            temperature: parseFloat(data.temperature),
            distance: parseFloat(data.distance),
            period: parseFloat(data.period),
            star_type: data.star_type
        };

        try {
            // Mock API call (for development if backend is not ready)
            // Replace with actual fetch to /predict
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            displayResult(result);

        } catch (error) {
            console.error('Error:', error);
            
            // For demonstration purposes, if the API fails (e.g. not connected), 
            // I'll simulate a result so the user can see the UI working.
            // REMOVE THIS IN PRODUCTION
            simulateResult();
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Check Habitability';
        }
    });

    function displayResult(result) {
        // result should have: { is_habitable: boolean, probability: number }
        resultContainer.classList.remove('hidden');
        
        // Scroll to results
        window.scrollTo({
            top: resultContainer.offsetTop - 150,
            behavior: 'smooth'
        });

        // Update status text
        if (result.is_habitable) {
            statusText.textContent = 'Habitable';
            statusText.className = 'status-text status-habitable';
        } else {
            statusText.textContent = 'Not Habitable';
            statusText.className = 'status-text status-not-habitable';
        }

        // Update probability visual
        const prob = Math.round(result.probability * 100);
        probabilityFill.style.width = '0%'; // Reset for animation
        
        setTimeout(() => {
            probabilityFill.style.width = `${prob}%`;
            probabilityText.textContent = `${prob}% Probability`;
        }, 100);
    }

    // This is just to show the UI works without a real backend
    function simulateResult() {
        const isHabitable = Math.random() > 0.5;
        const probability = Math.random();
        displayResult({ is_habitable: isHabitable, probability: probability });
    }
});
// Load visualization charts
fetch('/visualize')
.then(response => response.json())
.then(data => {
    if (data.chart1) {
        Plotly.newPlot('chart1', data.chart1.data, data.chart1.layout);
    }
    if (data.chart2) {
        Plotly.newPlot('chart2', data.chart2.data, data.chart2.layout);
    }
})
.catch(error => console.error('Error loading visualizations:', error));
