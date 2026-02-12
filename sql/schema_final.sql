-- ============================================================================
-- SCHÉMA RELATIONNEL OPTIMISÉ — ROCKET LEAGUE ANALYTICS
-- ============================================================================
-- Architecture: Dimensions autour + 1 table de stats centrale
-- Flexible et scalable
-- ============================================================================

-- ============================================================================
-- DIMENSIONS ESSENTIELLES
-- ============================================================================

CREATE TABLE IF NOT EXISTS Country (
    country_id TEXT PRIMARY KEY,
    country_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Region (
    region_id TEXT PRIMARY KEY,
    region_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Player (
    player_id TEXT PRIMARY KEY,
    team_id TEXT,
    player_tag TEXT NOT NULL,
    player_name TEXT,
    country_id TEXT,
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
    FOREIGN KEY (country_id) REFERENCES Country(country_id)
);

CREATE TABLE IF NOT EXISTS Team (
    team_id TEXT PRIMARY KEY,
    team_name TEXT NOT NULL,
    region_id TEXT,
    FOREIGN KEY (region_id) REFERENCES Region(region_id)
);

CREATE TABLE IF NOT EXISTS Match (
    match_id TEXT PRIMARY KEY,
    map_id TEXT,
    match_date TIMESTAMP,
    match_format TEXT,
    event_id TEXT,
    FOREIGN KEY (map_id) REFERENCES Map(map_id),
    FOREIGN KEY (event_id) REFERENCES Event(event_id)
);

CREATE TABLE IF NOT EXISTS Map (
    map_id TEXT PRIMARY KEY,
    map_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Score (
    score_id TEXT PRIMARY KEY,
    team_id TEXT,
    match_id TEXT,
    score DOUBLE,
    winner BOOLEAN,
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
    FOREIGN KEY (match_id) REFERENCES Match(match_id)
);

CREATE TABLE IF NOT EXISTS Event (
    event_id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    region_id TEXT,
    event_tier TEXT,
    FOREIGN KEY (region_id) REFERENCES Region(region_id)
);

-- ============================================================================
-- TABLE CENTRALE DE STATS
-- ============================================================================

CREATE TABLE IF NOT EXISTS StatMapping (
    stat_id TEXT PRIMARY KEY,
    entity_id TEXT,  -- player_id, team_id, ou match_id
    entity_type TEXT,  -- 'player', 'team', 'match'
    game_id TEXT,
    type_id TEXT
);

-- ============================================================================
-- TABLE DES TYPES DE STATS
-- ============================================================================

CREATE TABLE IF NOT EXISTS Stat (
    stat_id TEXT PRIMARY KEY,
    type_id TEXT,
    stat_value DOUBLE,
    FOREIGN KEY (type_id) REFERENCES StatType(type_id)
);

CREATE TABLE IF NOT EXISTS StatType (
    type_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT  -- 'CORE', 'BOOST', 'MOVEMENT', 'POSITIONING', 'DEMO', 'ADVANCED'
);

-- ============================================================================
-- INDEX POUR PERFORMANCES
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_player_team ON Player(team_id);
CREATE INDEX IF NOT EXISTS idx_player_country ON Player(country_id);
CREATE INDEX IF NOT EXISTS idx_team_region ON Team(region_id);
CREATE INDEX IF NOT EXISTS idx_event_region ON Event(region_id);
CREATE INDEX IF NOT EXISTS idx_match_map ON Match(map_id);
CREATE INDEX IF NOT EXISTS idx_match_event ON Match(event_id);
CREATE INDEX IF NOT EXISTS idx_score_team ON Score(team_id);
CREATE INDEX IF NOT EXISTS idx_score_match ON Score(match_id);
CREATE INDEX IF NOT EXISTS idx_statmapping_entity ON StatMapping(entity_id, entity_type);
CREATE INDEX IF NOT EXISTS idx_statmapping_type ON StatMapping(type_id);
CREATE INDEX IF NOT EXISTS idx_stat_type ON Stat(type_id);

-- ============================================================================
-- VUES
-- ============================================================================

-- Vue: Stats d'un joueur
CREATE OR REPLACE VIEW V_Player_Stats AS
SELECT 
    p.player_id,
    p.player_tag,
    p.team_id,
    t.team_name,
    sm.game_id,
    st.name AS stat_name,
    st.category,
    s.stat_value
FROM StatMapping sm
JOIN StatType st ON sm.type_id = st.type_id
JOIN Stat s ON sm.stat_id = s.stat_id
JOIN Player p ON sm.entity_id = p.player_id AND sm.entity_type = 'player'
JOIN Team t ON p.team_id = t.team_id
ORDER BY p.player_tag, sm.game_id, st.name;

-- Vue: Stats d'une équipe
CREATE OR REPLACE VIEW V_Team_Stats AS
SELECT 
    t.team_id,
    t.team_name,
    t.team_region,
    sm.game_id,
    st.name AS stat_name,
    st.category,
    s.stat_value
FROM StatMapping sm
JOIN StatType st ON sm.type_id = st.type_id
JOIN Stat s ON sm.stat_id = s.stat_id
JOIN Team t ON sm.entity_id = t.team_id AND sm.entity_type = 'team'
ORDER BY t.team_name, sm.game_id, st.name;

-- Vue: Stats d'un match
CREATE OR REPLACE VIEW V_Match_Stats AS
SELECT 
    m.match_id,
    m.match_date,
    m.match_format,
    ma.map_name,
    sm.entity_type,
    sm.entity_id,
    st.name AS stat_name,
    st.category,
    s.stat_value
FROM StatMapping sm
JOIN StatType st ON sm.type_id = st.type_id
JOIN Stat s ON sm.stat_id = s.stat_id
JOIN Match m ON sm.game_id LIKE CONCAT(m.match_id, '%') OR m.match_id = sm.game_id
LEFT JOIN Map ma ON m.map_id = ma.map_id
ORDER BY m.match_date, st.name;
