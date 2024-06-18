$(document).ready(function() {
    $('.reply-btn').click(function(event) {
        event.preventDefault();
        console.log('Reply button clicked'); // Check if this message appears in the console
        $(this).closest('.comment').find('.reply-form').toggle();
    });
});

document.getElementById('commentForm').addEventListener('submit', function(event) {
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const fileType = file.type;
        const fileSize = file.size;
        const maxSize = 100 * 1024; // 100 KB
        const allowedImageTypes = ['image/jpeg', 'image/gif', 'image/png'];
        const allowedTextType = 'text/plain';

        if (allowedImageTypes.includes(fileType)) {
            const img = new Image();
            img.src = URL.createObjectURL(file);
            img.onload = function() {
                const width = img.width;
                const height = img.height;
                if (width > 320 || height > 240) {
                    const ratio = Math.min(320 / width, 240 / height);
                    const newWidth = width * ratio;
                    const newHeight = height * ratio;
                    const canvas = document.createElement('canvas');
                    canvas.width = newWidth;
                    canvas.height = newHeight;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, newWidth, newHeight);
                    canvas.toBlob(function(blob) {
                        const newFile = new File([blob], file.name, {type: file.type});
                        const dataTransfer = new DataTransfer();
                        dataTransfer.items.add(newFile);
                        fileInput.files = dataTransfer.files;
                        document.getElementById('commentForm').submit();
                    }, file.type);
                    event.preventDefault();
                }
            };
        } else if (fileType === allowedTextType) {
            if (fileSize > maxSize) {
                alert('Text file must be less than 100KB.');
                event.preventDefault();
            }
        } else {
            alert('Invalid file type.');
            event.preventDefault();
        }
    }
});