document.addEventListener('DOMContentLoaded', function() {
    const clienteForm = document.getElementById('cliente-form');
    const buscarBtn = document.getElementById('buscar-btn');
    const emprestimoForm = document.getElementById('emprestimo-form');
    const dataDevolucao = document.getElementById('data-devolucao');
    const salvarBtn = document.getElementById('salvar-btn');

    clienteForm.addEventListener('change', function() {
        buscarBtn.disabled = !clienteForm.q.value;
    });

    emprestimoForm.addEventListener('change', function() {
        const checkboxes = document.querySelectorAll('input[name="livros_emprestimo[]"]:checked');
        salvarBtn.disabled = !(checkboxes.length > 0 && dataDevolucao.value.trim() !== '');
    });

    dataDevolucao.addEventListener('input', function() {
        const checkboxes = document.querySelectorAll('input[name="livros_emprestimo[]"]:checked');
        salvarBtn.disabled = !(checkboxes.length > 0 && dataDevolucao.value.trim() !== '');
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const emprestimoDeletado = urlParams.get('emprestimo_deletado');

    if (emprestimoDeletado === 'true') {
        window.location.href = window.location.pathname;
    }
});
   const addClientButton = document.getElementById('add-client-button');
        const deactivateClientButton = document.getElementById('deactivate-client-button');
        const addClientForm = document.getElementById('add-client-form');
        const deactivateClientForm = document.getElementById('deactivate-client-form');

        addClientButton.addEventListener('click', function() {
            addClientForm.style.display = 'block';
            deactivateClientForm.style.display = 'none';
        });

        deactivateClientButton.addEventListener('click', function() {
            deactivateClientForm.style.display = 'block';
            addClientForm.style.display = 'none';
        });

