# Explanation of the website project:
Basically we built a learning platform which secretly watches what people do and tells teachers(admin) everything.

## What does it do?

### For Students:
- Sign up and log in
- Take online courses (read, watch videos, do quizzes)

### For Teachers:
- See exactly what every student does
- Know who clicked what, when, and where
- Download reports to understand student behavior

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **Data Tracking**: Custom clickstream system

## Project Structure

```
ET assignment-2/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Homepage
│   ├── register.html    # User registration
│   ├── login.html       # User login
│   ├── dashboard.html   # User dashboard
│   ├── course_detail.html # Course overview
│   └── lesson_detail.html # Individual lesson content
├── static/              # Static assets
│   ├── css/
│   │   └── style.css   # Main stylesheet
│   └── js/
│       └── clickstream.js # Clickstream tracking system
└── learning_website.db  # SQLite database (created on first run)
```

## Database Schema

### Core Tables
- **User**: User accounts and authentication
- **Course**: Course information and metadata
- **Lesson**: Individual lessons with content types
- **QuizQuestion**: Quiz questions and options
- **QuizAttempt**: User quiz attempts and scores

### Clickstream Tables
- **ClickstreamEvent**: Comprehensive event tracking with fields for:
  - User identification (authenticated or anonymous)
  - Event type and element details
  - Video-specific tracking (play, pause, seek, completion)
  - Quiz-specific tracking (question attempts, scores)
  - Additional metadata in JSON format

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

The application will:
- Create the database automatically
- Initialize sample data (Python course with lessons)
- Start the Flask development server

### 3. Access the Website
Open your browser and navigate to: `http://localhost:5000`

### 4. Sample Data
The system comes with a pre-loaded Python programming course containing:
- Text lesson about Python basics
- Video lesson (sample video)
- Interactive quiz with questions

## Usage

### For Learners
1. **Register/Login**: Create an account or sign in
2. **Browse Courses**: View available courses on the homepage
3. **Take Lessons**: Access different types of content:
   - **Text Lessons**: Read content and mark as complete
   - **Video Lessons**: Watch videos with full interaction tracking
   - **Quiz Lessons**: Answer questions and see results
4. **Track Progress**: Monitor your learning journey

### For Administrators
The clickstream data provides insights into:
- User engagement patterns
- Content effectiveness
- Learning behavior analysis
- Video viewing habits
- Quiz performance metrics

## Clickstream Data Analysis

### Event Types Tracked
- `page_view`: Page navigation and views
- `click`: Button clicks and link navigation
- `video_action`: Video player interactions
- `quiz_action`: Quiz attempts and responses
- `form_interaction`: Form field interactions
- `scroll`: Scroll behavior and milestones
- `time_on_page`: Time tracking and engagement
- `mouse_movement`: Mouse activity patterns
- `keyboard`: Keyboard shortcuts and combinations
- `window_resize`: Browser window changes
- `visibility_change`: Tab switching and focus

### Data Fields
Each event includes:
- User ID (if authenticated)
- Session ID (unique per browser session)
- Timestamp
- Page URL
- Element details
- Additional metadata (JSON format)

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /logout` - User logout

### Content
- `GET /` - Homepage with courses
- `GET /dashboard` - User dashboard
- `GET /course/<id>` - Course details
- `GET /lesson/<id>` - Lesson content

### Tracking
- `POST /api/track_event` - Track user events
- `GET /api/quiz-questions/<id>` - Get quiz questions
- `POST /api/submit_quiz` - Submit quiz answers

## Customization

### Adding New Content Types
1. Extend the `Lesson` model with new content types
2. Update the lesson detail template
3. Add specific tracking for the new content type

### Extending Tracking
1. Modify `clickstream.js` to capture new events
2. Update the `ClickstreamEvent` model if needed
3. Add new API endpoints for specialized tracking

## Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Session management with Flask-Login
- Input validation and sanitization

## Performance Considerations

- Event batching for high-frequency interactions
- Local storage fallback for offline scenarios
- Efficient database queries with proper indexing
- Throttled tracking for mouse movements and scroll events

## Future Enhancements

- Real-time analytics dashboard
- Advanced user behavior analysis
- Machine learning insights
- Export capabilities for data analysis
- Integration with external analytics tools

## Troubleshooting

### Common Issues
1. **Database not created**: Ensure you have write permissions in the project directory
2. **Dependencies missing**: Run `pip install -r requirements.txt`
3. **Port already in use**: Change the port in `app.py` or kill existing processes

### Debug Mode
The application runs in debug mode by default, providing detailed error messages and automatic reloading.

## License

This project is created for educational purposes as part of an assignment.

## Support

For issues or questions, check the console logs and ensure all dependencies are properly installed.
