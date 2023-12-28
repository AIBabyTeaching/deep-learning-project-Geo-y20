function predictCharacter() {
  const fileInput = document.getElementById('imageUpload');
  const imagePreview = document.getElementById('imagePreview');
  const predictionResult = document.getElementById('predictionResult');

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  const url = '/predict'; // Assuming there's only one prediction endpoint

  fetch(url, {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      updatePredictionUI(predictionResult, data);
      displayImagePreview(imagePreview, file);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function updatePredictionUI(element, prediction) {
  element.textContent = `Prediction: ${prediction.prediction}`;
}

function displayImagePreview(element, file) {
  const reader = new FileReader();

  reader.onload = function (event) {
    const img = new Image();
    img.src = event.target.result;

    element.innerHTML = '';
    element.appendChild(img);
  };

  if (file) {
    reader.readAsDataURL(file);
  }
}

// Event listener for scrolling to sections
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();

    const targetId = this.getAttribute('href').substring(1);
    const targetElement = document.getElementById(targetId);
    if (targetElement) {
      targetElement.scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});
