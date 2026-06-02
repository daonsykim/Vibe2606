document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contactForm');
    const result = document.getElementById('formResult');

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const name = form.elements['name'].value.trim();
            const email = form.elements['email'].value.trim();
            const message = form.elements['message'].value.trim();

            if (!name || !email || !message) {
                result.textContent = '모든 항목을 입력해주세요.';
                result.style.color = '#d32f2f';
                return;
            }

            result.textContent = `감사합니다, ${name}님! 메시지가 성공적으로 전송되었습니다.`;
            result.style.color = '#004d7a';
            form.reset();
        });
    }
});
