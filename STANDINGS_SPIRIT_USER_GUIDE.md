# Standings & Spirit of the Game - User Guide

## Quick Start

### For Tournament Participants: Submitting Spirit Scores

1. **Navigate to Spirit Form**
   - Click "Spirit Form" in the main navigation menu
   - URL: `http://yoursite.com/spirit-form`

2. **Fill Out the Form**
   - **Match**: Select the completed match you want to rate
   - **Your Team**: Select your team
   - **Opposing Team**: Select the team you're rating
   - **Day**: Select "Day 1" or "Day 2"
   - **Stage**: Select the stage (Pool, Cross Pool, 5th Place, 3rd Place, or Finals)

3. **Rate the Five Criteria** (1-5 scale)
   - Use the slider for each criterion
   - 1 = Poor, 3 = Average, 5 = Excellent
   - **Rules Knowledge & Use**: Did they know and follow the rules?
   - **Fouls & Body Contact**: Were fouls minimal and contact controlled?
   - **Fair-Mindedness**: Were they fair and objective?
   - **Positive Attitude & Self-Control**: Did they maintain composure?
   - **Communication**: Did they communicate respectfully?

4. **Optional: Add Recognition & Feedback**
   - **MVP Names**: List the most valuable players (comma-separated)
   - **MSP Names**: List the most spirited players (comma-separated)
   - **Feedback**: Add any additional comments

5. **Submit**
   - Click "Submit Spirit Form"
   - You'll see a success message confirming submission

---

### For Spectators/Fans: Viewing Standings

1. **Navigate to Standings**
   - Click "Standings" in the main navigation menu
   - URL: `http://yoursite.com/standings`

2. **View Current Standings**
   - Default tab shows current tournament rankings
   - **#**: Current rank
   - **Team**: Team name
   - **W**: Wins
   - **L**: Losses
   - **Pts For**: Total points scored by team
   - **Pts Against**: Total points allowed by team
   - **Diff**: Point differential (+green, -red)

3. **View Initial Seedings**
   - Click "Initial Seedings" tab
   - Shows pre-tournament seeding/rankings
   - **Seed**: Original seed number
   - **Team**: Team name

4. **View Spirit Rankings**
   - Click "Spirit of the Game" tab
   - Shows teams ranked by average spirit scores
   - **#**: Current spirit rank
   - **Team**: Team name
   - **RK**: Average Rules Knowledge score
   - **FC**: Average Fouls & Body Contact score
   - **FM**: Average Fair-Mindedness score
   - **PA**: Average Positive Attitude score
   - **COM**: Average Communication score
   - **Overall**: Average of all five criteria
   - **Matches**: How many times this team was rated
   - This tab auto-refreshes every 30 seconds

---

### For Tournament Administrators: Setting Seedings

1. **Login as Admin**
   - Go to Admin Login
   - Enter credentials

2. **Navigate to Seeding Management**
   - Click "Admin" in navigation
   - Click "Set Seedings" menu item
   - URL: `http://yoursite.com/admin/seeding`

3. **Enter Seeding Ranks**
   - Each team has a card with an input field
   - Enter the seed number (1 for 1st seed, 2 for 2nd seed, etc.)
   - Leave blank if you don't want to set a seeding

4. **Save**
   - Click "Save Seedings"
   - You'll see a success message
   - Seedings will appear in Standings → Initial Seedings tab

---

## Understanding the Standings

### Current Standings

- **Calculated from**: Match results (wins/losses and points)
- **Updated**: After each match is completed
- **Ranking Logic**:
  1. Most wins
  2. If tied on wins, highest point differential

### Initial Seedings

- **Determined by**: Administrator input
- **Used for**: Pre-tournament predictions/expectations
- **Set before**: Tournament begins
- **Never changes**: During tournament

### Spirit of the Game

- **Calculated from**: Spirit scores submitted by other teams
- **Each team's score**: Average of all ratings they received
- **Updated**: Every 30 seconds when viewing tab
- **Ranking**: Highest average spirit score ranks #1

---

## Frequently Asked Questions

**Q: Can I change my spirit score after submitting?**
A: Not through the form. Contact a tournament administrator.

**Q: What if I don't want to rate all 5 criteria?**
A: All criteria are required - you must rate all 5.

**Q: Can I give spirit scores for a match my team played in?**
A: The form allows it, but it's recommended to only rate opponents (not your own team).

**Q: How often do standings update?**
A: Current standings update after each match completes. Spirit standings auto-refresh every 30 seconds.

**Q: What does "Most Spirited Player" mean?**
A: It's your team's way of recognizing an opponent player who embodied great sportsmanship and spirit.

**Q: Can I see which teams gave my team good/bad scores?**
A: Not through this interface. Scores are aggregated by team.

---

## Tips for Fair Spirit Scoring

1. **Be Consistent**: Rate based on actual observations, not emotions
2. **Be Fair**: Remember that all teams are trying their best
3. **Communicate**: Talk to the other team if something seems unclear
4. **Focus on Intent**: Consider whether infractions were intentional
5. **Recognize Excellence**: Give high scores when teams demonstrate good spirit
6. **Provide Feedback**: Use the feedback field to explain low scores constructively

---

## Technical Notes for Admins

### Database

- All standings data is stored in SQLite database
- Spirit scores are permanently saved
- Seedings can be updated anytime

### Manual Updates

- To manually adjust standings, modify the database directly
- To reset spirit scores, delete from `spirit_score` table
- To reset seedings, delete from `team_seeding` table

### Backup & Recovery

- Regularly backup the `frisbee.db` file
- Keep tournament data safe during the event
- Have a backup device or cloud storage

---

## Support

For technical issues or questions, contact the tournament administrator.
