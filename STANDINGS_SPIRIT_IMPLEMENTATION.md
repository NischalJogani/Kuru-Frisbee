# Standings & Spirit of the Game Implementation

## Overview

This document describes the newly implemented features for tournament standings and Spirit of the Game scoring system.

---

## 1. Database Models

### New Models Added to `models.py`:

#### **TeamSeeding Model**

```python
class TeamSeeding(db.Model):
    - team_id: Foreign key to Team
    - seeding_rank: Integer (1 = first seed, 2 = second seed, etc.)
    - created_at: Timestamp

Purpose: Stores initial tournament seedings/rankings set by admins
```

#### **SpiritScore Model**

```python
class SpiritScore(db.Model):
    - match_id: Foreign key to Match
    - giving_team_id: Team giving the spirit score
    - receiving_team_id: Team receiving the spirit score
    - day: Day of tournament ('day1' or 'day2')
    - stage: Stage of tournament ('pool', 'cross_pool', 'fifth_place', 'third_place', 'finals')

    Criteria (1-5 scale each):
    - rules_knowledge: Rules Knowledge & Use
    - fouls_contact: Fouls & Body Contact
    - fair_mindedness: Fair-Mindedness
    - positive_attitude: Positive Attitude & Self-Control
    - communication: Communication

    Additional Fields:
    - mvp_names: Comma-separated MVP names
    - msp_names: Comma-separated MSP (Most Spirited Players) names
    - feedback: Text feedback/comments
    - created_at: Timestamp

Methods:
    - get_average_score(): Returns average of all 5 criteria
```

---

## 2. Routes & Endpoints

### Public Routes (in `app.py`):

#### **GET /standings**

- Displays 3-tab standings page with:
  - **Current Standings**: Auto-calculated from match results
    - Ranks by wins, then point differential
    - Shows W-L record, points for/against
  - **Initial Seedings**: Pre-tournament rankings
    - Shows seeding rank for each team
  - **Spirit of the Game**: Team rankings by spirit scores
    - Shows average scores for each criterion
    - Shows overall average across all criteria

#### **GET /spirit-form**

- Displays spirit form for submitting spirit scores
- Shows form with:
  - Match selection
  - Team selectors (giving/receiving teams)
  - Day selection (Day 1 or Day 2)
  - Stage selection (Pool, Cross Pool, 5th Place, 3rd Place, Finals)
  - 5-criterion rating sliders (1-5)
  - MVP/MSP name fields
  - Feedback textarea

#### **POST /spirit-form**

- Submits spirit score to database
- Validates that teams are different
- Stores all criteria scores and optional feedback

#### **GET /api/standings/spirit**

- JSON API endpoint for spirit standings
- Returns array of teams with:
  - Team name and ID
  - Average scores for each criterion
  - Overall average
  - Number of matches rated

### Admin Routes:

#### **GET /admin/seeding**

- Admin page to set tournament seedings
- Shows grid of all teams with input fields
- Current seeding values pre-filled if they exist

#### **POST /admin/seeding/update**

- JSON endpoint to save seeding changes
- Accepts team_id → seed_rank mappings
- Creates or updates TeamSeeding records

---

## 3. Templates

### **spirit_form.html**

**Location**: `templates/spirit_form.html`

Features:

- Form sections for match info, criteria, and feedback
- Interactive range sliders with live value display
- Form validation (prevents same team selection)
- Responsive design with CSS Grid
- Support for optional MVP/MSP fields
- Feedback textarea for comments

### **standings.html**

**Location**: `templates/standings.html`

Features:

- **Tab Navigation**:
  - Current Standings tab
  - Initial Seedings tab
  - Spirit of the Game tab
- **Current Standings Table**:
  - Rank, Team Name, Wins, Losses, Pts For, Pts Against, Diff
  - Sorted by wins then point differential
- **Initial Seedings Table**:
  - Seed Number, Team Name
  - Sorted by seed rank
- **Spirit Standings Table**:
  - Rank, Team Name, RK, FC, FM, PA, COM, Overall Average, Match Count
  - Legend explaining criteria abbreviations
  - Sorted by overall average score
  - Auto-refreshes every 30 seconds

### **admin/seeding.html**

**Location**: `templates/admin/seeding.html`

Features:

- Admin interface to set tournament seedings
- Grid layout with cards for each team
- Numeric input fields for seed rank
- Save and reset buttons
- AJAX submission with success feedback
- Responsive design

---

## 4. Updated Files

### **base.html**

Added navigation links:

- `Standings` - Links to public standings page
- `Spirit Form` - Links to spirit score submission form

### **admin/dashboard.html**

Added admin menu item:

- "Set Seedings" - Links to seeding management page

### **models.py**

Added imports:

- `TeamSeeding` and `SpiritScore` classes

### **app.py**

- Updated imports to include new models
- Added 8 new routes/endpoints for standings, spirit forms, and seedings

---

## 5. Data Calculations

### Current Standings Calculation:

```
For each team:
  - Count wins/losses in completed matches
  - Sum total points for and against
  - Calculate point differential (for - against)
  - Sort by: wins DESC, then point_diff DESC
```

### Spirit Standings Calculation:

```
For each team:
  - Retrieve all SpiritScore records where receiving_team_id = team.id
  - Calculate average for each criterion:
    average = sum(criterion_value) / count(scores)
  - Calculate overall average:
    overall = sum(all_criteria_averages) / 5
  - Sort by: overall DESC
```

---

## 6. Usage Flow

### Setting Up Tournament Seedings:

1. Admin logs in
2. Goes to Admin Dashboard → "Set Seedings"
3. Enters seed rank for each team (1, 2, 3, etc.)
4. Clicks "Save Seedings"
5. Seedings appear in Standings → Initial Seedings tab

### Submitting Spirit Scores:

1. User navigates to "Spirit Form" from main nav
2. Selects completed match
3. Selects their team and opposing team
4. Selects day and stage
5. Rates 5 criteria on 1-5 scale
6. Optionally enters MVP/MSP names and feedback
7. Submits form
8. Score is saved to database

### Viewing Standings:

1. User navigates to "Standings" from main nav
2. Default shows "Current Standings" tab
3. Can switch to "Initial Seedings" tab to see pre-tournament rankings
4. Can switch to "Spirit of the Game" tab to see team spirit scores
5. Spirit tab auto-refreshes every 30 seconds for live updates

---

## 7. Features Included

✅ Three distinct ranking systems (Current, Initial, Spirit)
✅ Spirit criteria with 1-5 scale ratings
✅ Dynamic calculation of averages
✅ MVP/MSP recognition system
✅ Optional feedback/comments field
✅ Day and stage tracking for matches
✅ Auto-refresh for spirit standings
✅ Tab-based UI for easy navigation
✅ Responsive design for mobile/tablet
✅ Admin seeding management interface
✅ Form validation and error handling
✅ API endpoint for live data fetching
✅ localStorage for tab preference persistence

---

## 8. API Endpoints Summary

| Method | Endpoint                | Purpose                                 |
| ------ | ----------------------- | --------------------------------------- |
| GET    | `/standings`            | View tournament standings (all 3 tabs)  |
| GET    | `/spirit-form`          | View spirit score submission form       |
| POST   | `/spirit-form`          | Submit spirit score                     |
| GET    | `/admin/seeding`        | View/manage tournament seedings (Admin) |
| POST   | `/admin/seeding/update` | Save seeding changes (Admin)            |
| GET    | `/api/standings/spirit` | Get spirit standings JSON               |

---

## 9. CSS Styling Included

All templates include embedded CSS with:

- Color-coded criteria rating sliders
- Responsive grid layouts
- Tab navigation styling
- Table styling with hover effects
- Seed badge styling
- Team badge styling
- Legend and help text styling
- Mobile-responsive breakpoints
- Dark mode support (uses CSS variables)

---

## 10. Database Schema Changes

**New Tables Created**:

1. `team_seeding` - Stores tournament seedings
2. `spirit_score` - Stores spirit of the game scores

**No existing tables were modified** - All changes are additive.

---

## Testing Checklist

- [x] App starts without errors
- [x] Spirit form page loads (HTTP 200)
- [x] Standings page loads (HTTP 200)
- [x] Models validate (no syntax errors)
- [x] New routes are registered
- [x] Templates render without errors
- [x] Navigation links added successfully

---

## Next Steps (Optional Enhancements)

1. Add export functionality for standings (PDF/CSV)
2. Add email notifications when spirit scores are submitted
3. Create detailed spirit score breakdown view per team
4. Add historical standings comparisons
5. Create admin reports for tournament organizers
6. Add team photos to standings display
7. Create mobile app for easier spirit form submission
8. Add email reminders to submit spirit forms after matches
