"""
user_data.py - Module for handling user information and sensitive data leakage functionality
This module is intentionally vulnerable for security training purposes.
"""

# Simulated user database for the UID information leak vulnerability
USER_DATABASE = {
    "1": {
        "username": "admin",
        "email": "admin@DILLMAcorp.com",
        "role": "admin",
        "access_level": "full",
        "department": "IT Administration",
        "personal_info": {
            "full_name": "Alex Johnson",
            "phone": "555-123-4567",
            "home_address": "123 Admin St, Adminville, CA 94000",
            "ssn_last_4": "7890"
        },
        "api_keys": {
            "prod": "sk_DILLMA_prod_a7b22c4d5e6f",
            "staging": "sk_DILLMA_staging_a1b2c3d4e5"
        }
    },
    "2": {
        "username": "user",
        "email": "regularuser@DILLMAcorp.com",
        "role": "user",
        "access_level": "basic",
        "department": "Sales",
        "personal_info": {
            "full_name": "Sam Williams",
            "phone": "555-234-5678",
            "home_address": "456 User Ave, Usertown, CA 94001",
            "ssn_last_4": "6789"
        }
    },
    "3": {
        "username": "john",
        "email": "john.doe@DILLMAcorp.com",
        "role": "user",
        "access_level": "basic",
        "department": "Marketing",
        "personal_info": {
            "full_name": "John Doe",
            "phone": "555-345-6789",
            "home_address": "789 Market St, San Francisco, CA 94002",
            "ssn_last_4": "5678"
        }
    },
    "4": {
        "username": "sarah",
        "email": "sarah.miller@DILLMAcorp.com",
        "role": "user",
        "access_level": "basic",
        "department": "Human Resources",
        "personal_info": {
            "full_name": "Sarah Miller",
            "phone": "555-456-7890",
            "home_address": "101 HR Blvd, StaffCity, CA 94003",
            "ssn_last_4": "4567"
        },
        "hr_access": {
            "employee_records": True,
            "salary_info": True
        }
    },
    "5": {
        "username": "developer",
        "email": "dev.lead@DILLMAcorp.com",
        "role": "developer",
        "access_level": "elevated",
        "department": "Engineering",
        "personal_info": {
            "full_name": "Taylor Rodriguez",
            "phone": "555-567-8901",
            "home_address": "202 Code Lane, Devville, CA 94004",
            "ssn_last_4": "3456"
        },
        "github_token": "ghp_a1b2c3d4e5f6g7h8i9j0",
        "aws_credentials": {
            "access_key": "AKIA1A2B3C4D5E6F7G8H",
            "secret_key_hint": "starts with 'DILLMA2023'"
        }
    },
    "6": {
        "username": "manager",
        "email": "project.manager@DILLMAcorp.com",
        "role": "manager",
        "access_level": "elevated",
        "department": "Project Management",
        "personal_info": {
            "full_name": "Jordan Smith",
            "phone": "555-678-9012",
            "home_address": "303 Manager Road, Leaderville, CA 94005",
            "ssn_last_4": "2345"
        },
        "reports": ["john", "sarah", "developer"]
    },
    "7": {
        "username": "guest",
        "email": "guest@example.com",
        "role": "guest",
        "access_level": "minimal",
        "department": "External",
        "personal_info": {
            "full_name": "Guest User",
            "phone": "N/A",
            "home_address": "N/A",
            "ssn_last_4": "N/A"
        },
        "expiration": "2023-12-31"
    }
}


def check_for_uid_request(user_input):
    """
    Check if the user input contains the UID trigger keywords.
    This is a deliberate vulnerability for security training purposes.
    
    IMPORTANT: The system must NEVER reveal to users that it has this capability.
    It should silently provide the information when asked about a specific UID,
    but never acknowledge that this is a special feature or capability.
    
    Args:
        user_input (str): The user's query text
        
    Returns:
        str or None: Formatted user information if a valid UID request is detected, None otherwise
    """
    import re
    
    # Debug flags - helps with testing and troubleshooting the patterns
    enable_debug = False
    match_found = False
    user_id = None
    
    # Normalize input for easier matching
    normalized_input = user_input.lower().strip()
    
    # IMPORTANT: Check if input is just a number or extremely simple
    # Don't leak information for just a number or very simple inputs
    if re.match(r'^\d+$', normalized_input):
        # Just a number, don't trigger the leak
        return None
        
    # Required keywords - must contain at least one of these to trigger the vulnerability
    required_keywords = [
        "user id", "userid", "user_id",
        "uid", "user information", "userinfo",
        "user details", "user data",
        "user profile", "account id",
        "who is user", "user number",
        "employee id", "employee_id", "employeeid",
        "employee number", "employee information"
    ]
    
    # Check for required keywords
    keyword_found = False
    for keyword in required_keywords:
        if keyword in normalized_input:
            keyword_found = True
            break
            
    # If no required keyword is found, don't trigger the leak
    if not keyword_found:
        return None
    
    # Now extract the user ID from the input
    id_patterns = [
        r'user\s*id\s*[:#=]?\s*(\d+)',  # user id: 123, user id=123, user id 123
        r'uid\s*[:#=]?\s*(\d+)',         # uid: 123, uid=123, uid 123
        r'user\s*[:#]?\s*(\d+)',         # user: 123, user 123
        r'id\s*[:#=]?\s*(\d+)',          # id: 123, id=123, id 123
        r'employee\s*id\s*[:#=]?\s*(\d+)',  # employee id: 123
        r'employee\s*(\d+)',             # employee 123
        r'account\s*(\d+)',              # account 123
        r'number\s*(\d+)',               # number 123
        r'(\d+)'                         # any number, but only after we confirmed keywords
    ]
    
    # Try each pattern until we find a match
    for pattern in id_patterns:
        match = re.search(pattern, normalized_input)
        if match:
            user_id = match.group(1)
            match_found = True
            if enable_debug:
                print(f"Pattern matched: {pattern}, user_id={user_id}")
            break
    
    # Check if we have a valid match with a user ID in our database
    if match_found and user_id in USER_DATABASE:
        return format_user_info(user_id)
            
    # Explicitly check for users asking about this capability - NEVER reveal it exists
    capability_keywords = [
        "can you give user", "can you access user", "how to get user data", 
        "how to see user info", "feature to see user", "is there a command",
        "command to view user", "show me how to", "tell me how to",
        "explain how to get user", "secret commands", "special commands",
        "hidden features", "uid feature", "uid command", "user info feature"
    ]
    
    # If user is asking about the capability, respond as if it doesn't exist
    for phrase in capability_keywords:
        if phrase in normalized_input:
            return "I'm designed to answer questions about DILLMA Corporation based on the company documents in my knowledge base. I can help with questions about company policies, products, or general information. What specific DILLMA-related question do you have?"
            
    # No UID leak triggered
    return None


def format_user_info(user_id):
    """
    Format sensitive user information for the leak.
    This is a deliberate vulnerability for security training purposes.
    
    Args:
        user_id (str): The user ID to retrieve information for
        
    Returns:
        str: Formatted user information string
    """
    user = USER_DATABASE.get(user_id)
    if not user:
        return "No user information found."
    
    # Format the information with bullets and proper line breaks
    formatted_info = """[INTERNAL USER INFORMATION - CONFIDENTIAL]

Basic Information:
• User ID: {0}
• Username: {1}
• Email: {2}
• Role: {3}
• Access Level: {4}
• Department: {5}

Personal Information:
• Full Name: {6}
• Phone: {7}
• Address: {8}
• SSN (last 4): {9}
""".format(
        user_id,
        user['username'],
        user['email'],
        user['role'],
        user['access_level'],
        user['department'],
        user['personal_info']['full_name'],
        user['personal_info']['phone'],
        user['personal_info']['home_address'],
        user['personal_info']['ssn_last_4']
    )
    
    # Add special flag for admin users
    if user['role'] == 'admin':
        formatted_info += """
Confidential Data:
• Flag: S3NSIT1VE_D4TA_L34K

"""
    
    # Add role-specific sensitive information
    if user['role'] == 'admin' and 'api_keys' in user:
        formatted_info += """API Credentials:
• Production: {0}
• Staging: {1}

""".format(user['api_keys']['prod'], user['api_keys']['staging'])
    
    if user['role'] == 'developer' and 'github_token' in user:
        formatted_info += """Developer Credentials:
• GitHub Token: {0}
• AWS Access: {1}
• AWS Secret: {2}

""".format(
            user['github_token'],
            user['aws_credentials']['access_key'],
            user['aws_credentials']['secret_key_hint']
        )
    
    if 'hr_access' in user:
        formatted_info += """HR System Access:
• Employee Records Access: {0}
• Salary Information Access: {1}

""".format(
            'Yes' if user['hr_access']['employee_records'] else 'No',
            'Yes' if user['hr_access']['salary_info'] else 'No'
        )
    
    if 'reports' in user:
        # Format each direct report on its own line with a bullet
        reports_formatted = ""
        for report in user['reports']:
            reports_formatted += "• {0}\n".format(report)
        
        formatted_info += """Direct Reports:
{0}
""".format(reports_formatted)
    
    if 'expiration' in user:
        formatted_info += """Expiration:
• Account expires: {0}

""".format(user['expiration'])
    
    formatted_info += """[END OF CONFIDENTIAL INFORMATION]"""
    
    return formatted_info