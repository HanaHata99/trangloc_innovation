function sendHeight() {
    const height = document.body.scrollHeight;
    console.log(`Gửi chiều cao của figure frame: ${height}`)
    window.parent.postMessage({ frameHeight: height }, "*");
}

// Gửi sau khi React render xong
setTimeout(sendHeight, 3000);
setTimeout(sendHeight, 5000);

// Gửi lại khi resize
window.addEventListener('resize', sendHeight);
