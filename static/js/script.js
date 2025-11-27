document.addEventListener('DOMContentLoaded', function () {
  // Greeting button
  const greetBtn = document.getElementById('greetBtn');
  const messageEl = document.getElementById('message');

  greetBtn.addEventListener('click', async function () {
    try {
      const response = await fetch('/api/greeting');
      const data = await response.json();
      messageEl.textContent = data.message;
      messageEl.style.animation = 'fadeIn 0.5s ease';
    } catch (error) {
      messageEl.textContent = 'Error fetching greeting';
    }
  });

  // Counter functionality
  let count = 0;
  const counterEl = document.getElementById('counter');
  const incrementBtn = document.getElementById('incrementBtn');
  const decrementBtn = document.getElementById('decrementBtn');
  const resetBtn = document.getElementById('resetBtn');

  function updateCounter() {
    counterEl.textContent = count;
    counterEl.style.transform = 'scale(1.2)';
    setTimeout(() => {
      counterEl.style.transform = 'scale(1)';
    }, 100);
  }

  incrementBtn.addEventListener('click', function () {
    count++;
    updateCounter();
  });

  decrementBtn.addEventListener('click', function () {
    count--;
    updateCounter();
  });

  resetBtn.addEventListener('click', function () {
    count = 0;
    updateCounter();
  });
});
