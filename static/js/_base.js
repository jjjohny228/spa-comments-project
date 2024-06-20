$(document).ready(function() {
    $('.reply-btn').click(function(event) {
        event.preventDefault();
        console.log('Reply button clicked'); // Check if this message appears in the console
        $(this).closest('.comment').find('.reply-form').toggle();
    });
});
