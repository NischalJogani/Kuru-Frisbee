"""
Database migration script to add match_stage column to Match table
Run this script once to update your existing database
"""
import sqlite3
import os

def migrate_database():
    db_path = 'instance/frisbee.db'
    
    if not os.path.exists(db_path):
        print("Database not found. No migration needed - it will be created with the new schema.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(match)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'match_stage' in columns:
            print("✓ Column 'match_stage' already exists. No migration needed.")
        else:
            # Add the new column with a default value
            cursor.execute("""
                ALTER TABLE match 
                ADD COLUMN match_stage VARCHAR(30) DEFAULT 'Pool Stage'
            """)
            conn.commit()
            print("✓ Successfully added 'match_stage' column to match table")
            print("  All existing matches have been set to 'Pool Stage'")
        
    except Exception as e:
        print(f"✗ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Running database migration...")
    migrate_database()
    print("Migration complete!")
