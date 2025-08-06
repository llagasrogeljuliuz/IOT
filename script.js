document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.toggle-button');

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      const deviceBox = button.parentElement;
      const indicator = deviceBox.querySelector('.indicator');
      const status = deviceBox.querySelector('.status');

      const isOn = indicator.classList.contains('on');

      if (isOn) {
        indicator.classList.remove('on');
        status.textContent = 'Device is OFF';
        button.textContent = 'Turn ON';
      } else {
        indicator.classList.add('on');
        status.textContent = 'Device is ON';
        button.textContent = 'Turn OFF';
      }
    });
  });
});
