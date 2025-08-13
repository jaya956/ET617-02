#!/usr/bin/env python3
"""
Database Viewer for Learning Website Clickstream Data
This script allows you to view and analyze the data collected by the learning website.
"""

import sqlite3
import json
from datetime import datetime
import sys

def connect_db():
    """Connect to the SQLite database"""
    try:
        conn = sqlite3.connect('learning_website.db')
        conn.row_factory = sqlite3.Row  # This allows column access by name
        return conn
    except sqlite3.OperationalError:
        print("Error: Could not connect to database. Make sure the Flask app has been run at least once.")
        sys.exit(1)

def view_users(conn):
    """Display all registered users"""
    print("\n" + "="*50)
    print("REGISTERED USERS")
    print("="*50)
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, created_at FROM user")
    users = cursor.fetchall()
    
    if not users:
        print("No users found.")
        return
    
    for user in users:
        print(f"ID: {user['id']}")
        print(f"Username: {user['username']}")
        print(f"Email: {user['email']}")
        print(f"Created: {user['created_at']}")
        print("-" * 30)

def view_courses(conn):
    """Display all courses"""
    print("\n" + "="*50)
    print("COURSES")
    print("="*50)
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, created_at FROM course")
    courses = cursor.fetchall()
    
    if not courses:
        print("No courses found.")
        return
    
    for course in courses:
        print(f"ID: {course['id']}")
        print(f"Title: {course['title']}")
        print(f"Description: {course['description']}")
        print(f"Created: {course['created_at']}")
        print("-" * 30)

def view_lessons(conn):
    """Display all lessons"""
    print("\n" + "="*50)
    print("LESSONS")
    print("="*50)
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.id, l.title, l.content_type, l.content, c.title as course_title 
        FROM lesson l 
        JOIN course c ON l.course_id = c.id
        ORDER BY l.course_id, l.order
    """)
    lessons = cursor.fetchall()
    
    if not lessons:
        print("No lessons found.")
        return
    
    for lesson in lessons:
        print(f"ID: {lesson['id']}")
        print(f"Title: {lesson['title']}")
        print(f"Type: {lesson['content_type']}")
        print(f"Course: {lesson['course_title']}")
        print(f"Content: {lesson['content'][:100]}...")
        print("-" * 30)

def view_clickstream_events(conn, limit=20):
    """Display recent clickstream events"""
    print(f"\n" + "="*50)
    print(f"RECENT CLICKSTREAM EVENTS (Last {limit})")
    print("="*50)
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ce.*, u.username 
        FROM clickstream_event ce 
        LEFT JOIN user u ON ce.user_id = u.id
        ORDER BY ce.timestamp DESC 
        LIMIT ?
    """, (limit,))
    events = cursor.fetchall()
    
    if not events:
        print("No clickstream events found.")
        return
    
    for event in events:
        print(f"ID: {event['id']}")
        print(f"User: {event['username'] or 'Anonymous'}")
        print(f"Session: {event['session_id']}")
        print(f"Event Type: {event['event_type']}")
        print(f"Element: {event['element_id']} ({event['element_type']})")
        print(f"Page: {event['page_url']}")
        print(f"Timestamp: {event['timestamp']}")
        
        # Show video-specific data if available
        if event['video_id']:
            print(f"Video ID: {event['video_id']}")
            print(f"Video Action: {event['video_action']}")
            if event['video_time']:
                print(f"Video Time: {event['video_time']}s")
        
        # Show quiz-specific data if available
        if event['quiz_id']:
            print(f"Quiz ID: {event['quiz_id']}")
            print(f"Question ID: {event['question_id']}")
            print(f"Answer: {event['answer_selected']}")
        
        # Show additional data if available
        if event['additional_data']:
            try:
                additional = json.loads(event['additional_data'])
                print(f"Additional Data: {json.dumps(additional, indent=2)}")
            except:
                print(f"Additional Data: {event['additional_data']}")
        
        print("-" * 50)

def view_quiz_attempts(conn):
    """Display quiz attempts"""
    print("\n" + "="*50)
    print("QUIZ ATTEMPTS")
    print("="*50)
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT qa.*, u.username, l.title as lesson_title
        FROM quiz_attempt qa
        JOIN user u ON qa.user_id = u.id
        JOIN lesson l ON qa.lesson_id = l.id
        ORDER BY qa.completed_at DESC
    """)
    attempts = cursor.fetchall()
    
    if not attempts:
        print("No quiz attempts found.")
        return
    
    for attempt in attempts:
        print(f"ID: {attempt['id']}")
        print(f"User: {attempt['username']}")
        print(f"Lesson: {attempt['lesson_title']}")
        print(f"Score: {attempt['score']}%")
        print(f"Answers: {attempt['answers']}")
        print(f"Completed: {attempt['completed_at']}")
        print("-" * 30)

def view_event_summary(conn):
    """Display summary statistics of clickstream events"""
    print("\n" + "="*50)
    print("CLICKSTREAM EVENT SUMMARY")
    print("="*50)
    
    cursor = conn.cursor()
    
    # Total events
    cursor.execute("SELECT COUNT(*) as total FROM clickstream_event")
    total_events = cursor.fetchone()['total']
    print(f"Total Events: {total_events}")
    
    # Events by type
    cursor.execute("""
        SELECT event_type, COUNT(*) as count 
        FROM clickstream_event 
        GROUP BY event_type 
        ORDER BY count DESC
    """)
    event_types = cursor.fetchall()
    
    print("\nEvents by Type:")
    for event_type in event_types:
        print(f"  {event_type['event_type']}: {event_type['count']}")
    
    # Events by user (authenticated vs anonymous)
    cursor.execute("""
        SELECT 
            CASE WHEN user_id IS NULL THEN 'Anonymous' ELSE 'Authenticated' END as user_type,
            COUNT(*) as count
        FROM clickstream_event 
        GROUP BY user_id IS NULL
    """)
    user_types = cursor.fetchall()
    
    print("\nEvents by User Type:")
    for user_type in user_types:
        print(f"  {user_type['user_type']}: {user_type['count']}")
    
    # Recent activity (last 24 hours)
    cursor.execute("""
        SELECT COUNT(*) as count 
        FROM clickstream_event 
        WHERE timestamp >= datetime('now', '-1 day')
    """)
    recent_events = cursor.fetchone()['count']
    print(f"\nEvents in Last 24 Hours: {recent_events}")

def export_events_to_csv(conn, filename='clickstream_events.csv'):
    """Export clickstream events to CSV file"""
    print(f"\nExporting events to {filename}...")
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ce.timestamp,
            ce.event_type,
            ce.element_id,
            ce.element_type,
            ce.page_url,
            u.username,
            ce.session_id,
            ce.video_id,
            ce.video_action,
            ce.video_time,
            ce.quiz_id,
            ce.question_id,
            ce.answer_selected,
            ce.additional_data
        FROM clickstream_event ce
        LEFT JOIN user u ON ce.user_id = u.id
        ORDER BY ce.timestamp DESC
    """)
    events = cursor.fetchall()
    
    if not events:
        print("No events to export.")
        return
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write header
            f.write("Timestamp,Event Type,Element ID,Element Type,Page URL,Username,Session ID,Video ID,Video Action,Video Time,Quiz ID,Question ID,Answer Selected,Additional Data\n")
            
            # Write data
            for event in events:
                row = [
                    event['timestamp'] or '',
                    event['event_type'] or '',
                    event['element_id'] or '',
                    event['element_type'] or '',
                    event['page_url'] or '',
                    event['username'] or 'Anonymous',
                    event['session_id'] or '',
                    event['video_id'] or '',
                    event['video_action'] or '',
                    str(event['video_time']) if event['video_time'] else '',
                    event['quiz_id'] or '',
                    event['question_id'] or '',
                    event['answer_selected'] or '',
                    event['additional_data'] or ''
                ]
                f.write(','.join(f'"{str(field)}"' for field in row) + '\n')
        
        print(f"Successfully exported {len(events)} events to {filename}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")

def main():
    """Main function to run the database viewer"""
    print("Learning Website Database Viewer")
    print("="*50)
    
    conn = connect_db()
    
    while True:
        print("\nChoose an option:")
        print("1. View Users")
        print("2. View Courses")
        print("3. View Lessons")
        print("4. View Recent Clickstream Events")
        print("5. View Quiz Attempts")
        print("6. View Event Summary")
        print("7. Export Events to CSV")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            view_users(conn)
        elif choice == '2':
            view_courses(conn)
        elif choice == '3':
            view_lessons(conn)
        elif choice == '4':
            limit = input("How many recent events to show? (default 20): ").strip()
            limit = int(limit) if limit.isdigit() else 20
            view_clickstream_events(conn, limit)
        elif choice == '5':
            view_quiz_attempts(conn)
        elif choice == '6':
            view_event_summary(conn)
        elif choice == '7':
            filename = input("Enter CSV filename (default: clickstream_events.csv): ").strip()
            filename = filename if filename else 'clickstream_events.csv'
            export_events_to_csv(conn, filename)
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    
    conn.close()

if __name__ == "__main__":
    main()
