from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(db.Model):
    """Admin user model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class Team(db.Model):
    """Team model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    players = db.relationship('Player', backref='team', lazy=True, cascade='all, delete-orphan')
    home_matches = db.relationship('Match', foreign_keys='Match.team1_id', backref='team1', lazy=True)
    away_matches = db.relationship('Match', foreign_keys='Match.team2_id', backref='team2', lazy=True)
    
    def __repr__(self):
        return f'<Team {self.name}>'

class Player(db.Model):
    """Player model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    jersey_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships - specify foreign_keys to avoid ambiguity
    scores = db.relationship('Score', foreign_keys='Score.player_id', backref='player', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert player to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'team_id': self.team_id,
            'team_name': self.team.name if self.team else None,
            'jersey_number': self.jersey_number
        }
    
    def __repr__(self):
        return f'<Player {self.name}>'

class Match(db.Model):
    """Match model"""
    id = db.Column(db.Integer, primary_key=True)
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team1_score = db.Column(db.Integer, default=0)
    team2_score = db.Column(db.Integer, default=0)
    match_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    status = db.Column(db.String(20), default='scheduled')  # scheduled, live, completed
    match_stage = db.Column(db.String(30), default='Pool Stage')  # Pool Stage, Cross Pool, 5th Place Game, 3rd Place Game, Finals
    duration_minutes = db.Column(db.Integer, default=60)  # 60, 75, or 90 minutes
    max_score = db.Column(db.Integer, default=15)  # Game to X points
    start_time = db.Column(db.DateTime, nullable=True)  # When match actually started
    current_offense_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)  # Team on offense
    current_defense_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)  # Team on defense
    gender_ratio = db.Column(db.String(20), nullable=True)  # '4:3_boys' or '4:3_girls'
    total_points_played = db.Column(db.Integer, default=0)  # Track total points for ratio switching
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    scores = db.relationship('Score', backref='match', lazy=True, cascade='all, delete-orphan')
    offense_team = db.relationship('Team', foreign_keys=[current_offense_team_id], backref=db.backref('offense_matches', lazy=True))
    defense_team = db.relationship('Team', foreign_keys=[current_defense_team_id], backref=db.backref('defense_matches', lazy=True))
    
    def get_current_ratio(self):
        """Get current gender ratio for both teams based on points played"""
        if not self.gender_ratio:
            return {'team1': None, 'team2': None}
        
        points = self.total_points_played
        
        # Determine how many switches have occurred
        # Switch at points: 1, 3, 5, 7, 9... (odd numbers)
        # At point 0: both teams have original ratio
        # At point 1: switch
        # At points 2: same as point 1
        # At point 3: switch back
        # At points 4: same as point 3
        # etc.
        
        # Calculate number of switches: happens at odd points
        # For points 0: 0 switches
        # For points 1-2: 1 switch
        # For points 3-4: 2 switches
        # For points 5-6: 3 switches
        num_switches = (points + 1) // 2 if points > 0 else 0
        
        # Determine if we should use original or opposite ratio
        use_opposite = (num_switches % 2) == 1
        
        if use_opposite:
            # Teams have opposite ratios
            if self.gender_ratio == '4:3_boys':
                return {'team1': '4:3_girls', 'team2': '4:3_girls'}
            else:
                return {'team1': '4:3_boys', 'team2': '4:3_boys'}
        else:
            # Teams have original ratio
            return {'team1': self.gender_ratio, 'team2': self.gender_ratio}
    
    def __repr__(self):
        return f'<Match {self.team1.name} vs {self.team2.name}>'

class Score(db.Model):
    """Score model - individual scoring events"""
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    action_type = db.Column(db.String(20), nullable=False)  # 'score', 'defense'
    points = db.Column(db.Integer, default=1)
    assist_player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)  # Only for 'score' type
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship for assist
    assist_by = db.relationship('Player', foreign_keys=[assist_player_id], backref=db.backref('assists', lazy='dynamic'), post_update=True)
    
    def __repr__(self):
        return f'<Score {self.player.name} - {self.action_type}>'

class TeamSeeding(db.Model):
    """Initial tournament seeding/ranking for teams"""
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id', ondelete='CASCADE'), nullable=False, unique=True)
    seeding_rank = db.Column(db.Integer, nullable=False)  # 1 for 1st seed, 2 for 2nd seed, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    team = db.relationship('Team', backref=db.backref('seeding', uselist=False, lazy=True, cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f'<TeamSeeding {self.team.name} - Seed #{self.seeding_rank}>'

class SpiritScore(db.Model):
    """Spirit of the Game scores awarded to teams after matches"""
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    giving_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)  # Team giving the score
    receiving_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)  # Team receiving the score
    
    # Match details
    day = db.Column(db.String(20), nullable=False)  # 'day1', 'day2'
    stage = db.Column(db.String(20), nullable=False)  # 'pool', 'cross_pool', 'fifth_place', 'third_place', 'finals'
    
    # Spirit criteria (1-5 scale)
    rules_knowledge = db.Column(db.Integer, nullable=False)  # Rules Knowledge & Use
    fouls_contact = db.Column(db.Integer, nullable=False)  # Fouls & Body Contact
    fair_mindedness = db.Column(db.Integer, nullable=False)  # Fair-Mindedness
    positive_attitude = db.Column(db.Integer, nullable=False)  # Positive Attitude & Self-Control
    communication = db.Column(db.Integer, nullable=False)  # Communication
    
    # MVPs and MSPs
    mvp_names = db.Column(db.Text, nullable=True)  # Comma-separated MVP names
    msp_names = db.Column(db.Text, nullable=True)  # Comma-separated MSP (Most Spirited Player) names
    
    # Feedback
    feedback = db.Column(db.Text, nullable=True)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    match = db.relationship('Match', backref=db.backref('spirit_scores', lazy=True, cascade='all, delete-orphan'))
    giving_team = db.relationship('Team', foreign_keys=[giving_team_id], backref=db.backref('spirit_scores_given', lazy=True))
    receiving_team = db.relationship('Team', foreign_keys=[receiving_team_id], backref=db.backref('spirit_scores_received', lazy=True))
    
    def get_average_score(self):
        """Calculate average spirit score"""
        scores = [
            self.rules_knowledge,
            self.fouls_contact,
            self.fair_mindedness,
            self.positive_attitude,
            self.communication
        ]
        return sum(scores) / len(scores) if scores else 0
    
    def __repr__(self):
        return f'<SpiritScore {self.giving_team.name} -> {self.receiving_team.name}>'
