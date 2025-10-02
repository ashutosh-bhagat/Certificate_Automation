# 🏆 Certificate Automation System

A Python-based automation tool that generates personalized certificates and sends them via email to recipients listed in a CSV file. Perfect for educational institutions, training programs, workshops, and events.

## ✨ Features

- **Automated Certificate Generation**: Overlays recipient names onto a base certificate PDF
- **Bulk Email Distribution**: Sends personalized certificates to multiple recipients from CSV data
- **Custom Font Support**: Uses custom fonts (KodeMono-SemiBold) for professional-looking certificates
- **Gmail Integration**: Seamless email delivery through Gmail SMTP
- **Flexible Configuration**: Multiple command-line options for testing and customization
- **Logging System**: Comprehensive logging of all operations for tracking and debugging
- **Error Handling**: Robust error handling with detailed logging
- **Dry Run Mode**: Test certificate generation without sending emails

## 📋 Requirements

### Dependencies

```
reportlab
PyPDF2
```

### Files Required

- `life of py certi.pdf` - Base certificate template
- `email and name.csv` - Recipient data (name, email)
- `KodeMono-SemiBold.ttf` - Custom font file
- Gmail account with App Password for SMTP

## 🚀 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ashutosh-bhagat/Certificate_Automation.git
   cd Certificate_Automation
   ```

2. **Install required packages**:

   ```bash
   pip install reportlab PyPDF2
   ```

3. **Set up your files**:

   - Place your certificate template as `life of py certi.pdf`
   - Create `email and name.csv` with recipient data
   - Add `KodeMono-SemiBold.ttf` font file

4. **Configure email credentials**:
   - Set environment variables for security:
     ```bash
     set SMTP_USERNAME=your_email@gmail.com
     set SMTP_PASSWORD=your_app_password
     ```
   - Or modify the script directly (less secure)

## 📊 CSV File Format

Your `email and name.csv` should follow this structure:

```csv
name,email
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
Mike Johnson,mike.johnson@example.com
```

## 🎯 Usage

### Basic Usage

```bash
python main.py
```

### Advanced Options

**Dry Run (Generate certificates without sending emails)**:

```bash
python main.py --dry-run
```

**Process only first N recipients**:

```bash
python main.py --limit 5
```

**Send to specific email only**:

```bash
python main.py --only-email "john.doe@example.com"
```

**Send to specific name only**:

```bash
python main.py --only-name "John Doe"
```

**Send ad-hoc certificate**:

```bash
python main.py --adhoc-email "test@example.com" --adhoc-name "Test User"
```

**Custom email subject and body**:

```bash
python main.py --subject "Your Achievement Certificate" --body "Congratulations on your completion!"
```

**Debug mode**:

```bash
python main.py --smtp-debug
```

**Send email without attachment** (for testing):

```bash
python main.py --no-attach
```

## ⚙️ Configuration

### Email Settings

- **SMTP Server**: Gmail (smtp.gmail.com:587)
- **Authentication**: Username/password (App Password recommended)
- **From Name**: "The A.I.M. Club Team"
- **Subject**: "Your Certificate of Participation For Life Of .py"

### Certificate Positioning

- **Font Size**: 36pt
- **Text Color**: White
- **Position**: Centered horizontally, 42% from bottom
- **Font**: KodeMono-SemiBold (fallback: Helvetica-Bold)

### File Paths

- Base Certificate: `life of py certi.pdf`
- CSV Data: `email and name.csv`
- Output Directory: `personalized_certs/`
- Log File: `certificates.log`

## 📁 Project Structure

```
Certificate_Automation/
├── main.py                    # Main automation script
├── life of py certi.pdf       # Base certificate template (gitignored)
├── email and name.csv         # Recipient data (gitignored)
├── KodeMono-SemiBold.ttf     # Custom font file (gitignored)
├── personalized_certs/       # Generated certificates (gitignored)
├── certificates.log          # Operation logs (gitignored)
├── README.md                 # This documentation
└── .gitignore               # Git ignore rules
```

## 🔐 Security Notes

1. **Email Credentials**: Use environment variables or Gmail App Passwords
2. **Sensitive Files**: CSV files and certificates are gitignored for privacy
3. **SMTP Security**: Uses TLS encryption for email transmission
4. **File Permissions**: Ensure proper file permissions for sensitive data

## 📝 Logging

The system logs all operations to `certificates.log` including:

- Certificate generation status
- Email delivery confirmations
- Error messages and stack traces
- Processing statistics

## 🛠️ Troubleshooting

### Common Issues

1. **Font not found**: Ensure `KodeMono-SemiBold.ttf` is in the correct location
2. **SMTP authentication failed**: Check Gmail App Password and 2FA settings
3. **PDF merge errors**: Verify the base certificate PDF is not corrupted
4. **CSV encoding issues**: Ensure CSV is saved with UTF-8 encoding

### Error Codes

- Missing CSV file: Check file path and permissions
- SMTP errors: Verify email credentials and network connectivity
- PDF processing errors: Check base certificate file integrity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👥 Support

For issues and questions:

- Create an issue on GitHub
- Check the logs in `certificates.log`
- Verify all configuration settings

---

**Made with ❤️ by The A.I.M. Club Team**
