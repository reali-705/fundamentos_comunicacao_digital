CREATE TABLE IF NOT EXISTS tb_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Dados de Entrada
    entrada_comunicacao TEXT NOT NULL,
    tpcomunicacao TEXT NOT NULL CHECK (tpcomunicacao IN ('EMISSOR', 'RECEPTOR')),
    
    -- Status e Saída
    status_mensagem INTEGER NOT NULL CHECK (status_mensagem IN (0, 1)), -- 0: Erro, 1: Sucesso
    saida_comunicacao TEXT NOT NULL,
    tpsaida TEXT NOT NULL CHECK (tpsaida IN ('TEXTO', 'MORSE')),
    
    -- Arquivos e Tempo
    logging_path VARCHAR(255),
    data_evento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);