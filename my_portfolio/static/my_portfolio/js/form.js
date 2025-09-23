function handleFeedbackInput(fieldname, message) {
    $('#feedback-sent').removeClass('d-block');
    $('#error-feedback').addClass('d-block');
    $('.form-control').css('border', 'none');
    $(fieldname).css('border', '1px solid red');
    $('#error-feedback').html(message);
}

function validateFeedbackForm() {
    if ($('#clientName').val() === "") {
        handleFeedbackInput('#clientName', 'Please fill in your name');
        return false;
    }
    if ($('#clientEmail').val() === "") {
        handleFeedbackInput('#clientEmail', 'Please fill in the email field');
        return false;
    }
    if ($('#feedbackMessage').val() === "") {
        handleFeedbackInput('#feedbackMessage', 'Please input your feedback message');
        return false;
    }
    return true;
}

function onSubmit(token) {
    $('#feedbackFormBtn').html("Sending <span class='spinner-border spinner-border-sm' role='status'></span>");
    $('#feedbackFormBtn').css('pointer-events', 'none');
    
    const formData = new FormData($('#feedback-form')[0]);
    formData.append('g-recaptcha-response', token);
    
    $.ajax({
        type: 'POST',
        url: '/submit-feedback/',
        data: formData,
        processData: false,
        contentType: false, 
        success: handleFormSuccess,
        error: handleFormError
    });
}

function handleFormSuccess(response) {
    if (response.success) {
        $('#error-feedback').removeClass('d-block');
        $('#feedbackFormBtn').css('pointer-events', '');
        $('#feedbackFormBtn').html('Send Message');
        $('#feedback-sent').addClass('d-block');
        $('#feedback-sent').html(response.message);
        $('.form-control').css('border', 'none');
        $('#feedback-form')[0].reset();
        grecaptcha.reset(); // Reset reCAPTCHA
    } else {
        handleFormError(response);
    }
}

function handleFormError(response) {
    $('#feedback-sent').removeClass('d-block');
    $('#feedbackFormBtn').css('pointer-events', '');
    $('#feedbackFormBtn').html('Send Message');
    $('#error-feedback').addClass('d-block');
    $('.form-control').css('border', 'none');
    $('#error-feedback').html(response.message || "Can't submit comment right now");
    grecaptcha.reset(); // Reset reCAPTCHA
}

$(document).ready(function(){
    // Pre-validate before reCAPTCHA triggers
    $('#feedbackFormBtn').click(function(e) {
        if (!validateFeedbackForm()) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }
    });

     $('#submitEmailBtn').click(function(e) {
        // Validate before reCAPTCHA triggers
        if ($('#name').val() === "") {
            handleEmailInput('#name', 'Please input your name');
            return false;
        }
        if ($('#email').val() === "") {
            handleEmailInput('#email', 'Please fill in your email');
            return false;
        }
        if ($('#message').val() === "") {
            handleEmailInput('#message', 'Input your message');
            return false;
        }
    });
});

function onEmailSubmit(token) {
    $('#submitEmailBtn').html("Sending <span class='spinner-border spinner-border-sm' role='status'></span>");
    $('#submitEmailBtn').css('pointer-events', 'none');
    
    const formData = new FormData($('#email-form')[0]);
    formData.append('g-recaptcha-response', token);
    $.ajax({
        type: 'POST',
        url: '/submit-email/',
        data: formData,
        processData: false,
        contentType: false,
        success: EmailSuccessful,
        error: EmailFailure
    });
}

    function EmailSuccessful(response) {
        if (response.success){
            $('#submitEmailBtn').css('pointer-events', '')
            $('#submitEmailBtn').html("Send message")
            $('.form-control').css('border', 'none')
            $('#status-message').html(`<div class='alert sent-message d-block alert-dismissible fade show' role='alert'>${response.message}<button type='button' class='btn-close text-white' data-bs-dismiss='alert' aria-label='Close'></button></div>`)
            $('#email-form')[0].reset()      
        }
        else {
            EmailFailure(response)
        }
    }

    function EmailFailure(response) {
        $('#submitEmailBtn').html("Send message")
        $('#submitEmailBtn').css('pointer-events', '')
        $('.form-control').css('border', 'none')
        $('#status-message').html(`<div class='alert error-message d-block alert-dismissible fade show' role='alert'>${response.message}<button type='button' class='btn-close text-white' data-bs-dismiss='alert' aria-label='Close'></button></div>`)
    }