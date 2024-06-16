$(document).ready(function() {
    $('.reply-btn').click(function(event) {
        event.preventDefault();
        console.log('Reply button clicked'); // Check if this message appears in the console
        $(this).closest('.comment').find('.reply-form').toggle();
    });
});

// document.addEventListener("DOMContentLoaded", function() {
//     document.querySelectorAll('.comment').forEach(function(comment) {
//         let level = comment.getAttribute('data-level');
//         if (level !== null) {
//             comment.style.marginLeft = `${level * 20}px`;
//         }
//     });
// });