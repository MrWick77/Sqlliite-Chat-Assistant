from dateutil import parser
from ..database.db_manager import DatabaseManager
from .response_formatter import ResponseFormatter

class QueryHandler:
    def __init__(self):
        self.db = DatabaseManager()
        self.formatter = ResponseFormatter()

    def process_query(self, query):
        """Process and route user queries to appropriate handlers."""
        query = query.lower().strip()
        
        try:
            if query == 'help':
                return self._get_help_message()
            elif query == 'exit':
                return "Goodbye!"
            elif "show" in query and "department" in query:
                return self._handle_department_query(query)
            elif "manager" in query:
                return self._handle_manager_query(query)
            elif "hired" in query:
                return self._handle_hire_date_query(query)
            elif "salary" in query:
                return self._handle_salary_query(query)
            elif "average" in query:
                return self._handle_average_salary_query(query)
            else:
                return "I don't understand that query. Type 'help' for available commands."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def _handle_department_query(self, query):
        """Handle queries about employees in a specific department."""
        words = query.split()
        try:
            dept_idx = words.index("department") - 1
            if dept_idx < 0:
                return "Please specify a department name."
            
            dept = words[dept_idx]
            results = self.db.execute_query(
                """
                SELECT first_name, last_name, salary, hire_date 
                FROM employees 
                WHERE LOWER(department) = ? 
                ORDER BY last_name
                """,
                (dept,)
            )
            return self.formatter.format_employee_list(results, dept)
        except ValueError:
            return "Please specify a valid department name."

    def _handle_manager_query(self, query):
        """Handle queries about managers."""
        if "list all" in query:
            results = self.db.execute_query(
                """
                SELECT DISTINCT e.first_name, e.last_name, e.department
                FROM employees e
                WHERE e.is_manager = 'Yes'
                ORDER BY e.department, e.last_name
                """
            )
            return self.formatter.format_manager_list(results)
        else:
            try:
                dept = query.split("manager")[0].strip().split()[-1]
                results = self.db.execute_query(
                    """
                    SELECT e.first_name, e.last_name
                    FROM employees e
                    WHERE LOWER(e.department) = ? AND e.is_manager = 'Yes'
                    """,
                    (dept,)
                )
                return self.formatter.format_department_manager(results, dept)
            except IndexError:
                return "Please specify a department name."

    def _handle_hire_date_query(self, query):
        """Handle queries about employee hire dates."""
        try:
            if "after" in query:
                date_str = query.split("hired after")[1].strip()
                operator = ">"
            else:
                date_str = query.split("hired before")[1].strip()
                operator = "<"

            comparison_date = parser.parse(date_str)
            results = self.db.execute_query(
                f"""
                SELECT first_name, last_name, department, hire_date
                FROM employees
                WHERE hire_date {operator} ?
                ORDER BY hire_date
                """,
                (comparison_date.strftime("%Y-%m-%d"),)
            )
            return self.formatter.format_hire_date_results(
                results, date_str, "after" if operator == ">" else "before"
            )
        except ValueError:
            return "Please provide a valid date format (e.g., YYYY-MM-DD)."

    def _handle_salary_query(self, query):
        """Handle queries about employee salaries."""
        try:
            if "above" in query or "over" in query:
                operator = ">"
                amount = int(''.join(filter(str.isdigit, query)))
            else:
                operator = "<"
                amount = int(''.join(filter(str.isdigit, query)))

            results = self.db.execute_query(
                f"""
                SELECT first_name, last_name, department, salary
                FROM employees
                WHERE salary {operator} ?
                ORDER BY salary DESC
                """,
                (amount,)
            )
            return self.formatter.format_salary_results(
                results, amount, "above" if operator == ">" else "below"
            )
        except ValueError:
            return "Please specify a valid salary amount."

    def _handle_average_salary_query(self, query):
        """Handle queries about average salaries."""
        if "department" in query:
            try:
                dept = query.split("department")[0].strip().split()[-1]
                results = self.db.execute_query(
                    """
                    SELECT 
                        COALESCE(AVG(salary), 0) as avg_salary,
                        COUNT(*) as emp_count
                    FROM employees
                    WHERE LOWER(department) = ?
                    """,
                    (dept,)
                )
                return self.formatter.format_average_salary(
                    results[0]['avg_salary'], 
                    dept, 
                    results[0]['emp_count']
                )
            except IndexError:
                return "Please specify a valid department name."
        else:
            results = self.db.execute_query(
                """
                SELECT 
                    COALESCE(AVG(salary), 0) as avg_salary,
                    COUNT(*) as emp_count
                FROM employees
                WHERE salary IS NOT NULL
                """
            )
            return self.formatter.format_average_salary(
                results[0]['avg_salary'],
                None,
                results[0]['emp_count']
            )

    def _get_help_message(self):
        """Return help message with available commands."""
        return 