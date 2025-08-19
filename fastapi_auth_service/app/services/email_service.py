import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..core.config import settings


class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL
    
    def send_client_admin_credentials(self, email: str, username: str, password: str, user_id: int):
        """Send login credentials to newly created Client Admin"""
        
        subject = f"Welcome to {settings.APP_NAME} - Your Client Admin Account"
        
        # Create the email body
        body = f"""
        <html>
        <body>
            <h2>Welcome to {settings.APP_NAME}!</h2>
            <p>Your Client Admin account has been successfully created by the Super Administrator.</p>
            
            <h3>Your Login Credentials:</h3>
            <ul>
                <li><strong>User ID:</strong> {user_id}</li>
                <li><strong>Username:</strong> {username}</li>
                <li><strong>Password:</strong> {password}</li>
            </ul>
            
            <p><strong>Important:</strong> Please change your password after your first login for security purposes.</p>
            
            <h3>Login Link:</h3>
            <p>Click the link below to access your account:</p>
            <p><a href="{settings.LOGIN_URL}" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-decoration: none; border-radius: 4px;">Login to Your Account</a></p>
            
            <p>If the button doesn't work, copy and paste this URL into your browser:</p>
            <p>{settings.LOGIN_URL}</p>
            
            <h3>Security Notice:</h3>
            <ul>
                <li>Keep your credentials secure and do not share them with anyone</li>
                <li>Use a strong password when you change it</li>
                <li>Log out when you're done using the system</li>
                <li>Contact the Super Administrator if you have any issues</li>
            </ul>
            
            <p>Best regards,<br>{settings.APP_NAME} Team</p>
        </body>
        </html>
        """
        
        self._send_email(email, subject, body)
    
    def send_organizer_credentials(self, email: str, username: str, password: str, user_id: int, client_admin_name: str):
        """Send login credentials to newly created Organizer"""
        
        subject = f"Welcome to {settings.APP_NAME} - Your Organizer Account"
        
        # Create the email body
        body = f"""
        <html>
        <body>
            <h2>Welcome to {settings.APP_NAME}!</h2>
            <p>Your Organizer account has been successfully created by {client_admin_name}.</p>
            
            <h3>Your Login Credentials:</h3>
            <ul>
                <li><strong>User ID:</strong> {user_id}</li>
                <li><strong>Username:</strong> {username}</li>
                <li><strong>Password:</strong> {password}</li>
            </ul>
            
            <p><strong>Important:</strong> Please change your password after your first login for security purposes.</p>
            
            <h3>Login Link:</h3>
            <p>Click the link below to access your account:</p>
            <p><a href="{settings.LOGIN_URL}" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-decoration: none; border-radius: 4px;">Login to Your Account</a></p>
            
            <p>If the button doesn't work, copy and paste this URL into your browser:</p>
            <p>{settings.LOGIN_URL}</p>
            
            <h3>Your Role:</h3>
            <p>As an Organizer, you have access to organizer-specific features and can manage events and activities under the supervision of your Client Administrator.</p>
            
            <h3>Security Notice:</h3>
            <ul>
                <li>Keep your credentials secure and do not share them with anyone</li>
                <li>Use a strong password when you change it</li>
                <li>Log out when you're done using the system</li>
                <li>Contact your Client Administrator if you have any issues</li>
            </ul>
            
            <p>Best regards,<br>{settings.APP_NAME} Team</p>
        </body>
        </html>
        """
        
        self._send_email(email, subject, body)
    
    def send_password_reset(self, email: str, reset_token: str):
        """Send password reset link"""
        
        subject = f"{settings.APP_NAME} - Password Reset Request"
        
        reset_url = f"{settings.LOGIN_URL}?reset_token={reset_token}"
        
        body = f"""
        <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>You have requested to reset your password for {settings.APP_NAME}.</p>
            
            <p>Click the link below to reset your password:</p>
            <p><a href="{reset_url}" style="background-color: #4CAF50; color: white; padding: 14px 20px; text-decoration: none; border-radius: 4px;">Reset Password</a></p>
            
            <p>If the button doesn't work, copy and paste this URL into your browser:</p>
            <p>{reset_url}</p>
            
            <p><strong>Note:</strong> This link will expire in 1 hour for security reasons.</p>
            
            <p>If you didn't request this password reset, please ignore this email.</p>
            
            <p>Best regards,<br>{settings.APP_NAME} Team</p>
        </body>
        </html>
        """
        
        self._send_email(email, subject, body)
    
    def _send_email(self, to_email: str, subject: str, body: str):
        """Send email using SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach HTML body
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                
        except Exception as e:
            # In production, you might want to log this error
            print(f"Failed to send email to {to_email}: {str(e)}")
            raise Exception(f"Failed to send email: {str(e)}")


email_service = EmailService()
