function confirmeAction(event, formId) {
    event.preventDefault();
    const formDelete = document.getElementById(formId);

    const userConfirmed = confirm('Deseja excluir a atividade? Essa ação é irreversível!');

    if (userConfirmed) {
        formDelete.submit();
        };
}

