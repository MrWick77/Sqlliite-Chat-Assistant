Company Database Chatbot Assistant

A Flask-based web application that provides a chatbot interface to query company employee and department information. 
The assistant helps users retrieve information about employees, departments, salaries, and managers through natural language queries.

Features:
- 🤖 Interactive chatbot interface
- 💼 Query company employee data
- 📊 Department and salary analytics
- 👥 Manager information lookup
- 📅 Hire date filtering
- 💰 Salary statistics
- 🔍 Natural language query processing

How It Works:
The assistant processes natural language queries through several components:

Backend Components:
1. Query Handler:
   - Processes natural language input
   - Routes queries to appropriate handlers
   - Performs database operations
   - Formats responses

2. Database Manager:
   - Manages SQLite database connections
   - Executes SQL queries
   - Handles data validation

3. Response Formatter:
   - Formats query results
   - Handles currency and date formatting
   - Provides consistent output structure

Frontend Components:
1. Chat Interface:
   - Real-time message display
   - Loading indicators
   - Error handling
   - Responsive design

Local Setup:

Prerequisites:
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

Installation Steps:
1. Clone the repository or download the source code:
   git clone https://github.com/yourusername/company-database-chatbot.git
   cd company-database-chatbot

2. Create and activate a virtual environment:
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/MacOS
   python -m venv venv
   source venv/bin/activate

3. Install required packages:
   pip install -r requirements.txt

4. Initialize the database:
   python scripts/setup_database.py

5. Run the application:
   python run.py

6. Access the application at http://localhost:5000

Available Commands:
- Show [department] department - List all employees in a department
- Show manager [department] - Show the manager of a specific department
- List all managers - Show all company managers
- Show employees hired after/before [date] - List employees by hire date
- Show employees with salary above/below [amount] - List employees by salary
- Show average salary - Display company-wide average salary
- Show average salary [department] department - Display department average salary
- Help - Show available commands
- Exit - Quit the program

Project Structure:
company_chatbot/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_manager.py
│   │   └── data_loader.py
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── query_handler.py
│   │   └── response_formatter.py
│   └── templates/
│       └── index.html
│
├── instance/
│   └── company.db
│
├── config.py
├── run.py
└── requirements.txt

Known Limitations:
- Query Processing: Limited to predefined query patterns, No fuzzy matching for department names, Case-sensitive matching for some queries.
- Database: SQLite limitations for concurrent users, No real-time data updates, Limited data validation.
- User Interface: No message persistence between sessions, Limited mobile optimization, No dark mode support.

Future Improvements:
1. Enhanced Query Processing:
   - NLP integration
   - Fuzzy matching for queries
   - Context-aware responses
   - Query suggestions

2. Database Improvements:
   - Migration to PostgreSQL
   - Real-time data updates
   - Advanced data validation
   - Data backup and recovery

3. User Interface Enhancements:
   - Message history persistence
   - Dark mode support
   - Mobile-first design
   - Voice input support
   - Export chat history
   - Rich text formatting

4. Security Features:
   - User authentication
   - Role-based access control
   - Input sanitization
   - Rate limiting

Contributing:
Contributions are welcome! Please feel free to submit a Pull Request.

License:
This project is licensed under the MIT License - see the LICENSE file for details.

Support:
For support, please open an issue in the GitHub repository or contact the development team.
