
// Function to show options of User Profile
document.addEventListener('DOMContentLoaded', () => {
    const userIcon = document.getElementById('dropdown-user');
    const userMenu = document.getElementById('dropdown-user-menu');
    const overlay = document.getElementById('overlay');

    userIcon.addEventListener('click', () => {
        userMenu.classList.toggle('active');
        overlay.classList.toggle('active');
    })

    overlay.addEventListener('click', () => {
        userMenu.classList.toggle('active');
        overlay.classList.toggle('active');
    })
})

// Function to confirm Logout
document.addEventListener('DOMContentLoaded', () => {
    const logoutButton = document.getElementById('logout');
    const formLogout = document.getElementById('form-logout')

    logoutButton.addEventListener('click', (event) => {
        event.preventDefault();

        const userConfirmed = confirm('Você tem certeza que quer sair?');

        if (userConfirmed) {
            formLogout.submit();
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const navMenuBar = document.getElementById('dropdown-navigation-items');
    const navMenu = document.getElementById('dropdown-navigation-items-menu');

    navMenuBar.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    })
})