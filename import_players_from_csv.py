"""
Import players from CSV file
CSV format: team_name,player_name,jersey_number
Example CSV content:
    Team Alpha,John Doe,1
    Team Alpha,Jane Smith,2
    Team Beta,Mike Johnson,1
"""
from app import app, db
from models import Team, Player
import csv
import sys

def import_from_csv(csv_file):
    """Import players from CSV file"""
    with app.app_context():
        # Get all teams for lookup
        teams = {team.name: team for team in Team.query.all()}
        
        added_count = 0
        skipped_count = 0
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            # Skip header if it exists
            first_row = next(reader, None)
            if first_row and first_row[0].lower() in ['team', 'team_name', 'teamname']:
                print("Skipping header row")
            else:
                # Process first row as data
                if first_row:
                    team_name, player_name = first_row[0], first_row[1]
                    jersey = first_row[2] if len(first_row) > 2 else None
                    
                    if team_name in teams:
                        player = Player(
                            name=player_name,
                            team_id=teams[team_name].id,
                            jersey_number=jersey
                        )
                        db.session.add(player)
                        added_count += 1
                    else:
                        print(f"⚠️  Team not found: {team_name}")
                        skipped_count += 1
            
            # Process remaining rows
            for row in reader:
                if len(row) < 2:
                    continue
                    
                team_name = row[0].strip()
                player_name = row[1].strip()
                jersey_number = row[2].strip() if len(row) > 2 else None
                
                if team_name in teams:
                    player = Player(
                        name=player_name,
                        team_id=teams[team_name].id,
                        jersey_number=jersey_number
                    )
                    db.session.add(player)
                    added_count += 1
                    
                    if added_count % 10 == 0:
                        print(f"Imported {added_count} players...")
                else:
                    print(f"⚠️  Team not found: {team_name}")
                    skipped_count += 1
        
        db.session.commit()
        print("-" * 50)
        print(f"✅ Import complete!")
        print(f"   Added: {added_count} players")
        print(f"   Skipped: {skipped_count} rows")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_players_from_csv.py <csv_file>")
        print("\nCSV Format:")
        print("  team_name,player_name,jersey_number")
        print("\nExample:")
        print("  Team Alpha,John Doe,1")
        print("  Team Alpha,Jane Smith,2")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    print(f"Importing players from: {csv_file}")
    import_from_csv(csv_file)
