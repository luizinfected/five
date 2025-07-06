/*

 -- arquivo de criação de relatórios

*/


/*
View para relatório de validações
*/
CREATE VIEW view_relatorio_validacoes AS
SELECT 
    nf.empresa_id,
    e.razao_social,
    COUNT(*) AS total_notas,
    COUNT(CASE WHEN v.status = 'sucesso' THEN 1 END) AS validacoes_sucesso,
    COUNT(CASE WHEN v.status = 'erro' THEN 1 END) AS validacoes_erro,
    COUNT(CASE WHEN v.status = 'pendente' THEN 1 END) AS validacoes_pendentes
FROM 
    notas_fiscais nf
JOIN 
    empresas e ON nf.empresa_id = e.id
LEFT JOIN 
    validacoes v ON nf.id = v.nota_fiscal_id
GROUP BY 
    nf.empresa_id, e.razao_social;

-- View para usuários com informações da empresa
CREATE VIEW view_usuarios_com_empresa AS
SELECT 
    u.id,
    u.nome,
    u.email,
    u.tipo,
    u.ativo,
    u.ultimo_login,
    e.id AS empresa_id,
    e.razao_social,
    e.cnpj
FROM 
    usuarios u
JOIN 
    empresas e ON u.empresa_id = e.id;