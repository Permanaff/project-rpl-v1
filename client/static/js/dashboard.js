$(document).ready(function () {
    check_permission()
    // $('#nama-user').append('Samantha Doe')
});

function check_permission() {
    fetch('http://127.0.0.1:5000/login-status', {method: 'post'})
    // fetch('https://a4a2-202-51-208-50.ngrok-free.app/login-status', {method: 'post'})
    .then(response => response.json())
    .then(response => {
        $('#nama-user').append(response.nama)

        let container = $('#manage-account')

        if (response.level_user === '1') {
            container.removeClass('visually-hidden')
            $('#add-carousel').removeClass('visually-hidden')
            $('#tile-user').append('Super Admin')
        } 
        else {
            $('#tile-user').append('Admin')
        }

    })
    .catch(error => {
        console.log(error)
    })
}

function profile () {
    fetch('http://127.0.0.1:5000/login-status')
}

