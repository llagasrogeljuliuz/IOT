document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.toggle-button');
  const notification = document.getElementById('notification');
  let notificationTimeout;

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      const deviceBox = button.parentElement;
      const indicator = deviceBox.querySelector('.indicator');
      const status = deviceBox.querySelector('.status');
      const deviceName = deviceBox.getAttribute('data-device');
      const isOn = indicator.classList.contains('on');

      const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      let message = '';

      if (isOn) {
        indicator.classList.remove('on');
        status.textContent = 'Device is OFF';
        button.textContent = 'Turn ON';
        message = `❌ ${deviceName} turned OFF at ${currentTime}`;
      } else {
        indicator.classList.add('on');
        status.textContent = 'Device is ON';
        button.textContent = 'Turn OFF';
        message = `✅ ${deviceName} turned ON at ${currentTime}`;
      }

      showNotification(message);
    });
  });

  function showNotification(message) {
    notification.textContent = message;
    notification.classList.remove('hidden');
    notification.classList.add('show');

    clearTimeout(notificationTimeout);
    notificationTimeout = setTimeout(() => {
      notification.classList.remove('show');
      setTimeout(() => {
        notification.classList.add('hidden');
      }, 500); // Delay to allow slide-out animation
    }, 3000);
  }
});
