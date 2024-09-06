// Rating form Counting 

document.addEventListener('DOMContentLoaded', () => {
    const textArea = document.querySelectorAll('#id_comment');
    const charCount = document.querySelectorAll('#charCount');
    const cancelButton = document.querySelectorAll('.restart-charcount');

    textArea.forEach(area => {
        area.addEventListener('input', () => {
            const currentLength = area.value.length;
            charCount.forEach(div => {
                div.textContent = `${currentLength}/250 caracteres`
            })
        })
    })

    cancelButton.forEach(button => {
        button.addEventListener('click', () => {
            charCount.forEach(button => {
                button.textContent = '0/250 caracteres'
            })
        })
    })
})

// show rate sistem
document.addEventListener('DOMContentLoaded', () => {
    const starsDiv = document.getElementById('stars');
    const commentDiv = document.getElementById('rating-form_comment');
    const formbuttons = document.getElementById('rating-form_buttons')
    const cancelButton = document.getElementById('rating-cancel_button');

    starsDiv.addEventListener('click', () => {
        commentDiv.classList.add('active');
        formbuttons.classList.add('active');
        cancelButton.classList.add('active');
    })


    cancelButton.addEventListener('click', () => {
        commentDiv.classList.remove('active');
        formbuttons.classList.remove('active');
        cancelButton.classList.remove('active');
    })
})

document.addEventListener('DOMContentLoaded', function() {
    const buttonRatingOptions = document.getElementById('user-rating_options_show');
    const ratingOptions = document.getElementById('user-rating_options_menu');

    buttonRatingOptions.addEventListener('mouseover', function() {
        ratingOptions.classList.add('active')
    })

    buttonRatingOptions.addEventListener('mouseleave', function() {
        ratingOptions.classList.remove('active')
    })
    
    ratingOptions.addEventListener('mouseover', function() {
        ratingOptions.classList.add('active')
    })

    ratingOptions.addEventListener('mouseleave', function() {
        ratingOptions.classList.remove('active')
    })

    buttonRatingOptions.addEventListener('click', function() {
        ratingOptions.classList.toggle('active')
    })

})


// Edit rating Form:
document.addEventListener('DOMContentLoaded', function() {
    const buttonEditForm = document.getElementById('button-form_edit');
    const divEditForm = document.getElementById('rating-edit-form_container');
    const divFormCreate = document.getElementById('rating-form_container');
    const userRating = document.getElementById('user_rating')

    buttonEditForm.addEventListener('click', function() {
        divEditForm.style.display = 'block';
        divFormCreate.style.display = 'none';
        userRating.style.display = 'none';
    })

    const cancelButton = document.getElementById('rating-cancel_edit_form');

    cancelButton.addEventListener('click', function() {
        divEditForm.style.display = 'none';
        divFormCreate.style.display = 'block';
        userRating.style.display = 'block';
    })
})


// Delete rate confim
function confimRateDelete(event, formId) {
    event.preventDefault();
    const formDelete = document.getElementById(formId);
    const userConfirmed = confirm('Deseja excluir seu comentário? Essa ação é irreversível!')

    if (userConfirmed) {
        formDelete.submit()
    };
}

// Confirm Edit
document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.querySelectorAll('.activity_edit_button');
    
    editButton.forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('.overlay-edit_warning').forEach(div => {
                div.classList.remove('active')
            });

            const buttonTarget = this.getAttribute('data-target');
            const targetDiv = document.getElementById(buttonTarget);

            if (targetDiv) {
                targetDiv.classList.add('active');
                document.body.classList.add('no-scroll');
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                })
            }

            const editCancel = document.querySelectorAll('#edit-cancel');
            editCancel.forEach(button => {
                button.addEventListener('click', function() {
                    targetDiv.classList.remove('active');
                    document.body.classList.remove('no-scroll')

                })
            })
        })
    })
})