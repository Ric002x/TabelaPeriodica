document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.sidebar ul li a');
    const sections = document.querySelectorAll('.section');

    links.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            // Remove a classe 'active' de todos os links
            links.forEach(lnk => lnk.classList.remove('active'));

            // Adiciona a classe 'active' ao link clicado
            this.classList.add('active');

            // Esconde todas as seções
            sections.forEach(section => section.classList.remove('active'));

            // Mostra a seção correspondente ao link clicado
            const sectionId = this.getAttribute('data-section');
            document.getElementById(sectionId).classList.add('active');
        });
    });
});

function confirmeAction(event, formId) {
    event.preventDefault();
    const formDelete = document.getElementById(formId);

    const userConfirmed = confirm('Deseja excluir a atividade? Essa ação é irreversível!');

    if (userConfirmed) {
        formDelete.submit();
        };
}
