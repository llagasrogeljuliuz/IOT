document.addEventListener('DOMContentLoaded', () => {
    const clientID = "webclient_" + parseInt(Math.random() * 1000000, 10);

    const client = new Paho.Client(
        "5c1e782f3c924391aecb3b50c3b6316d.s1.eu.hivemq.cloud",
        Number(8884),
        "/mqtt",
        clientID
    );

    client.connect({
        useSSL: true,
        userName: "user1",
        password: "User1234",
        onSuccess: onConnect,
        onFailure: (err) => console.error("Connection failed", err)
    });

    client.onMessageArrived = function (message) {
        console.log("Received:", message.payloadString);
    };

    function onConnect() {
        console.log("Connected!");
        client.subscribe("my/test/topic");
    }

    // Device button logic
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
                message = `Off`;
            } else {
                indicator.classList.add('on');
                status.textContent = 'Device is ON';
                button.textContent = 'Turn OFF';
                message = `On`;
            }

            client.send("my/test/topic", message);
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
            }, 500);
        }, 3000);
    }
});

