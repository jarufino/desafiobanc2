from abc import *
from datetime import datetime

class Cliente:
    def __init__(self,endereco):
        self.endereco=endereco
       
        self.contas=[]
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome=nome
        self.data_nascimento=data_nascimento
        self.cpf=cpf
class Conta:
    def __init__(self, numero, cliente):
        self._saldo=0
        self._numero=numero
        self._agencia='0001'
        self._cliente=cliente
        self._historico=Historico()
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    @property
    def saldo(self):
        return self._saldo
    @property
    def numero(self):
        return self._numero
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    def sacar(self, valor):
        saldo=self.saldo
        excedeu_saldo=valor>saldo
        if excedeu_saldo:
            print('\n@@@ Falha na operação, você está sem saldo!!! @@@')
        elif valor>0:
            self._saldo-=valor
            print('\n=== Realizado o saque!!!===')
            return True
        else:
            print('\n@@@ Falha na operação, valor inválido!!! @@@')
            return False
    def depositar(self, valor):
        if valor>0:
            self._saldo+=valor
            print('\n=== Realizado o depósito!!! ===')
        else:
            print('\n@@@ Falha na operação, o valor foi inválido!!! @@@')
        return True
class ContaCoerrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super()._init__(numero, cliente)
        self.limite=limite
        self.limte_saques=limite_saques
    def sacar(self, valor):
        numero_saques=len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo']==Saque.__name__]
        )
        excedeu_limite=valor>self.limite
        excedeu_saques=numero_saques>=self.limite_saques
        
        if excedeu_limite:
            print('\n@@@ Falha na operação, valor excedeu o limite!!! @@@')
        elif excedeu_saques:
            print('\n@@@ Falha na operação, limite de saques excedido!!! @@@')
        else:
            return super().sacar(valor)
        return False
    def __str__(self):
        return f'''\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}'''
class Historico:
    def __init__(self):
        self._transacoes=[]
    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            'tipo':transacao.__class.__.__name__,
            'valor':transacao.valor,
            'data':datetime.now().strftime('%d-%m-%Y %H:%M:%s')            
        })
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractstaticmethod
    def registrar(self, conta):
        pass
class Saque(Transacao):
    def __init__(self, valor):
        self._valor=valor
        @property
        def valor(self):
            return self._valor
        def registrar(self, conta):
            sucesso_transacao=conta.sacar(self.valor)
            if sucesso_transacao:
                conta.historico.adicionar_transacao(self)
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor=valor
        @property
        def valor(self):
            return self._valor
    def registrar(self, conta):
        sucesso_transacao=conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adcionar_transacao(self)