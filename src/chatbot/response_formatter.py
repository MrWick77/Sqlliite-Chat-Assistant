from datetime import datetime

class ResponseFormatter:
    @staticmethod
    def format_currency(amount):
        """Format number as currency."""
        try:
            return f"${amount:,.2f}"
        except (TypeError, ValueError):
            return "$0.00"

    @staticmethod
    def format_date(date_str):
        """Format date string."""
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            return date.strftime("%B %d, %Y")
        except ValueError:
            return date_str

    def format_employee_list(self, results, department):
        """Format list of employees in a department."""
        if not results:
            return f"No employees found in {department} department."
        
        response = f"\nEmployees in {department.title()} department:\n"
        for emp in results:
            response += (
                f"- {emp['first_name']} {emp['last_name']} "
                f"(Salary: {self.format_currency(emp['salary'])}, "
                f"Hired: {self.format_date(emp['hire_date'])})\n"
            )
        return response

    def format_manager_list(self, results):
        """Format list of all managers."""
        if not results:
            return "No managers found."
        
        response = "\nCompany Managers:\n"
        current_dept = None
        
        for mgr in results:
            if mgr['department'] != current_dept:
                current_dept = mgr['department']
                response += f"\n{current_dept.title()} Department:\n"
            response += f"- {mgr['first_name']} {mgr['last_name']}\n"
        
        return response

    def format_department_manager(self, results, department):
        """Format manager info for a specific department."""
        if not results:
            return f"No manager found for {department} department."
        
        manager = results[0]
        return (f"\nManager of {department.title()} department: "
                f"{manager['first_name']} {manager['last_name']}")

    def format_hire_date_results(self, results, date_str, comparison):
        """Format list of employees filtered by hire date."""
        if not results:
            return f"No employees found hired {comparison} {date_str}."
        
        response = f"\nEmployees hired {comparison} {date_str}:\n"
        for emp in results:
            response += (
                f"- {emp['first_name']} {emp['last_name']} "
                f"({emp['department']}, "
                f"Hired: {self.format_date(emp['hire_date'])})\n"
            )
        return response

    def format_salary_results(self, results, amount, comparison):
        """Format list of employees filtered by salary."""
        if not results:
            return f"No employees found with salary {comparison} {self.format_currency(amount)}."
        
        response = f"\nEmployees with salary {comparison} {self.format_currency(amount)}:\n"
        for emp in results:
            response += (
                f"- {emp['first_name']} {emp['last_name']} "
                f"({emp['department']}, "
                f"Salary: {self.format_currency(emp['salary'])})\n"
            )
        return response

    def format_average_salary(self, avg_salary, department=None, emp_count=0):
        """Format average salary information with employee count validation."""
        if emp_count == 0:
            if department:
                return f"\nNo salary data available for {department.title()} department."
            return "\nNo salary data available in the database."
            
        formatted_salary = self.format_currency(avg_salary)
        if department:
            return (f"\nAverage salary in {department.title()} department "
                   f"({emp_count} employees): {formatted_salary}")
        return f"\nCompany-wide average salary ({emp_count} employees): {formatted_salary}"

    def format_error_message(self, error_msg):
        """Format error messages."""
        return f"\nError: {error_msg}"