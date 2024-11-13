document.addEventListener("DOMContentLoaded", () => {
    const showAPINav = document.getElementById("showAPINav");
    const APINav = document.getElementById("APINav");

    showAPINav.addEventListener('click', () => {
        APINav.classList.toggle('active');
    })
})