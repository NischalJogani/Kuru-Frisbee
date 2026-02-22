"""
Bulk add players to teams
Run this script to automatically generate and add players to all teams
"""
from app import app, db
from models import Team, Player
import random

# Configuration
PLAYERS_PER_TEAM = 18

# Sample first and last names for generating player names
FIRST_NAMES = [
    "Alex", "Jordan", "Casey", "Morgan", "Riley", "Taylor", "Jamie", "Avery",
    "Drew", "Sam", "Charlie", "Blake", "Cameron", "Skyler", "Quinn", "Rowan",
    "Sage", "River", "Dakota", "Parker", "Reese", "Hayden", "Kai", "Phoenix",
    "Elliot", "Emerson", "Finley", "Peyton", "Spencer", "Justice"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Walker", "Hall",
    "Allen", "Young", "King", "Wright", "Scott", "Green", "Baker", "Adams",
    "Nelson", "Carter", "Mitchell", "Roberts", "Turner", "Phillips", "Campbell"
]

def generate_player_name(existing_names):
    """Generate a unique player name"""
    max_attempts = 100
    for _ in range(max_attempts):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        name = f"{first} {last}"
        if name not in existing_names:
            return name
    # Fallback with number
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)} {random.randint(1, 999)}"

def bulk_add_players():
    """Add players to all teams"""
    with app.app_context():
        # Get all teams
        teams = Team.query.all()
        
        if not teams:
            print("❌ No teams found! Please add teams first.")
            return
        
        print(f"Found {len(teams)} teams")
        print("-" * 50)
        
        existing_names = set()
        total_added = 0
        
        for team in teams:
            # Check if team already has players
            existing_count = Player.query.filter_by(team_id=team.id).count()
            
            if existing_count > 0:
                print(f"⚠️  {team.name} already has {existing_count} players")
                response = input(f"   Add {PLAYERS_PER_TEAM} more? (y/n): ").lower()
                if response != 'y':
                    continue
            
            print(f"\n📝 Adding {PLAYERS_PER_TEAM} players to: {team.name}")
            
            for i in range(PLAYERS_PER_TEAM):
                player_name = generate_player_name(existing_names)
                existing_names.add(player_name)
                
                jersey_number = str(i + 1)
                
                player = Player(
                    name=player_name,
                    team_id=team.id,
                    jersey_number=jersey_number
                )
                db.session.add(player)
                total_added += 1
                
                if (i + 1) % 5 == 0:
                    print(f"   Added {i + 1}/{PLAYERS_PER_TEAM} players...")
            
            db.session.commit()
            print(f"   ✅ Completed! {PLAYERS_PER_TEAM} players added to {team.name}")
        
        print("-" * 50)
        print(f"✅ DONE! Total players added: {total_added}")
        print(f"📊 Total players in database: {Player.query.count()}")

if __name__ == "__main__":
    print("=" * 50)
    print("BULK PLAYER ADDITION TOOL")
    print("=" * 50)
    print(f"This will add {PLAYERS_PER_TEAM} players to each team")
    print("Players will have auto-generated names and jersey numbers")
    print("-" * 50)
    
    response = input("Continue? (y/n): ").lower()
    if response == 'y':
        bulk_add_players()
    else:
        print("Cancelled.")
