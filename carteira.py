from blockchain import Blockchain

class Carteira(object):

    @staticmethod
    def saldo(endereco, blockchain):
        entrada = 0
        saida = 0
        for bloco in blockchain.chain:
            for transacao in bloco['transactions']:
                valor = transacao['amount']
                if transacao['recipient'] == endereco:
                    entrada += valor
                if transacao['sender'] == endereco:
                    saida += valor
        saldo = entrada - saida;
        return saldo
