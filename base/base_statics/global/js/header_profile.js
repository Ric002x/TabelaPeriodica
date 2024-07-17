
document.addEventListener('DOMContentLoaded', () => {
    const userIcon = document.getElementById('user-icon');
    const menuOptions = document.getElementById('menu-options');

    userIcon.addEventListener('mouseover', () => {
        menuOptions.style.display = 'flex';
    });

    userIcon.addEventListener('mouseout', () => {
        menuOptions.style.display = 'none';
    });

    menuOptions.addEventListener('mouseover', () => {
        menuOptions.style.display = 'flex';
    });

    menuOptions.addEventListener('mouseout', () => {
        menuOptions.style.display = 'none';
    });
});

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