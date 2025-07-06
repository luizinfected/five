-- Extensão para UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de empresas/clientes
CREATE TABLE empresas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    cnpj VARCHAR(14) NOT NULL UNIQUE,
    inscricao_estadual VARCHAR(20),
    telefone VARCHAR(20),
    email VARCHAR(255) NOT NULL UNIQUE,
    endereco_logradouro VARCHAR(255),
    endereco_numero VARCHAR(20),
    endereco_complemento VARCHAR(100),
    endereco_bairro VARCHAR(100),
    endereco_cidade VARCHAR(100),
    endereco_estado VARCHAR(2),
    endereco_cep VARCHAR(8),
    ativo BOOLEAN DEFAULT TRUE,
    data_assinatura DATE,
    plano VARCHAR(50) CHECK (plano IN ('free', 'basic', 'professional', 'enterprise')),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT cnpj_valido CHECK (cnpj ~ '^[0-9]{14}$')
);

-- Tabela de tipos de usuário (enum personalizado)
CREATE TYPE tipo_usuario AS ENUM ('admin', 'gerente', 'analista', 'auditor');

-- Tabela de usuários
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    tipo tipo_usuario NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    ultimo_login TIMESTAMP WITH TIME ZONE,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    reset_token VARCHAR(255),
    reset_token_expira_em TIMESTAMP WITH TIME ZONE
);

-- Tabela de auditoria de acessos
CREATE TABLE auditoria_acessos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,
    empresa_id UUID REFERENCES empresas(id) ON DELETE CASCADE,
    acao VARCHAR(50) NOT NULL,
    endpoint VARCHAR(255),
    ip_address VARCHAR(45),
    user_agent TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de integração com prefeituras/sistemas externos
CREATE TABLE integracoes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('prefeitura', 'sefaz', 'outro')),
    nome VARCHAR(100) NOT NULL,
    url_base VARCHAR(255),
    api_key VARCHAR(255),
    client_id VARCHAR(255),
    client_secret VARCHAR(255),
    token_acesso VARCHAR(255),
    token_expira_em TIMESTAMP WITH TIME ZONE,
    ativo BOOLEAN DEFAULT TRUE,
    configuracao JSONB,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de notas fiscais
CREATE TABLE notas_fiscais (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    usuario_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,
    chave_acesso VARCHAR(44) NOT NULL UNIQUE,
    numero VARCHAR(15) NOT NULL,
    serie VARCHAR(3) NOT NULL,
    modelo VARCHAR(2) NOT NULL,
    emitente_cnpj VARCHAR(14) NOT NULL,
    emitente_nome VARCHAR(255) NOT NULL,
    destinatario_cnpj VARCHAR(14),
    destinatario_nome VARCHAR(255),
    data_emissao TIMESTAMP WITH TIME ZONE NOT NULL,
    data_recebimento TIMESTAMP WITH TIME ZONE,
    valor_total DECIMAL(15,2) NOT NULL,
    situacao VARCHAR(50) CHECK (situacao IN ('pendente', 'validada', 'rejeitada', 'cancelada')),
    xml TEXT NOT NULL,
    json_dados JSONB,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chave_acesso_valida CHECK (chave_acesso ~ '^[0-9]{44}$')
);

-- Tabela de validações de notas fiscais
CREATE TABLE validacoes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nota_fiscal_id UUID NOT NULL REFERENCES notas_fiscais(id) ON DELETE CASCADE,
    usuario_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,
    integracao_id UUID REFERENCES integracoes(id) ON DELETE SET NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('sucesso', 'erro', 'pendente', 'processando')),
    codigo_status VARCHAR(50),
    mensagem TEXT,
    detalhes JSONB,
    tempo_resposta_ms INTEGER,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de logs de atividades
CREATE TABLE logs_alteracoes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tabela_alterada VARCHAR(50) NOT NULL,
    registro_id UUID NOT NULL,
    usuario_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,
    acao VARCHAR(20) NOT NULL CHECK (acao IN ('insert', 'update', 'delete')),
    valores_antigos JSONB,
    valores_novos JSONB,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de faturas/pagamentos
CREATE TABLE faturas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    valor DECIMAL(10,2) NOT NULL,
    data_vencimento DATE NOT NULL,
    data_pagamento DATE,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pendente', 'pago', 'atrasado', 'cancelado')),
    metodo_pagamento VARCHAR(50),
    referencia VARCHAR(100),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhorar performance
CREATE INDEX idx_notas_fiscais_empresa ON notas_fiscais(empresa_id);
CREATE INDEX idx_notas_fiscais_chave ON notas_fiscais(chave_acesso);
CREATE INDEX idx_validacoes_nota ON validacoes(nota_fiscal_id);
CREATE INDEX idx_usuarios_empresa ON usuarios(empresa_id);
CREATE INDEX idx_auditoria_usuario ON auditoria_acessos(usuario_id);