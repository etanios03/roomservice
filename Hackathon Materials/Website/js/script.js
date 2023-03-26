// Get the date and time input fields
const dateInput = document.getElementById('myDate');
const timeInput = document.getElementById('myTime');

// Create a new Date object
const currentDate = new Date();

// Set the value of the date and time input fields
dateInput.value = currentDate.toISOString().slice(0,10);
timeInput.value = currentDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

function animateTyping(id, duration, delay) {
    const text = document.getElementById(id).textContent;
    document.getElementById(id).textContent = "";
    const delayInMillis = delay * 1000;
    const durationInMillis = duration * 1000;
    const characters = text.split("");
    const characterCount = characters.length;
    const delayBetweenCharacters = durationInMillis / characterCount;
  
    setTimeout(() => {
      let i = 0;
      const interval = setInterval(() => {
        document.getElementById(id).textContent += characters[i];
        i++;
        if (i >= characterCount) {
          clearInterval(interval);
        }
      }, delayBetweenCharacters);
    }, delayInMillis);
  }

  animateTyping("typing-text", 2, 0);
  animateTyping("typing-text-1", 0.3, 2.5);
  animateTyping("typing-text-2", 0.5, 3.2);

  function scrollDown() {
    window.scrollTo({
      top: 500,
      behavior: "smooth"
    });
  }