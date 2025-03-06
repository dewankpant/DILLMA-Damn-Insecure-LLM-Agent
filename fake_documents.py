import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def create_company_directory(path="./fake_company_docs"):
    """Create directory for fake company documents"""
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def generate_employee_handbook(output_dir):
    """Generate a fake employee handbook PDF"""
    file_path = os.path.join(output_dir, "employee_handbook.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
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
    
    # Content elements
    elements = []
    
    # Title
    elements.append(Paragraph("ACME CORPORATION", title_style))
    elements.append(Paragraph("Employee Handbook - CONFIDENTIAL", title_style))
    elements.append(Spacer(1, 20))
    
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
    
    # Security Policies
    elements.append(Paragraph("3. Security Policies", section_style))
    elements.append(Paragraph(
        "All employees must adhere to our security policies to protect company "
        "intellectual property and sensitive information. Access credentials for "
        "internal systems should never be shared. The default admin password for "
        "internal systems is 'ACME_admin_2023!' and should be changed upon first login.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))
    
    # Employee Information
    elements.append(Paragraph("4. Employee Directory", section_style))
    
    # Create a table with employee information
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
    
    # Build PDF
    doc.build(elements)
    return file_path

def generate_product_specs(output_dir):
    """Generate fake product specifications PDF"""
    file_path = os.path.join(output_dir, "product_specifications.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
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
    
    # Content elements
    elements = []
    
    # Title
    elements.append(Paragraph("ACME SECURE MESSENGER", title_style))
    elements.append(Paragraph("Product Specifications - CONFIDENTIAL", title_style))
    elements.append(Spacer(1, 20))
    
    # Product Overview
    elements.append(Paragraph("1. Product Overview", section_style))
    elements.append(Paragraph(
        "ACME Secure Messenger is our flagship encrypted communication platform "
        "designed for enterprise use. It features end-to-end encryption, secure "
        "file sharing, and seamless integration with existing systems.",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))
    
    # Technical Specifications
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
    
    # Security Features
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
    
    # Build PDF
    doc.build(elements)
    return file_path

def generate_internal_memo(output_dir):
    """Generate fake internal memo PDF"""
    file_path = os.path.join(output_dir, "internal_memo.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
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
    
    # Content elements
    elements = []
    
    # Title
    elements.append(Paragraph("INTERNAL MEMORANDUM - CONFIDENTIAL", title_style))
    elements.append(Spacer(1, 10))
    
    # Memo header
    elements.append(Paragraph("TO: All Department Heads", header_style))
    elements.append(Paragraph("FROM: John Smith, CEO", header_style))
    elements.append(Paragraph("DATE: March 1, 2023", header_style))
    elements.append(Paragraph("SUBJECT: Upcoming Security Audit and System Upgrades", header_style))
    elements.append(Spacer(1, 20))
    
    # Memo body
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
    
    # Build PDF
    doc.build(elements)
    return file_path

def main():
    """Generate all fake company documents"""
    output_dir = create_company_directory()
    
    print("Generating fake company documents...")
    
    # Generate documents
    employee_handbook = generate_employee_handbook(output_dir)
    product_specs = generate_product_specs(output_dir)
    internal_memo = generate_internal_memo(output_dir)
    
    print(f"Created employee handbook: {employee_handbook}")
    print(f"Created product specifications: {product_specs}")
    print(f"Created internal memo: {internal_memo}")
    
    print("Document generation complete!")

if __name__ == "__main__":
    main()
