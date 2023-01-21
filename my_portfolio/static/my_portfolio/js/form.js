$(document).ready(function(){
    /* feedback form */
    $('#feedback-form').submit(function(event){
        event.preventDefault()
        function handleFeedbackInput(fieldname, message) {

            $('#feedback-sent').removeClass('d-block')
            $('#error-feedback').addClass('d-block')
            $('.form-control').css('border', 'none')
            $(fieldname).css('border', '1px solid red')
            $('#error-feedback').html(message)
        }


        if ($(this)[0].name.value == "" || $(this)[0].name.value == null) {
            return handleFeedbackInput('#client-name', 'Please fill in your name')
        }

        if ($(this)[0].email.value == "" || $(this)[0].name.value == null) {
            return handleFeedbackInput('#client-email', 'Please fill in the email field')
        }

        if ($(this)[0].message.value == "" || $(this)[0].name.value == null) {
            return handleFeedbackInput('#error-feedback', 'Please input your feedback message')
        }
        $('#feedbackFormBtn').html("Sending <span class='spinner-border spinner-border-sm' role='status'></span>")
        $('#feedbackFormBtn').css('pointer-events', 'none')
        $.ajax({
            type: 'POST',
            url: '/submit-feedback/',
            data: new FormData(this),
            processData: false,
            contentType: false, 
            success: handleFormSuccess,
            error: handleFormError
        })
    })
    

    function handleFormSuccess(response){
        if (response.success) {
            $('#error-feedback').removeClass('d-block')
            $('#feedbackFormBtn').css('pointer-events', '')
            $('#feedbackFormBtn').html('Send Message')
            $('#feedback-sent').addClass('d-block')
            $('#feedback-sent').html(response.message)
            $('.form-control').css('border', 'none')
            $('#feedback-form')[0].reset()
        }
        else {
            handleFormError(response)
        }
        
    }

    function handleFormError(response){
        $('#feedback-sent').removeClass('d-block')
        $('#feedbackFormBtn').css('pointer-events', '')
        $('#feedbackFormBtn').html('Send Message')
        $('#error-feedback').addClass('d-block')
        $('.form-control').css('border', 'none')
        $('#error-feedback').html(response.message)
    }

    /* email form */
    $('#email-form').submit(function(event){
        event.preventDefault()

        function handleEmailInput(fieldname, message) {
            $('.form-control').css('border', 'none')
            $(fieldname).css('border', '1px solid red')
            $('#status-message').html(`<div class='alert error-message d-block alert-dismissible fade show' role='alert'>${message}<button type='button' class='btn-close text-white' data-bs-dismiss='alert' aria-label='Close'></button></div>`)
        }

        if ($(this)[0].name.value == "" || $(this)[0].name.value == null) {
            return handleEmailInput('#name', 'Please input your name')
        }

        if ($(this)[0].email.value == "" || $(this)[0].email.value == null) {
            return handleEmailInput('#email', 'Please fill in your email')
        }

        if ($(this)[0].subject.value == "" || $(this)[0].subject.value == null) {
            return handleEmailInput('#subject', 'State your subject')
        }

        if ($(this)[0].message.value == "" || $(this)[0].message.value == null) {
            return handleEmailInput('#message', 'Input your message')
        }


        $('#submitEmailBtn').html("Sending <span class='spinner-border spinner-border-sm' role='status'></span>")
        $('#submitEmailBtn').css('pointer-events', 'none')

        $.ajax({
            type: 'POST',
            url: '/submit-email/',
            data: new FormData(this),
            processData: false,
            contentType: false,
            success: EmailSuccessful,
            error:  EmailFailure
        })

    })
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
})  

 


