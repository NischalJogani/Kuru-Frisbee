# Nischal Instructions

create virtual env: python3 -m venv venv
actvate: ./venv/Scripts/activate
run: python3 app.py








# 🥏 Frisbee Live Tracker

A comprehensive live frisbee score tracking and leaderboard application built with Flask, Python, HTML, and CSS.

## Features

### Public Features
- **Live Match Tracking** - View live scores with real-time updates
- **Leaderboard** - Top 10 players ranked by total points
- **Match Schedule** - See upcoming, live, and completed matches
- **Responsive Design** - Optimized for both laptop and mobile devices

### Admin Features
- **Team Management** - Register and manage teams
- **Player Management** - Add players to teams with jersey numbers
- **Match Scheduling** - Schedule matches between teams
- **Live Scoring Interface** - Quick score updates with player tracking
- **Match Status Control** - Set matches as scheduled, live, or completed
- **Score History** - View and undo scoring events

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Navigate to the project directory**
   ```bash
   cd frisbee
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to: `http://localhost:5000`
   - Admin dashboard: `http://localhost:5000/admin`

## Usage Guide

### First Time Setup

1. **Add Teams**
   - Go to Admin → Manage Teams
   - Add all participating teams

2. **Add Players**
   - Go to Admin → Manage Players
   - Register players and assign them to teams
   - Optionally add jersey numbers

3. **Schedule Matches**
   - Go to Admin → Manage Matches
   - Create matches between teams
   - Set date, time, and location

### During a Match

1. **Start the Match**
   - Go to Admin → Manage Matches
   - Change match status to "Live"

2. **Score the Match**
   - Click "Score" button on the match
   - Click player buttons to add points
   - Scores update in real-time
   - Use "Undo" to remove incorrect scores

3. **Complete the Match**
   - Change match status to "Completed" when done

### Viewing Live Scores

- Public users can visit the home page to:
  - See live match scores (updates every 5 seconds)
  - View the leaderboard (top 10 players)
  - Check upcoming and completed matches
  - Click on live matches for detailed view

## Project Structure

```
frisbee/
├── app.py                      # Main Flask application with routes
├── models.py                   # Database models (Team, Player, Match, Score)
├── requirements.txt            # Python dependencies
├── frisbee.db                  # SQLite database (auto-created)
├── static/
│   ├── css/
│   │   └── style.css          # Responsive CSS styling
│   └── js/
│       └── main.js            # JavaScript for live updates
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Public home page
    ├── match_detail.html      # Live match detail view
    └── admin/
        ├── dashboard.html     # Admin dashboard
        ├── teams.html         # Team management
        ├── players.html       # Player management
        ├── matches.html       # Match management
        └── live_scoring.html  # Live scoring interface
```

## Database Schema

### Team
- id, name, created_at

### Player
- id, name, team_id, jersey_number, created_at

### Match
- id, team1_id, team2_id, team1_score, team2_score, match_date, location, status, created_at

### Score
- id, match_id, player_id, points, timestamp

## API Endpoints

### Public
- `GET /` - Home page with matches and leaderboard
- `GET /match/<id>` - Live match detail page
- `GET /api/match/<id>/scores` - JSON API for live score updates

### Admin
- `GET /admin` - Admin dashboard
- `GET /admin/teams` - Manage teams
- `POST /admin/teams/add` - Add new team
- `POST /admin/teams/delete/<id>` - Delete team
- `GET /admin/players` - Manage players
- `POST /admin/players/add` - Add new player
- `POST /admin/players/delete/<id>` - Delete player
- `GET /admin/matches` - Manage matches
- `POST /admin/matches/add` - Schedule new match
- `POST /admin/matches/update_status/<id>` - Update match status
- `POST /admin/matches/delete/<id>` - Delete match
- `GET /admin/scoring/<id>` - Live scoring interface
- `POST /admin/scoring/<id>/add` - Add score
- `POST /admin/scoring/<id>/undo/<score_id>` - Undo score

## Features Details

### Live Updates
- Match detail pages auto-refresh every 3-5 seconds when a match is live
- Scoring interface refreshes automatically
- Uses AJAX for smooth updates without page reload

### Responsive Design
- Mobile-first approach
- Optimized layouts for:
  - Mobile phones (< 480px)
  - Tablets (480px - 768px)
  - Laptops (> 768px)

### Leaderboard System
- Automatically calculates player rankings
- Ranks players by total points across all matches
- Highlights top 3 with medals (🥇🥈🥉)

### Match Status System
- **Scheduled** - Future matches
- **Live** - Currently ongoing matches
- **Completed** - Finished matches

## Customization

### Changing Colors
Edit variables in [static/css/style.css](static/css/style.css):
```css
:root {
    --primary-color: #2563eb;
    --live-color: #dc2626;
    /* ... more colors */
}
```

### Adjusting Auto-Refresh Rate
In templates, modify the `setInterval` value (in milliseconds):
```javascript
setInterval(function() {
    location.reload();
}, 3000); // 3 seconds
```

## Troubleshooting

### Database Issues
If you encounter database errors, delete `frisbee.db` and restart the app to recreate it.

### Port Already in Use
Change the port in [app.py](app.py):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Styles Not Loading
Clear browser cache or do a hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

## Security Note

This application is designed without authentication for simplicity. For production use:
- Add user authentication for admin routes
- Implement CSRF protection
- Add input validation and sanitization
- Use environment variables for configuration
- Enable HTTPS

## Future Enhancements

Possible additions:
- User authentication system
- Team statistics and analytics
- Player performance graphs
- Export match reports to PDF
- Email notifications for matches
- Mobile app version
- Multi-tournament support
- Photo uploads for teams/players

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions, please check the code comments or modify as needed for your specific requirements.

---

**Built with ❤️ for Frisbee enthusiasts**
