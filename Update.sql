-- ============================================================================
-- PROTON ERP - ESTRUTURA DO BANCO DE DADOS
-- Versao organizada a partir do script enviado
-- Banco: PostgreSQL
-- ============================================================================
-- IMPORTANTE:
-- 1. Este arquivo cria a estrutura principal e insere os dados iniciais.
-- 2. CREATE TABLE IF NOT EXISTS nao altera tabelas que ja existem.
--    Em bancos existentes, revise e execute as migracoes da secao 12.
-- 3. Comandos de exclusao/limpeza foram deixados comentados na secao 13.
-- 4. Nao armazene senhas em texto puro em ambiente de producao.
--    Os valores de seed abaixo foram preservados do script original e devem
--    ser substituidos por hashes gerados pela aplicacao.
-- ============================================================================


-- ============================================================================
-- 1. AUTENTICACAO E CONTROLE DE ACESSO
-- ============================================================================

CREATE TABLE IF NOT EXISTS usuarios_sistema (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    senha           VARCHAR(255) NOT NULL,
    nivel_acesso    VARCHAR(50) DEFAULT 'TECNICO',
    status          VARCHAR(20) DEFAULT 'ATIVO',
    data_criacao    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================================
-- 2. CLIENTES DEDICADOS
-- ============================================================================

CREATE TABLE IF NOT EXISTS clientes_dedicados (
    id              SERIAL PRIMARY KEY,
    cliente         VARCHAR(255) NOT NULL,
    cnpj_cpf        VARCHAR(255),
    qnt_de_servs    INTEGER,
    ad              VARCHAR(100),
    ambiente        VARCHAR(255),
    vpn             BOOLEAN,
    sgbd            VARCHAR(50),
    data_criacao    DATE DEFAULT CURRENT_DATE,
    criado_por      VARCHAR(255),
    hora_criacao    TIME DEFAULT CURRENT_TIME
);


-- ============================================================================
-- 3. SERVIDORES DOS CLIENTES DEDICADOS
-- ============================================================================

CREATE TABLE IF NOT EXISTS servidores_clientes_dedicados (
    id              SERIAL PRIMARY KEY,
    cliente_id      INTEGER NOT NULL
                    REFERENCES clientes_dedicados(id) ON DELETE CASCADE,
    tipo_servidor   VARCHAR(50),
    ip_publico      VARCHAR(100),
    ip_privado      VARCHAR(150),
    hostname        VARCHAR(150),
    usuario         VARCHAR(100),
    senha           VARCHAR(150)
);


-- ============================================================================
-- 4. BANCOS DE DADOS DOS CLIENTES DEDICADOS
-- ============================================================================

CREATE TABLE IF NOT EXISTS bancos_dedicados (
    id              SERIAL PRIMARY KEY,
    id_cliente      INTEGER NOT NULL
                    REFERENCES clientes_dedicados(id) ON DELETE CASCADE,
    sgbd            VARCHAR(100),
    hqbird          VARCHAR(50),
    versao          VARCHAR(100),
    usuario_banco   VARCHAR(100),
    senha_banco     VARCHAR(255),
    produtos        VARCHAR(500)
);


-- ============================================================================
-- 5. CLIENTES COMPARTILHADOS
-- ============================================================================

CREATE TABLE IF NOT EXISTS clientes_compartilhados (
    id                  SERIAL PRIMARY KEY,
    tipo_nuvem          VARCHAR(255),
    pod                 INTEGER,
    data_criacao        DATE DEFAULT CURRENT_DATE,
    razao_social        VARCHAR(255) NOT NULL,
    cpf_cnpj            VARCHAR(255),
    razao_cnpj_antigos  VARCHAR(255),
    cod_ag              VARCHAR(255),
    pasta_rede          VARCHAR(150),
    contato             VARCHAR(100),
    usuarios            INTEGER,
    origem              VARCHAR(100),
    telefone            VARCHAR(255),
    email               VARCHAR(150),
    sistemas            VARCHAR(255),
    status              VARCHAR(255),
    banco               VARCHAR(255),
    criado_por          VARCHAR(255),
    hora_criacao        TIME DEFAULT CURRENT_TIME,
    valor_seguro        VARCHAR(100) DEFAULT 'N/A'
);


-- ============================================================================
-- 6. BANCOS DE DADOS DA NUVEM COMPARTILHADA
-- ============================================================================

CREATE TABLE IF NOT EXISTS bancos_nuvem_compartilhada (
    id                  SERIAL PRIMARY KEY,
    id_cliente          INTEGER
                        REFERENCES clientes_compartilhados(id) ON DELETE CASCADE,
    sgbd                VARCHAR(50),
    segmento            VARCHAR(50),
    ip_servidor         VARCHAR(100),
    nome_banco          VARCHAR(255),
    caminho_banco       VARCHAR(255),
    caminho_conexao     VARCHAR(255),
    versao              VARCHAR(50),
    usuario_banco       VARCHAR(100),
    senha_banco         VARCHAR(255),
    razao_social        VARCHAR(255)
);


-- ============================================================================
-- 7. USUARIOS DA NUVEM COMPARTILHADA
-- ============================================================================

CREATE TABLE IF NOT EXISTS usuarios_nuvem_compartilhada (
    id              SERIAL PRIMARY KEY,
    id_cliente      INTEGER
                    REFERENCES clientes_compartilhados(id) ON DELETE CASCADE,
    nome_usuario    VARCHAR(255),
    email_usuario   VARCHAR(255),
    perfil          VARCHAR(100)
);


-- ============================================================================
-- 8. DADOS DOS CLIENTES FORTESRH
-- ============================================================================

CREATE TABLE IF NOT EXISTS fortesrh (
    id                  SERIAL PRIMARY KEY,
    tipo_ambiente       VARCHAR(50),
    cliente             VARCHAR(255) NOT NULL,
    cnpj_cpf            VARCHAR(50),
    url_acesso          VARCHAR(255),
    servidor_app        VARCHAR(150),
    banco_dados         VARCHAR(150),
    pasta_web           VARCHAR(150),
    usuario_db          VARCHAR(100),
    senha_db            VARCHAR(100),
    load_balance        VARCHAR(50),
    ip_load_balance     VARCHAR(50),
    status              VARCHAR(50),
    data_criacao        DATE DEFAULT CURRENT_DATE,
    web_aplication      VARCHAR(255),
    ip_publico          VARCHAR(50),
    ip_privado          VARCHAR(50),
    versao              VARCHAR(50),
    criado_por          VARCHAR(255),
    hora_criacao        TIME DEFAULT CURRENT_TIME
);


-- ============================================================================
-- 9. CLIENTES CANCELADOS
-- ============================================================================

CREATE TABLE IF NOT EXISTS clientes_cancelados (
    id                      SERIAL PRIMARY KEY,
    tipo_nuvem              VARCHAR(50),
    pod                     INTEGER,
    data_criacao            DATE DEFAULT CURRENT_DATE,
    cliente_razao           VARCHAR(255) NOT NULL,
    status_antigo           VARCHAR(50),
    inicio_cancelamento     DATE,
    final_cancelamento      DATE,
    chamado                 VARCHAR(100),
    tecnico_responsavel     VARCHAR(255),
    criado_por              VARCHAR(255),
    hora_criacao            TIME DEFAULT CURRENT_TIME
);


-- ============================================================================
-- 10. WEBSERVICES COMPARTILHADOS
-- ============================================================================

CREATE TABLE IF NOT EXISTS webservices_compartilhados (
    id                  SERIAL PRIMARY KEY,
    id_cliente          INTEGER
                        REFERENCES clientes_compartilhados(id) ON DELETE CASCADE,
    integracao          VARCHAR(150),
    servidor_ws         VARCHAR(100),
    porta               VARCHAR(20),
    endereco_soap       VARCHAR(255),
    endereco_wsdl       VARCHAR(255),
    string_conexao_bd   VARCHAR(255),
    usuario_bd          VARCHAR(100),
    senha_bd            VARCHAR(100)
);


-- ============================================================================
-- 11. AUDITORIA E CONTROLE DE VERSAO
-- ============================================================================

CREATE TABLE IF NOT EXISTS logs_auditoria (
    id              SERIAL PRIMARY KEY,
    usuario_email   VARCHAR(255),
    acao            VARCHAR(100),
    detalhes        TEXT,
    data_hora       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS controle_versao (
    id                  SERIAL PRIMARY KEY,
    versao_db           VARCHAR(50) NOT NULL,
    data_atualizacao    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descricao           TEXT
);


-- ============================================================================
-- 12. INDICES PARA RELACIONAMENTOS E CONSULTAS FREQUENTES
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_servidores_dedicados_cliente
    ON servidores_clientes_dedicados(cliente_id);

CREATE INDEX IF NOT EXISTS idx_bancos_dedicados_cliente
    ON bancos_dedicados(id_cliente);

CREATE INDEX IF NOT EXISTS idx_bancos_compartilhados_cliente
    ON bancos_nuvem_compartilhada(id_cliente);

CREATE INDEX IF NOT EXISTS idx_usuarios_compartilhados_cliente
    ON usuarios_nuvem_compartilhada(id_cliente);

CREATE INDEX IF NOT EXISTS idx_webservices_compartilhados_cliente
    ON webservices_compartilhados(id_cliente);


-- ============================================================================
-- 13. DADOS INICIAIS (SEED)
-- ============================================================================

INSERT INTO controle_versao (versao_db, descricao)
SELECT '1.0', 'Lancamento inicial - Proton ERP V1'
WHERE NOT EXISTS (
    SELECT 1
    FROM controle_versao
    WHERE versao_db = '1.0'
);

-- ATENCAO: substituir as senhas abaixo por hashes seguros gerados pela aplicacao.
-- ON CONFLICT evita duplicar usuarios quando o script for executado novamente.
INSERT INTO usuarios_sistema (email, senha, nivel_acesso)
VALUES
    ('gabriellevi@fortestecnologia.com.br', 'fortes123', 'MASTER'),
    ('pauloteixeira@fortestecnologia.com.br', 'fortes123', 'MASTER'),
    ('wcordeiro@fortestecnologia.com.br', 'fortes123', 'MASTER'),
    ('vivianlima@fortestecnologia.com.br', 'fortes123', 'N2'),
    ('kenedysoares@fortestecnologia.com.br', 'fortes123', 'N2'),
    ('damiaosilva@fortestecnologia.com.br', 'fortes123', 'N2')
ON CONFLICT (email) DO NOTHING;


-- ============================================================================
-- 14. CONSULTAS ADMINISTRATIVAS
-- Execute individualmente quando precisar consultar os dados.
-- ============================================================================

-- Total de clientes dedicados:
-- SELECT COUNT(*) AS total_clientes_dedicados FROM clientes_dedicados;

-- Total de clientes compartilhados:
-- SELECT COUNT(*) AS total_clientes_compartilhados FROM clientes_compartilhados;

-- Listar clientes dedicados:
-- SELECT * FROM clientes_dedicados ORDER BY cliente;

-- Listar clientes compartilhados:
-- SELECT * FROM clientes_compartilhados ORDER BY razao_social;

-- Listar servidores e seus clientes:
-- SELECT c.cliente, s.*
-- FROM servidores_clientes_dedicados AS s
-- JOIN clientes_dedicados AS c ON c.id = s.cliente_id
-- ORDER BY c.cliente, s.id;


-- ============================================================================
-- 15. MIGRACOES OPCIONAIS PARA BANCOS JA EXISTENTES
-- ATENCAO: revise cada comando antes de executar.
-- Estas migracoes nao sao necessarias em uma instalacao nova criada do zero.
-- ============================================================================

-- Adicionar campos que podem estar ausentes em instalacoes antigas:
-- ALTER TABLE clientes_dedicados
--     ADD COLUMN IF NOT EXISTS sgbd VARCHAR(50),
--     ADD COLUMN IF NOT EXISTS data_criacao DATE DEFAULT CURRENT_DATE,
--     ADD COLUMN IF NOT EXISTS criado_por VARCHAR(255),
--     ADD COLUMN IF NOT EXISTS hora_criacao TIME DEFAULT CURRENT_TIME;

-- ALTER TABLE servidores_clientes_dedicados
--     ADD COLUMN IF NOT EXISTS hostname VARCHAR(150),
--     ADD COLUMN IF NOT EXISTS ip_publico VARCHAR(100);

-- Se a coluna antiga ip_servidor existir e ip_privado ainda nao existir:
-- ALTER TABLE servidores_clientes_dedicados
--     RENAME COLUMN ip_servidor TO ip_privado;

-- Campos adicionais de auditoria em tabelas antigas:
-- ALTER TABLE clientes_compartilhados
--     ADD COLUMN IF NOT EXISTS criado_por VARCHAR(255),
--     ADD COLUMN IF NOT EXISTS hora_criacao TIME DEFAULT CURRENT_TIME;

-- ALTER TABLE fortesrh
--     ADD COLUMN IF NOT EXISTS status VARCHAR(50),
--     ADD COLUMN IF NOT EXISTS data_criacao DATE DEFAULT CURRENT_DATE,
--     ADD COLUMN IF NOT EXISTS web_aplication VARCHAR(255),
--     ADD COLUMN IF NOT EXISTS ip_publico VARCHAR(50),
--     ADD COLUMN IF NOT EXISTS ip_privado VARCHAR(50),
--     ADD COLUMN IF NOT EXISTS versao VARCHAR(50),
--     ADD COLUMN IF NOT EXISTS criado_por VARCHAR(255),
--     ADD COLUMN IF NOT EXISTS hora_criacao TIME DEFAULT CURRENT_TIME;


-- ============================================================================
-- 16. IMPORTACAO DE PLANILHAS (TABELAS DE STAGING OPCIONAIS)
-- Descomente somente se for utilizar uma rotina de importacao via Python.
-- ============================================================================

-- CREATE TABLE IF NOT EXISTS tmp_dedicados (
--     cliente VARCHAR,
--     cnpj_cpf VARCHAR,
--     qnt_de_servs VARCHAR,
--     ad VARCHAR,
--     ambiente VARCHAR,
--     vpn VARCHAR,
--     sgbd VARCHAR
-- );

-- CREATE TABLE IF NOT EXISTS tmp_servidores (
--     data_criacao VARCHAR,
--     cliente VARCHAR,
--     ip_publico VARCHAR,
--     ip_privado VARCHAR,
--     funcao VARCHAR,
--     usuario VARCHAR,
--     senha VARCHAR,
--     hostname VARCHAR
-- );

-- CREATE TABLE IF NOT EXISTS tmp_sgbd (
--     cliente VARCHAR,
--     sgbd VARCHAR,
--     versao VARCHAR,
--     usuario VARCHAR,
--     senha VARCHAR,
--     hqbird VARCHAR,
--     cnpj_cpf VARCHAR,
--     produtos VARCHAR
-- );

-- CREATE TABLE IF NOT EXISTS tmp_comp_bancos (
--     segmento VARCHAR,
--     razao_social VARCHAR,
--     servidor VARCHAR,
--     conexao VARCHAR,
--     sgbd VARCHAR
-- );

-- CREATE TABLE IF NOT EXISTS tmp_comp_usuarios (
--     responsavel VARCHAR,
--     razao_social VARCHAR,
--     email VARCHAR
-- );


-- ============================================================================
-- 17. MANUTENCAO MANUAL - COMANDOS DE RISCO
-- NAO EXECUTE automaticamente. Faça backup e confira os registros primeiro.
-- ============================================================================

-- Verificar possiveis duplicados em clientes compartilhados:
-- SELECT cpf_cnpj, COUNT(*)
-- FROM clientes_compartilhados
-- GROUP BY cpf_cnpj
-- HAVING COUNT(*) > 1;

-- Verificar possiveis duplicados em clientes dedicados:
-- SELECT cnpj_cpf, COUNT(*)
-- FROM clientes_dedicados
-- GROUP BY cnpj_cpf
-- HAVING COUNT(*) > 1;

-- As exclusoes abaixo foram deixadas desativadas porque podem apagar registros
-- relacionados (ON DELETE CASCADE) e precisam de validacao antes da execucao.
-- DELETE FROM clientes_compartilhados
-- WHERE id IN (
--     SELECT id
--     FROM (
--         SELECT id,
--                ROW_NUMBER() OVER (PARTITION BY cpf_cnpj ORDER BY id) AS rn
--         FROM clientes_compartilhados
--     ) AS duplicados
--     WHERE rn > 1
-- );

-- DELETE FROM clientes_dedicados
-- WHERE id IN (
--     SELECT id
--     FROM (
--         SELECT id,
--                ROW_NUMBER() OVER (PARTITION BY cnpj_cpf ORDER BY id) AS rn
--         FROM clientes_dedicados
--     ) AS duplicados
--     WHERE rn > 1
-- );

-- NAO execute TRUNCATE ou DROP em ambiente com dados sem backup e autorizacao.
-- TRUNCATE TABLE clientes_dedicados RESTART IDENTITY CASCADE;
-- TRUNCATE TABLE clientes_compartilhados RESTART IDENTITY CASCADE;
-- DROP TABLE IF EXISTS clientes_dedicados;
-- DROP TABLE IF EXISTS clientes_compartilhados;


-- ============================================================================
-- FIM DO SCRIPT - PROTON ERP
-- ============================================================================
