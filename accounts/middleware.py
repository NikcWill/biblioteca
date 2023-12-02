from datetime import datetime
from cliente.models import Emprestimo

class UpdateLoanDaysMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.update_loan_days()
        return response

    def update_loan_days(self):
        emprestimos = Emprestimo.objects.filter(devolvido=False)
        for emprestimo in emprestimos:
            data_atual = datetime.now().date()
            data_prev_devolucao = emprestimo.data_prev_devolucao.date()

            diferenca_dias = (data_prev_devolucao - data_atual).days
            emprestimo.dias_para_devolver = diferenca_dias
            emprestimo.save()