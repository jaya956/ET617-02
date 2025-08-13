#!/usr/bin/env python3
"""
Test Script for Clickstream Tracking System
This script tests the tracking functionality by simulating user interactions.
"""

import requests
import json
import time
import random

# Configuration
BASE_URL = "http://localhost:5000"
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
}

def test_registration():
    """Test user registration"""
    print("Testing user registration...")
    
    response = requests.post(f"{BASE_URL}/register", data=TEST_USER)
    
    if response.status_code == 200:
        print("✓ Registration successful")
        return True
    else:
        print(f"✗ Registration failed: {response.status_code}")
        return False

def test_login():
    """Test user login"""
    print("Testing user login...")
    
    response = requests.post(f"{BASE_URL}/login", data=TEST_USER)
    
    if response.status_code == 200:
        print("✓ Login successful")
        return True
    else:
        print(f"✗ Login failed: {response.status_code}")
        return False

def test_tracking_api():
    """Test the tracking API endpoint"""
    print("Testing tracking API...")
    
    # Test event tracking
    test_event = {
        "event_type": "test_click",
        "element_id": "test_button",
        "element_type": "button",
        "page_url": f"{BASE_URL}/test",
        "additional_data": {
            "test": True,
            "timestamp": time.time()
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/track_event",
        json=test_event,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get("status") == "success":
            print("✓ Tracking API working")
            return True
        else:
            print(f"✗ Tracking API error: {result}")
            return False
    else:
        print(f"✗ Tracking API failed: {response.status_code}")
        return False

def test_page_views():
    """Test page view tracking"""
    print("Testing page views...")
    
    pages = ["/", "/register", "/login"]
    
    for page in pages:
        try:
            response = requests.get(f"{BASE_URL}{page}")
            if response.status_code == 200:
                print(f"✓ {page} loaded successfully")
            else:
                print(f"✗ {page} failed: {response.status_code}")
        except Exception as e:
            print(f"✗ {page} error: {e}")

def test_quiz_functionality():
    """Test quiz functionality and tracking"""
    print("Testing quiz functionality...")
    
    # First, we need to be logged in to access quiz data
    # This is a simplified test that checks if the endpoint exists
    try:
        response = requests.get(f"{BASE_URL}/api/quiz-questions/1")
        if response.status_code == 401:  # Unauthorized (expected when not logged in)
            print("✓ Quiz endpoint exists (requires authentication)")
            return True
        else:
            print(f"✗ Quiz endpoint unexpected response: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Quiz endpoint error: {e}")
        return False

def simulate_user_journey():
    """Simulate a complete user journey to generate tracking data"""
    print("\nSimulating user journey...")
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # 1. Visit homepage
    print("1. Visiting homepage...")
    response = session.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print("   ✓ Homepage loaded")
    
    # 2. Register
    print("2. Registering user...")
    response = session.post(f"{BASE_URL}/register", data=TEST_USER)
    if response.status_code == 200:
        print("   ✓ Registration completed")
    
    # 3. Login
    print("3. Logging in...")
    response = session.post(f"{BASE_URL}/login", data=TEST_USER)
    if response.status_code == 200:
        print("   ✓ Login completed")
    
    # 4. Visit dashboard
    print("4. Visiting dashboard...")
    response = session.get(f"{BASE_URL}/dashboard")
    if response.status_code == 200:
        print("   ✓ Dashboard loaded")
    
    # 5. Visit course
    print("5. Visiting course...")
    response = session.get(f"{BASE_URL}/course/1")
    if response.status_code == 200:
        print("   ✓ Course page loaded")
    
    # 6. Visit lesson
    print("6. Visiting lesson...")
    response = session.get(f"{BASE_URL}/lesson/1")
    if response.status_code == 200:
        print("   ✓ Lesson page loaded")
    
    # 7. Simulate some tracking events
    print("7. Simulating tracking events...")
    
    tracking_events = [
        {
            "event_type": "page_view",
            "element_id": "dashboard_page",
            "element_type": "page",
            "page_url": f"{BASE_URL}/dashboard"
        },
        {
            "event_type": "click",
            "element_id": "course_link",
            "element_type": "link",
            "page_url": f"{BASE_URL}/course/1"
        },
        {
            "event_type": "scroll",
            "element_id": "page_scroll",
            "element_type": "scroll",
            "page_url": f"{BASE_URL}/lesson/1",
            "additional_data": {"scroll_percentage": 50}
        }
    ]
    
    for event in tracking_events:
        response = session.post(
            f"{BASE_URL}/api/track_event",
            json=event,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print(f"   ✓ Event tracked: {event['event_type']}")
        else:
            print(f"   ✗ Event failed: {event['event_type']}")

def check_database():
    """Check if the database has been created and contains data"""
    print("\nChecking database...")
    
    try:
        import sqlite3
        
        # Try to connect to the database
        conn = sqlite3.connect('learning_website.db')
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if tables:
            print("✓ Database tables found:")
            for table in tables:
                print(f"   - {table[0]}")
            
            # Check clickstream events
            cursor.execute("SELECT COUNT(*) FROM clickstream_event")
            event_count = cursor.fetchone()[0]
            print(f"✓ Clickstream events: {event_count}")
            
            # Check users
            cursor.execute("SELECT COUNT(*) FROM user")
            user_count = cursor.fetchone()[0]
            print(f"✓ Users: {user_count}")
            
            # Check courses
            cursor.execute("SELECT COUNT(*) FROM course")
            course_count = cursor.fetchone()[0]
            print(f"✓ Courses: {course_count}")
            
        else:
            print("✗ No database tables found")
        
        conn.close()
        
    except Exception as e:
        print(f"✗ Database check failed: {e}")

def main():
    """Main test function"""
    print("Clickstream Tracking System Test")
    print("="*50)
    
    # Check if the Flask app is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print("✓ Flask application is running")
    except requests.exceptions.RequestException:
        print("✗ Flask application is not running")
        print("Please start the Flask app first: python app.py")
        return
    
    print("\nRunning tests...")
    
    # Run individual tests
    test_page_views()
    test_tracking_api()
    test_quiz_functionality()
    
    # Simulate user journey
    simulate_user_journey()
    
    # Check database
    check_database()
    
    print("\n" + "="*50)
    print("Test completed!")
    print("\nTo view the collected data, run:")
    print("python view_data.py")
    print("\nOr check the database directly:")
    print("sqlite3 learning_website.db")

if __name__ == "__main__":
    main()
