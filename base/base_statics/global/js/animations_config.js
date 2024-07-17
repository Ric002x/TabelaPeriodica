// script.js

document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-enter');
                observer.unobserve(entry.target); // Stop observing once the animation has been triggered
            }
        });
    }, {
        threshold: 0.1 // Adjust this value to trigger animation earlier or later
    });

    elements.forEach(element => {
        observer.observe(element);
    });
});
