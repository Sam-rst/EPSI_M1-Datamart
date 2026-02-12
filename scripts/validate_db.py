#!/usr/bin/env python3
"""
Validate the DuckDB database and display statistics about the imported data.
"""
from pathlib import Path
import json
import sys

try:
    import duckdb
except Exception:
    print('❌ duckdb not installed. Run: pip install duckdb')
    sys.exit(1)

def main():
    repo = Path.cwd()
    
    # Chemin vers la base de données
    db_path = repo / 'data' / 'rl.duckdb'
    
    # Fallback vers l'ancienne structure
    if not db_path.exists():
        db_path = repo / 'Atelier1' / 'data' / 'rl.duckdb'
    
    if not db_path.exists():
        print(f'❌ Base de données introuvable : {db_path}')
        print('   Exécutez d\'abord : python scripts/ingest_duckdb.py')
        sys.exit(1)

    print('📊 Validation de la base DuckDB...')
    print(f'   Base : {db_path}')
    print(f'   Taille : {db_path.stat().st_size / (1024*1024):.2f} MB\n')
    
    conn = duckdb.connect(database=str(db_path), read_only=True)
    
    checks = []
    
    # 1. Compter les lignes par table
    print('=' * 60)
    print('📋 NOMBRE DE LIGNES PAR TABLE')
    print('=' * 60)
    
    tables = ['players_db', 'main', 'games_by_players', 'games_by_teams', 
              'matches_by_players', 'matches_by_teams']
    
    total_rows = 0
    for tbl in tables:
        try:
            cnt = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            total_rows += cnt
            print(f'✓ {tbl:<25} {cnt:>10,} lignes')
            checks.append({'check': 'row_count', 'table': tbl, 'count': cnt})
        except Exception as e:
            print(f'❌ {tbl:<25} ERREUR: {e}')
            checks.append({'check': 'row_count', 'table': tbl, 'error': str(e)})
    
    print('=' * 60)
    print(f'   TOTAL                      {total_rows:>10,} lignes')
    print('=' * 60)
    
    # 2. Vérifier les valeurs nulles dans les colonnes clés
    print('\n🔍 VÉRIFICATION DES VALEURS NULLES DANS LES CLÉS')
    print('=' * 60)
    
    key_cols = {
        'games_by_players': ['game_id', 'player_id', 'team_id'],
        'matches_by_players': ['match_id', 'player_id', 'team_id'],
        'main': ['game_id', 'match_id'],
    }
    
    null_found = False
    for tbl, cols in key_cols.items():
        for c in cols:
            try:
                nulls = conn.execute(
                    f"SELECT SUM(CASE WHEN {c} IS NULL OR {c} = '' THEN 1 ELSE 0 END) FROM {tbl}"
                ).fetchone()[0]
                checks.append({'check': 'null_count', 'table': tbl, 'column': c, 'nulls': nulls})
                
                if nulls and nulls > 0:
                    print(f'⚠️  {tbl}.{c}: {nulls} valeurs nulles/vides')
                    null_found = True
            except Exception as e:
                print(f'❌ Erreur sur {tbl}.{c}: {e}')
    
    if not null_found:
        print('✓ Aucune valeur nulle trouvée dans les colonnes clés')
    
    # 3. Intégrité référentielle : joueurs dans players_db
    print('\n🔗 VÉRIFICATION DE L\'INTÉGRITÉ RÉFÉRENTIELLE')
    print('=' * 60)
    
    try:
        missing = conn.execute("""
            SELECT COUNT(DISTINCT gp.player_id) 
            FROM games_by_players gp 
            LEFT JOIN players_db p ON gp.player_id = p.player_id 
            WHERE p.player_id IS NULL
        """).fetchone()[0]
        
        checks.append({'check': 'missing_players', 'missing_count': missing})
        
        if missing == 0:
            print('✓ Tous les joueurs référencés existent dans players_db')
        else:
            print(f'⚠️  {missing} joueurs référencés sont absents de players_db')
    except Exception as e:
        print(f'❌ Erreur lors de la vérification: {e}')
    
    # 4. Distribution des plateformes
    print('\n🎮 DISTRIBUTION DES PLATEFORMES')
    print('=' * 60)
    
    try:
        platforms = conn.execute("""
            SELECT 
                COALESCE(platform, 'non spécifié') as platform, 
                COUNT(*) as count
            FROM games_by_players 
            GROUP BY platform 
            ORDER BY count DESC
        """).fetchall()
        
        for platform, count in platforms:
            print(f'  {platform:<20} {count:>10,} entrées')
            
        checks.append({'check': 'platform_distribution', 'result': [(p, c) for p, c in platforms]})
    except Exception as e:
        print(f'❌ Erreur: {e}')
    
    # 5. Top 5 joueurs les plus actifs
    print('\n🏆 TOP 5 JOUEURS LES PLUS ACTIFS')
    print('=' * 60)
    
    try:
        top_players = conn.execute("""
            SELECT p.player_name, COUNT(*) as nb_games
            FROM games_by_players g
            JOIN players_db p ON g.player_id = p.player_id
            WHERE p.player_name IS NOT NULL
            GROUP BY p.player_name
            ORDER BY nb_games DESC
            LIMIT 5
        """).fetchall()
        
        for idx, (name, count) in enumerate(top_players, 1):
            print(f'  {idx}. {name:<30} {count:>5} parties')
    except Exception as e:
        print(f'❌ Erreur: {e}')
    
    conn.close()
    
    # Sauvegarder le rapport JSON
    report_path = repo / 'validation_report.json'
    with report_path.open('w', encoding='utf-8') as f:
        json.dump({'db': str(db_path), 'checks': checks}, f, ensure_ascii=False, indent=2)
    
    print('\n' + '=' * 60)
    print('✅ Validation terminée')
    print(f'   Rapport JSON sauvegardé : {report_path}')
    print('=' * 60)

if __name__ == '__main__':
    main()
