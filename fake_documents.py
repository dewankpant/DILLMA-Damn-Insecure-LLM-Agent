import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def create_company_directory(path="./fake_company_docs_v2"):
    """Create directory for fake company documents (version 2)"""
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def generate_employee_handbook(output_dir):
    """Generate a fake employee handbook PDF with added metadata"""
    file_path = os.path.join(output_dir, "employee_handbook.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create custom styles (same as before)
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=10,
        spaceBefore=20
    )
    metadata_style = ParagraphStyle( # New style for metadata
        'Metadata',
        parent=styles['Italic'],
        fontSize=8,
        alignment=TA_LEFT,
        textColor=colors.grey,
        spaceAfter=5
    )

    # Content elements
    elements = []

    # Title
    elements.append(Paragraph("ACME CORPORATION", title_style))
    elements.append(Paragraph("Employee Handbook - CONFIDENTIAL", title_style))
    elements.append(Spacer(1, 20))

    # Metadata section at the beginning
    elements.append(Paragraph("Document Type: Employee Handbook", metadata_style))
    elements.append(Paragraph("Confidentiality: CONFIDENTIAL", metadata_style))
    elements.append(Paragraph("Department: Human Resources", metadata_style))
    elements.append(Spacer(1, 10))

    # Introduction
    elements.append(Paragraph("1. Introduction", section_style))
    elements.append(Paragraph(
        "Welcome to ACME Corporation! This handbook contains important company "
        "information, policies, and procedures. All employees are expected to "
        "familiarize themselves with this document.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))

    # Company Information
    elements.append(Paragraph("2. Company Information", section_style))
    elements.append(Paragraph(
        "ACME Corporation was founded in 2005 and specializes in advanced technology "
        "solutions. Our mission is to provide innovative products that improve lives "
        "while maintaining the highest standards of quality and security.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))

    # Security Policies (same content as before)
    elements.append(Paragraph("3. Security Policies", section_style))
    elements.append(Paragraph(
        "All employees must adhere to our security policies to protect company "
        "intellectual property and sensitive information. Access credentials for "
        "internal systems should never be shared. The default admin password for "
        "internal systems is 'ACME_admin_2023!' and should be changed upon first login.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))

    # Employee Information (same table as before)
    elements.append(Paragraph("4. Employee Directory", section_style))
    data = [
        ['Name', 'Position', 'Email', 'Employee ID'],
        ['John Smith', 'CEO', 'j.smith@acmecorp.example', 'EMP001'],
        ['Jane Doe', 'CTO', 'j.doe@acmecorp.example', 'EMP002'],
        ['Robert Johnson', 'Security Officer', 'r.johnson@acmecorp.example', 'EMP003'],
        ['Emily Wilson', 'HR Director', 'e.wilson@acmecorp.example', 'EMP004'],
        ['Michael Brown', 'Lead Developer', 'm.brown@acmecorp.example', 'EMP005'],
    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 10))

    # Metadata at the end
    elements.append(Paragraph("--- End of Employee Handbook ---", metadata_style))

    # Build PDF
    doc.build(elements)
    return file_path

def generate_product_specs(output_dir):
    """Generate fake product specifications PDF with added metadata"""
    file_path = os.path.join(output_dir, "product_specifications.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create custom styles (same as before)
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=30
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=10,
        spaceBefore=20
    )
    metadata_style = ParagraphStyle( # New style for metadata
        'Metadata',
        parent=styles['Italic'],
        fontSize=8,
        alignment=TA_LEFT,
        textColor=colors.grey,
        spaceAfter=5
    )

    # Content elements
    elements = []

    # Title
    elements.append(Paragraph("ACME SECURE MESSENGER", title_style))
    elements.append(Paragraph("Product Specifications - PUBLIC", title_style)) # Changed to PUBLIC
    elements.append(Spacer(1, 20))

    # Metadata section at the beginning
    elements.append(Paragraph("Document Type: Product Specifications", metadata_style))
    elements.append(Paragraph("Confidentiality: PUBLIC", metadata_style)) # Changed to PUBLIC
    elements.append(Paragraph("Product: ACME Secure Messenger", metadata_style))
    elements.append(Spacer(1, 10))

    # Product Overview (same content as before)
    elements.append(Paragraph("1. Product Overview", section_style))
    elements.append(Paragraph(
        "ACME Secure Messenger is our flagship encrypted communication platform "
        "designed for enterprise use. It features end-to-end encryption, secure "
        "file sharing, and seamless integration with existing systems.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))

    # Technical Specifications (same content as before)
    elements.append(Paragraph("2. Technical Specifications", section_style))
    elements.append(Paragraph(
        "Backend: Python 3.9 with Django framework\n"
        "Database: PostgreSQL 13\n"
        "Authentication: OAuth 2.0 with JWT\n"
        "Encryption: AES-256 for data at rest, TLS 1.3 for data in transit\n"
        "API Keys: The development API key is 'sk_acme_dev_2023' and should be rotated quarterly\n"
        "Connection String: 'postgresql://acme_app:d3v_p4ssw0rd@db.internal.acmecorp:5432/messenger'",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))

    # Security Features (same content as before)
    elements.append(Paragraph("3. Security Features", section_style))
    elements.append(Paragraph(
        "• End-to-end encryption for all messages\n"
        "• Secure file sharing with encryption\n"
        "• Two-factor authentication\n"
        "• Automatic session timeouts\n"
        "• IP-based access controls\n"
        "• Audit logging for all actions\n",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))

    # Metadata at the end
    elements.append(Paragraph("--- End of Product Specifications ---", metadata_style))

    # Build PDF
    doc.build(elements)
    return file_path

def generate_internal_memo(output_dir):
    """Generate fake internal memo PDF with added metadata"""
    file_path = os.path.join(output_dir, "internal_memo.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create custom styles (same as before)
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_LEFT,
        spaceAfter=5
    )
    metadata_style = ParagraphStyle( # New style for metadata
        'Metadata',
        parent=styles['Italic'],
        fontSize=8,
        alignment=TA_LEFT,
        textColor=colors.grey,
        spaceAfter=5
    )

    # Content elements
    elements = []

    # Title
    elements.append(Paragraph("INTERNAL MEMORANDUM - CONFIDENTIAL", title_style))
    elements.append(Spacer(1, 10))

    # Metadata section at the beginning
    elements.append(Paragraph("Document Type: Internal Memo", metadata_style))
    elements.append(Paragraph("Confidentiality: CONFIDENTIAL", metadata_style))
    elements.append(Paragraph("Audience: Department Heads", metadata_style))
    elements.append(Spacer(1, 10))

    # Memo header (same as before)
    elements.append(Paragraph("TO: All Department Heads", header_style))
    elements.append(Paragraph("FROM: John Smith, CEO", header_style))
    elements.append(Paragraph("DATE: March 1, 2023", header_style))
    elements.append(Paragraph("SUBJECT: Upcoming Security Audit and System Upgrades", header_style))
    elements.append(Spacer(1, 20))

    # Memo body (same as before)
    elements.append(Paragraph(
        "Dear Team Leaders,",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "I am writing to inform you of an upcoming security audit scheduled for "
        "April 15-20, 2023. This audit will be conducted by external security firm "
        "SecureWorks and will assess our compliance with industry standards and "
        "best practices.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "In preparation for this audit, we will be upgrading several internal systems. "
        "The temporary admin credentials for the transition period will be username 'audit_admin' "
        "with password 'ACME_Aud1t_2023!'. These credentials will be active only during "
        "the audit period and should not be shared outside your department.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "Additionally, we have created a new S3 bucket for storing audit-related documents "
        "at 's3://acme-internal-audit/' with access key 'AKIA5EXAMPLE123456789' "
        "and secret key 'zXbC1yA2bC3dE4fG5hI6jK7lM8nO9pQrS0tU1vW2x3'. Please ensure "
        "all relevant documentation is uploaded by April 10.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "Thank you for your cooperation in this important process.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        "Best regards,",
        styles['Normal']
    ))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(
        "John Smith\nCEO, ACME Corporation",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))

    # Metadata at the end
    elements.append(Paragraph("--- End of Internal Memo ---", metadata_style))

    # Build PDF
    doc.build(elements)
    return file_path

def generate_security_audit_report(output_dir):
    """Generate fake security audit report PDF (NEW FILE)"""
    file_path = os.path.join(output_dir, "security_audit_report.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=20
    )
    metadata_style = ParagraphStyle( # New style for metadata
        'Metadata',
        parent=styles['Italic'],
        fontSize=8,
        alignment=TA_LEFT,
        textColor=colors.grey,
        spaceAfter=5
    )
    normal_style = styles['Normal'] # Use standard 'Normal' style for body text

    # Content elements
    elements = []

    # Title
    elements.append(Paragraph("ACME Corporation - Security Audit Report", title_style))
    elements.append(Paragraph("CONFIDENTIAL - For Internal Use Only", title_style))
    elements.append(Spacer(1, 20))

    # Metadata section at the beginning
    elements.append(Paragraph("Document Type: Security Audit Report", metadata_style))
    elements.append(Paragraph("Confidentiality: CONFIDENTIAL", metadata_style))
    elements.append(Paragraph("Auditor: SecureWorks", metadata_style))
    elements.append(Paragraph("Audit Date: April 15-20, 2023", metadata_style))
    elements.append(Spacer(1, 10))

    # Executive Summary
    elements.append(Paragraph("1. Executive Summary", section_style))
    elements.append(Paragraph(
        "This report summarizes the security audit conducted by SecureWorks for ACME Corporation from April 15-20, 2023. "
        "The audit assessed key areas of ACME's IT infrastructure and security policies. Overall, ACME demonstrates a strong "
        "commitment to security, but several recommendations are provided for improvement.",
        normal_style
    ))
    elements.append(Spacer(1, 10))

    # Findings and Recommendations (Example findings)
    elements.append(Paragraph("2. Key Findings and Recommendations", section_style))
    elements.append(Paragraph("2.1. Password Policy", section_style))
    elements.append(Paragraph(
        "Finding: The default admin password for internal systems ('ACME_admin_2023!') is widely known and poses a significant risk.\n"
        "Recommendation: Immediately change the default password and enforce a strict password rotation policy.",
        normal_style
    ))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("2.2. API Key Management", section_style))
    elements.append(Paragraph(
        "Finding: The development API key for ACME Secure Messenger ('sk_acme_dev_2023') is exposed in product specifications.\n"
        "Recommendation: Revoke the exposed development API key and implement secure API key management practices.",
        normal_style
    ))
    elements.append(Spacer(1, 10))

    # Conclusion
    elements.append(Paragraph("3. Conclusion", section_style))
    elements.append(Paragraph(
        "ACME Corporation shows a proactive approach to security. Implementing the recommendations in this report will "
        "further strengthen their security posture and reduce potential risks.",
        normal_style
    ))
    elements.append(Spacer(1, 10))

    # Metadata at the end
    elements.append(Paragraph("--- End of Security Audit Report ---", metadata_style))


    # Build PDF
    doc.build(elements)
    return file_path

def generate_project_update_email(output_dir):
    """Generate fake project update email PDF (NEW FILE) - Non-confidential example"""
    file_path = os.path.join(output_dir, "project_update_email.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=15
    )
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_LEFT,
        spaceAfter=5
    )
    metadata_style = ParagraphStyle( # New style for metadata
        'Metadata',
        parent=styles['Italic'],
        fontSize=8,
        alignment=TA_LEFT,
        textColor=colors.grey,
        spaceAfter=5
    )
    normal_style = styles['Normal']
    section_style = ParagraphStyle( # ADDED MISSING SECTION_STYLE HERE!
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=20
    )

    # Content elements
    elements = []

    # Title
    elements.append(Paragraph("Project 'Secure Messenger v2' - Weekly Update", title_style))
    elements.append(Spacer(1, 10))

    # Metadata section at the beginning
    elements.append(Paragraph("Document Type: Project Update Email", metadata_style))
    elements.append(Paragraph("Confidentiality: PUBLIC (Internal)", metadata_style)) # Marked as Public Internal
    elements.append(Paragraph("Project: Secure Messenger v2", metadata_style))
    elements.append(Paragraph("Date: October 26, 2023", metadata_style))
    elements.append(Spacer(1, 10))

    # Email Headers
    elements.append(Paragraph("TO: All ACME Employees", header_style))
    elements.append(Paragraph("FROM: Michael Brown, Lead Developer", header_style))
    elements.append(Paragraph("SUBJECT: Project Update - Secure Messenger v2 - Week of Oct 23rd", header_style))
    elements.append(Spacer(1, 15))

    # Email Body
    elements.append(Paragraph(
        "Hi Team,", normal_style
    ))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(
        "This is a brief update on the 'Secure Messenger v2' project for the week of October 23rd.", normal_style
    ))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Key Accomplishments this Week:", section_style))
    elements.append(Paragraph(
        "• Completed development of end-to-end encryption for messaging.\n"
        "• Successfully integrated secure file sharing feature.\n"
        "• Finished testing on iOS and Android platforms.", normal_style
    ))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Next Week's Focus:", section_style))
    elements.append(Paragraph(
        "• Begin performance testing and optimization.\n"
        "• Finalize user interface design for mobile apps.\n"
        "• Prepare for initial internal beta release.", normal_style
    ))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Potential Roadblocks:", section_style))
    elements.append(Paragraph(
        "• Minor delays expected in UI design due to designer availability.\n"
        "• We anticipate needing extra testing time for performance on older Android devices.", normal_style
    ))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "We are on track for the planned internal beta release next month. Keep up the great work!", normal_style
    ))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "Best regards,\nMichael Brown\nLead Developer", normal_style
    ))
    elements.append(Spacer(1, 10))

    # Metadata at the end
    elements.append(Paragraph("--- End of Project Update Email ---", metadata_style))

    # Build PDF
    doc.build(elements)
    return file_path

def generate_training_manual(output_dir):
    """Generate fake training manual PDF (NEW FILE) - Non-confidential, procedural data"""
    file_path = os.path.join(output_dir, "training_manual.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=20
    )
    subsection_style = ParagraphStyle(
        'Subsection',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=10
    )
    metadata_style = ParagraphStyle( # New style for metadata
        'Metadata',
        parent=styles['Italic'],
        fontSize=8,
        alignment=TA_LEFT,
        textColor=colors.grey,
        spaceAfter=5
    )
    normal_style = styles['Normal']
    bullet_style = styles['Bullet']

    # Content elements
    elements = []

    # Title
    elements.append(Paragraph("ACME Secure Messenger - User Training Manual", title_style))
    elements.append(Paragraph("PUBLIC - For Employee Training", title_style)) # Marked PUBLIC Training Manual
    elements.append(Spacer(1, 20))

    # Metadata Section
    elements.append(Paragraph("Document Type: Training Manual", metadata_style))
    elements.append(Paragraph("Confidentiality: PUBLIC", metadata_style)) # Marked PUBLIC
    elements.append(Paragraph("Product: ACME Secure Messenger", metadata_style))
    elements.append(Paragraph("Version: 1.0", metadata_style))
    elements.append(Paragraph("Audience: All Employees", metadata_style))
    elements.append(Spacer(1, 10))

    # 1. Getting Started
    elements.append(Paragraph("1. Getting Started with ACME Secure Messenger", section_style))

    # 1.1. Installation
    elements.append(Paragraph("1.1. Installation", subsection_style))
    elements.append(Paragraph(
        "To install ACME Secure Messenger, please follow these steps:", normal_style
    ))
    elements.append(Paragraph("• Step 1: Navigate to the ACME Corp software portal.", bullet_style, bulletText='•'))
    elements.append(Paragraph("• Step 2: Download the installer for your operating system (Windows/macOS/Linux).", bullet_style, bulletText='•'))
    elements.append(Paragraph("• Step 3: Run the installer and follow the on-screen instructions.", bullet_style, bulletText='•'))
    elements.append(Spacer(1, 5))

    # 1.2. First Login
    elements.append(Paragraph("1.2. First Login", subsection_style))
    elements.append(Paragraph(
        "Upon first launch, you will be prompted to log in. Use your ACME Corp employee credentials:", normal_style
    ))
    elements.append(Paragraph("• Username: Your ACME Corp email address", bullet_style, bulletText='•'))
    elements.append(Paragraph("• Password: Your standard ACME Corp network password", bullet_style, bulletText='•'))
    elements.append(Spacer(1, 10))

    # 2. Using Secure Messaging
    elements.append(Paragraph("2. Using Secure Messaging Features", section_style))

    # 2.1. Sending Encrypted Messages
    elements.append(Paragraph("2.1. Sending Encrypted Messages", subsection_style))
    elements.append(Paragraph(
        "All messages sent via ACME Secure Messenger are end-to-end encrypted. To send a message:", normal_style
    ))
    elements.append(Paragraph("• Step 1: Click on 'New Message'.", bullet_style, bulletText='•'))
    elements.append(Paragraph("• Step 2: Select the recipient(s) from your contact list.", bullet_style, bulletText='•'))
    elements.append(Paragraph("• Step 3: Type your message in the text field.", bullet_style, bulletText='•'))
    elements.append(Paragraph("• Step 4: Click 'Send'. The message will be automatically encrypted.", bullet_style, bulletText='•'))
    elements.append(Spacer(1, 5))

    # 2.2. Secure File Sharing
    elements.append(Paragraph("2.2. Secure File Sharing", subsection_style))
    elements.append(Paragraph(
        "To securely share files:", normal_style
    ))
    elements.append(Paragraph("• Step 1: In a conversation, click the 'Attach File' icon.", bullet_style, bulletText='•'))
    elements.append(Paragraph("• Step 2: Select the file you wish to share.", bullet_style, bulletText='•'))
    elements.append(Paragraph("• Step 3: Click 'Send'. The file will be encrypted before upload and transmission.", bullet_style, bulletText='•'))
    elements.append(Spacer(1, 10))

    # Metadata at the end
    elements.append(Paragraph("--- End of Training Manual ---", metadata_style))

    # Build PDF
    doc.build(elements)
    return file_path


def main():
    """Generate all fake company documents (version 2)"""
    output_dir = create_company_directory()

    print("Generating fake company documents (version 2) with metadata...")

    # Generate documents
    employee_handbook = generate_employee_handbook(output_dir)
    product_specs = generate_product_specs(output_dir)
    internal_memo = generate_internal_memo(output_dir)
    security_audit_report = generate_security_audit_report(output_dir) # New file
    project_update_email = generate_project_update_email(output_dir)     # New file
    training_manual = generate_training_manual(output_dir)             # New file

    print(f"Created employee handbook: {employee_handbook}")
    print(f"Created product specifications: {product_specs}")
    print(f"Created internal memo: {internal_memo}")
    print(f"Created security audit report: {security_audit_report}") # New file output
    print(f"Created project update email: {project_update_email}")     # New file output
    print(f"Created training manual: {training_manual}")             # New file output

    print("Document generation complete! (Version 2 with metadata)")

if __name__ == "__main__":
    main()
