document.addEventListener('DOMContentLoaded', function() {
    const clienteForm = document.getElementById('cliente-form');
    const buscarBtn = document.getElementById('buscar-btn');
    const emprestimoForm = document.getElementById('emprestimo-form');
    const dataDevolucao = document.getElementById('data-devolucao');
    const salvarBtn = document.getElementById('salvar-btn');

    // Verifica se o campo do cliente foi preenchido
    clienteForm.addEventListener('change', function() {
        buscarBtn.disabled = !clienteForm.q.value;
    });

    // Verifica se pelo menos um livro foi selecionado ou se a data de devolução foi preenchida
    emprestimoForm.addEventListener('change', function() {
        const checkboxes = document.querySelectorAll('input[name="livros_emprestimo[]"]:checked');
        salvarBtn.disabled = !(checkboxes.length > 0 && dataDevolucao.value.trim() !== '');
    });

    // Verifica se o campo de data de devolução foi preenchido
    dataDevolucao.addEventListener('input', function() {
        const checkboxes = document.querySelectorAll('input[name="livros_emprestimo[]"]:checked');
        salvarBtn.disabled = !(checkboxes.length > 0 && dataDevolucao.value.trim() !== '');
    });
});