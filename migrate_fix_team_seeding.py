"""
Migration script to fix team_seeding foreign key constraint.
This adds CASCADE behavior to the team_id foreign key.
"""
from app import app, db
from models import Team, Player, Match, Score, TeamSeeding, SpiritScore, Admin
import os
import shutil
from datetime import datetime

def backup_database():
    """Create a backup of the current database"""
    db_path = 'instance/frisbee.db'
    if os.path.exists(db_path):
        backup_path = f'instance/frisbee_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        shutil.copy2(db_path, backup_path)
        print(f"✓ Database backed up to: {backup_path}")
        return backup_path
    return None

def migrate():
    """Perform the migration"""
    with app.app_context():
        print("Starting migration to fix team_seeding foreign key constraint...")
        
        # Backup database
        backup_path = backup_database()
        
        # Store all existing data
        print("Reading existing data...")
        teams_data = []
        for team in Team.query.all():
            teams_data.append({
                'id': team.id,
                'name': team.name,
                'created_at': team.created_at
            })
        
        players_data = []
        for player in Player.query.all():
            players_data.append({
                'id': player.id,
                'name': player.name,
                'team_id': player.team_id,
                'jersey_number': player.jersey_number,
                'created_at': player.created_at
            })
        
        seeding_data = []
        for seeding in TeamSeeding.query.all():
            seeding_data.append({
                'id': seeding.id,
                'team_id': seeding.team_id,
                'seeding_rank': seeding.seeding_rank,
                'created_at': seeding.created_at
            })
        
        matches_data = []
        for match in Match.query.all():
            matches_data.append({
                'id': match.id,
                'team1_id': match.team1_id,
                'team2_id': match.team2_id,
                'team1_score': match.team1_score,
                'team2_score': match.team2_score,
                'match_date': match.match_date,
                'location': match.location,
                'status': match.status,
                'match_stage': match.match_stage,
                'duration_minutes': match.duration_minutes,
                'max_score': match.max_score,
                'start_time': match.start_time,
                'current_offense_team_id': match.current_offense_team_id,
                'current_defense_team_id': match.current_defense_team_id,
                'gender_ratio': match.gender_ratio,
                'total_points_played': match.total_points_played,
                'created_at': match.created_at
            })
        
        scores_data = []
        for score in Score.query.all():
            scores_data.append({
                'id': score.id,
                'match_id': score.match_id,
                'player_id': score.player_id,
                'action_type': score.action_type,
                'points': score.points,
                'assist_player_id': score.assist_player_id,
                'timestamp': score.timestamp
            })
        
        spirit_scores_data = []
        for spirit in SpiritScore.query.all():
            spirit_scores_data.append({
                'id': spirit.id,
                'match_id': spirit.match_id,
                'giving_team_id': spirit.giving_team_id,
                'receiving_team_id': spirit.receiving_team_id,
                'day': spirit.day,
                'stage': spirit.stage,
                'rules_knowledge': spirit.rules_knowledge,
                'fouls_contact': spirit.fouls_contact,
                'fair_mindedness': spirit.fair_mindedness,
                'positive_attitude': spirit.positive_attitude,
                'communication': spirit.communication,
                'mvp_names': spirit.mvp_names,
                'msp_names': spirit.msp_names,
                'feedback': spirit.feedback,
                'created_at': spirit.created_at
            })
        
        admins_data = []
        for admin in Admin.query.all():
            admins_data.append({
                'id': admin.id,
                'username': admin.username,
                'password_hash': admin.password_hash,
                'created_at': admin.created_at
            })
        
        print(f"✓ Found {len(teams_data)} teams, {len(players_data)} players, {len(seeding_data)} seedings")
        print(f"✓ Found {len(matches_data)} matches, {len(scores_data)} scores, {len(spirit_scores_data)} spirit scores")
        print(f"✓ Found {len(admins_data)} admin users")
        
        # Drop and recreate all tables
        print("Recreating database schema...")
        db.drop_all()
        db.create_all()
        print("✓ Database schema recreated")
        
        # Restore data
        print("Restoring data...")
        
        # Restore admins first
        for admin_dict in admins_data:
            admin = Admin(
                id=admin_dict['id'],
                username=admin_dict['username'],
                created_at=admin_dict['created_at']
            )
            admin.password_hash = admin_dict['password_hash']  # Set directly to preserve hash
            db.session.add(admin)
        
        # Restore teams
        for team_dict in teams_data:
            team = Team(
                id=team_dict['id'],
                name=team_dict['name'],
                created_at=team_dict['created_at']
            )
            db.session.add(team)
        
        # Restore seeding
        for seeding_dict in seeding_data:
            seeding = TeamSeeding(
                id=seeding_dict['id'],
                team_id=seeding_dict['team_id'],
                seeding_rank=seeding_dict['seeding_rank'],
                created_at=seeding_dict['created_at']
            )
            db.session.add(seeding)
        
        # Restore players
        for player_dict in players_data:
            player = Player(
                id=player_dict['id'],
                name=player_dict['name'],
                team_id=player_dict['team_id'],
                jersey_number=player_dict['jersey_number'],
                created_at=player_dict['created_at']
            )
            db.session.add(player)
        
        # Restore matches
        for match_dict in matches_data:
            match = Match(
                id=match_dict['id'],
                team1_id=match_dict['team1_id'],
                team2_id=match_dict['team2_id'],
                team1_score=match_dict['team1_score'],
                team2_score=match_dict['team2_score'],
                match_date=match_dict['match_date'],
                location=match_dict['location'],
                status=match_dict['status'],
                match_stage=match_dict['match_stage'],
                duration_minutes=match_dict['duration_minutes'],
                max_score=match_dict['max_score'],
                start_time=match_dict['start_time'],
                current_offense_team_id=match_dict['current_offense_team_id'],
                current_defense_team_id=match_dict['current_defense_team_id'],
                gender_ratio=match_dict['gender_ratio'],
                total_points_played=match_dict['total_points_played'],
                created_at=match_dict['created_at']
            )
            db.session.add(match)
        
        # Restore scores
        for score_dict in scores_data:
            score = Score(
                id=score_dict['id'],
                match_id=score_dict['match_id'],
                player_id=score_dict['player_id'],
                action_type=score_dict['action_type'],
                points=score_dict['points'],
                assist_player_id=score_dict['assist_player_id'],
                timestamp=score_dict['timestamp']
            )
            db.session.add(score)
        
        # Restore spirit scores
        for spirit_dict in spirit_scores_data:
            spirit = SpiritScore(
                id=spirit_dict['id'],
                match_id=spirit_dict['match_id'],
                giving_team_id=spirit_dict['giving_team_id'],
                receiving_team_id=spirit_dict['receiving_team_id'],
                day=spirit_dict['day'],
                stage=spirit_dict['stage'],
                rules_knowledge=spirit_dict['rules_knowledge'],
                fouls_contact=spirit_dict['fouls_contact'],
                fair_mindedness=spirit_dict['fair_mindedness'],
                positive_attitude=spirit_dict['positive_attitude'],
                communication=spirit_dict['communication'],
                mvp_names=spirit_dict['mvp_names'],
                msp_names=spirit_dict['msp_names'],
                feedback=spirit_dict['feedback'],
                created_at=spirit_dict['created_at']
            )
            db.session.add(spirit)
        
        db.session.commit()
        print("✓ All data restored successfully")
        
        print("\n✅ Migration completed successfully!")
        print(f"Backup location: {backup_path}")
        print("\nThe team deletion issue has been fixed. You can now delete teams without errors.")

if __name__ == '__main__':
    migrate()
