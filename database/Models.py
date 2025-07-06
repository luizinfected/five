from database import Base, TipoUsuarioEnum, StatusValidacaoEnum, PlanoEnum
from sqlalchemy.sql import func

class Empresa(Base):
    __tablename__ = 'empresas'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255))
    cnpj = Column(String(14), nullable=False, unique=True)
    inscricao_estadual = Column(String(20))
    telefone = Column(String(20))
    email = Column(String(255), nullable=False, unique=True)
    endereco_logradouro = Column(String(255))
    endereco_numero = Column(String(20))
    endereco_complemento = Column(String(100))
    endereco_bairro = Column(String(100))
    endereco_cidade = Column(String(100))
    endereco_estado = Column(String(2))
    endereco_cep = Column(String(8))
    ativo = Column(Boolean, default=True)
    data_assinatura = Column(DateTime)
    plano = Column(Enum(PlanoEnum), default=PlanoEnum.teste)
    data_inicio_teste = Column(DateTime)
    data_fim_teste = Column(DateTime)
    teste_utilizado = Column(Boolean, default=False)
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    usuarios = relationship("Usuario", back_populates="empresa")
    notas_fiscais = relationship("NotaFiscal", back_populates="empresa")
    integracoes = relationship("Integracao", back_populates="empresa")
    testes = relationship("TesteGratuito", back_populates="empresa")

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey('empresas.id'), nullable=False)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoUsuarioEnum), nullable=False)
    ativo = Column(Boolean, default=True)
    ultimo_login = Column(DateTime)
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())
    reset_token = Column(String(255))
    reset_token_expira_em = Column(DateTime)
    
    empresa = relationship("Empresa", back_populates="usuarios")
    notas_fiscais = relationship("NotaFiscal", back_populates="usuario")
    validacoes = relationship("Validacao", back_populates="usuario")
    acessos = relationship("AuditoriaAcesso", back_populates="usuario")

class TesteGratuito(Base):
    __tablename__ = 'testes_gratuitos'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey('empresas.id'), nullable=False)
    data_inicio = Column(DateTime, nullable=False, server_default=func.now())
    data_fim = Column(DateTime, nullable=False)
    limite_validacoes = Column(Integer, default=100)
    validacoes_utilizadas = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())
    
    empresa = relationship("Empresa", back_populates="testes")

class NotaFiscal(Base):
    __tablename__ = 'notas_fiscais'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey('empresas.id'), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'))
    chave_acesso = Column(String(44), nullable=False, unique=True)
    numero = Column(String(15), nullable=False)
    serie = Column(String(3), nullable=False)
    modelo = Column(String(2), nullable=False)
    emitente_cnpj = Column(String(14), nullable=False)
    emitente_nome = Column(String(255), nullable=False)
    destinatario_cnpj = Column(String(14))
    destinatario_nome = Column(String(255))
    data_emissao = Column(DateTime, nullable=False)
    data_recebimento = Column(DateTime)
    valor_total = Column(Numeric(15, 2), nullable=False)
    situacao = Column(String(50))
    xml = Column(Text, nullable=False)
    json_dados = Column(JSON)
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    empresa = relationship("Empresa", back_populates="notas_fiscais")
    usuario = relationship("Usuario", back_populates="notas_fiscais")
    validacoes = relationship("Validacao", back_populates="nota_fiscal")

class Validacao(Base):
    __tablename__ = 'validacoes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nota_fiscal_id = Column(UUID(as_uuid=True), ForeignKey('notas_fiscais.id'), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey('usuarios.id'))
    integracao_id = Column(UUID(as_uuid=True), ForeignKey('integracoes.id'))
    status = Column(Enum(StatusValidacaoEnum), nullable=False)
    codigo_status = Column(String(50))
    mensagem = Column(Text)
    detalhes = Column(JSON)
    tempo_resposta_ms = Column(Integer)
    criado_em = Column(DateTime, server_default=func.now())
    
    nota_fiscal = relationship("NotaFiscal", back_populates="validacoes")
    usuario = relationship("Usuario", back_populates="validacoes")
    integracao = relationship("Integracao")

# ... (continuam os outros modelos: Integracao, AuditoriaAcesso, LogAlteracao)