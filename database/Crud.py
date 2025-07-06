from sqlalchemy.orm import Session
from models import Empresa, Usuario, NotaFiscal, Validacao, TesteGratuito
from datetime import datetime, timedelta
import bcrypt

class DatabaseOperations:
    def __init__(self):
        self.db = SessionLocal()
    
    # REGRAS DE USUÁRIO
    def criar_usuario(self, nome: str, email: str, senha: str, tipo: str, empresa_id: str):
        # RN001: Apenas admins podem criar usuários (verificar no controller)
        # RN003: Validação de senha (deve ser feita antes)
        
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            tipo=tipo,
            empresa_id=empresa_id
        )
        
        self.db.add(novo_usuario)
        self.db.commit()
        return novo_usuario
    
    # REGRAS DE EMPRESA E TESTE GRATUITO
    def criar_empresa_com_teste(self, razao_social: str, cnpj: str, email: str):
        # RN050: Cria empresa com período de teste
        nova_empresa = Empresa(
            razao_social=razao_social,
            cnpj=cnpj,
            email=email,
            plano=PlanoEnum.teste
        )
        
        self.db.add(nova_empresa)
        self.db.commit()
        
        # Cria o registro de teste gratuito
        teste = TesteGratuito(
            empresa_id=nova_empresa.id,
            data_inicio=datetime.utcnow(),
            data_fim=datetime.utcnow() + timedelta(days=7),
            ativo=True
        )
        
        self.db.add(teste)
        self.db.commit()
        
        return nova_empresa
    
    # REGRAS DE VALIDAÇÃO DE NOTA FISCAL
    def validar_nota_fiscal(self, empresa_id: str, usuario_id: str, xml: str):
        # Verifica se está no período de teste e tem validações disponíveis (RN050, RN051)
        teste = self.db.query(TesteGratuito).filter(
            TesteGratuito.empresa_id == empresa_id,
            TesteGratuito.ativo == True,
            TesteGratuito.data_fim > datetime.utcnow(),
            TesteGratuito.validacoes_utilizadas < TesteGratuito.limite_validacoes
        ).first()
        
        if not teste:
            raise Exception("Período de teste expirado ou limite de validações atingido")
        
        # Processa a nota fiscal (extrai dados do XML)
        dados_nota = self._extrair_dados_nota(xml)
        
        # Cria registro da nota fiscal
        nova_nota = NotaFiscal(
            empresa_id=empresa_id,
            usuario_id=usuario_id,
            chave_acesso=dados_nota['chave_acesso'],
            numero=dados_nota['numero'],
            serie=dados_nota['serie'],
            modelo=dados_nota['modelo'],
            emitente_cnpj=dados_nota['emitente_cnpj'],
            emitente_nome=dados_nota['emitente_nome'],
            destinatario_cnpj=dados_nota.get('destinatario_cnpj'),
            destinatario_nome=dados_nota.get('destinatario_nome'),
            data_emissao=dados_nota['data_emissao'],
            valor_total=dados_nota['valor_total'],
            situacao='pendente',
            xml=xml,
            json_dados=dados_nota
        )
        
        self.db.add(nova_nota)
        
        # Atualiza contador de validações do teste
        teste.validacoes_utilizadas += 1
        
        # Cria registro de validação pendente
        validacao = Validacao(
            nota_fiscal_id=nova_nota.id,
            usuario_id=usuario_id,
            status=StatusValidacaoEnum.pendente
        )
        
        self.db.add(validacao)
        self.db.commit()
        
        # Disparar tarefa assíncrona para validação real
        self._disparar_validacao_async(nova_nota.id)
        
        return nova_nota
    
    def _extrair_dados_nota(self, xml: str):
        # Implementação real precisaria de um parser de XML
        return {
            'chave_acesso': '12345678901234567890123456789012345678901234',
            'numero': '12345',
            'serie': '1',
            'modelo': '55',
            'emitente_cnpj': '12345678000199',
            'emitente_nome': 'EMITENTE TESTE LTDA',
            'data_emissao': datetime.utcnow(),
            'valor_total': 100.50
        }
    
    def _disparar_validacao_async(self, nota_id: str):
        # Implementação real usaria Celery ou similar
        pass
    
    # REGRAS DE CONVERSÃO PARA PAGO
    def converter_para_plano_pago(self, empresa_id: str, plano: str):
        # RN052: Conversão do teste para plano pago
        empresa = self.db.query(Empresa).get(empresa_id)
        
        if not empresa:
            raise Exception("Empresa não encontrada")
        
        # Desativa o teste
        teste = self.db.query(TesteGratuito).filter(
            TesteGratuito.empresa_id == empresa_id,
            TesteGratuito.ativo == True
        ).first()
        
        if teste:
            teste.ativo = False
        
        # Atualiza a empresa
        empresa.plano = plano
        empresa.data_assinatura = datetime.utcnow()
        empresa.teste_utilizado = True
        
        self.db.commit()
        return empresa