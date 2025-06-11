import csv
import os

def generate_mock_data():
    """Generates a CSV file with mock historical support ticket data."""
    data = [
        ["ticket_id", "customer_id", "request", "category", "suggested_solution"],
        ["TICK-001", "CUST-101", "I can't log in, I forgot my password.", "Password Reset", "Please follow the password reset link on the login page."],
        ["TICK-002", "CUST-102", "My monthly bill is higher than I expected.", "Billing", "You can view a detailed breakdown of your charges in the 'Billing' section of your account dashboard."],
        ["TICK-003", "CUST-103", "How do I add a new user to my team?", "General Inquiry", "To add a new user, go to 'Team Settings', click 'Invite User', and enter their email address."],
        ["TICK-004", "CUST-101", "I tried resetting my password but the link didn't work.", "Technical", "I have manually resent the password reset link to your email. Please check your spam folder as well."],
        ["TICK-005", "CUST-104", "The API is returning a 500 error on the /v1/data endpoint.", "Technical", "Our engineering team has identified a temporary issue with the /v1/data endpoint and is working on a fix. We expect it to be resolved within the hour."],
        ["TICK-006", "CUST-105", "My account has been suspended and I don't know why.", "Account Suspension", "Please check your email for a suspension notification. If you need to appeal, contact our support team with your account details."],
        ["TICK-007", "CUST-106", "How do I set up two-factor authentication?", "Security", "Go to Security Settings in your profile and click 'Enable Two-Factor Authentication'. Follow the setup wizard to configure your authenticator app."],
        ["TICK-008", "CUST-107", "I want to upgrade my plan to Pro.", "Plan Upgrade", "Navigate to the 'Billing' section and click 'Upgrade' next to the Pro plan. Your new features will be available immediately."],
        ["TICK-009", "CUST-108", "The mobile app keeps crashing on my iPhone.", "Mobile App", "Please update to the latest app version from the App Store. If the issue persists, try restarting your device."],
        ["TICK-010", "CUST-109", "I'm not receiving email notifications anymore.", "Email Notifications", "Check your notification settings in your profile and ensure the email address is correct. Also check your spam folder."],
        ["TICK-011", "CUST-110", "How can I export all my data?", "Data Export", "Go to Settings > Data Export, select the data types you want, choose a format, and click 'Request Export'. You'll receive an email when ready."],
        ["TICK-012", "CUST-111", "I need help integrating with your API.", "API Integration", "Check our API documentation at docs.example.com/api. Generate an API key in your dashboard under 'API Keys' section."],
        ["TICK-013", "CUST-112", "My API key doesn't seem to be working.", "API Integration", "Ensure you're including the API key in the Authorization header as 'Bearer YOUR_API_KEY' and that requests are made over HTTPS."],
        ["TICK-014", "CUST-113", "I'm getting charged for API overages but I don't understand why.", "Billing", "API usage beyond your plan's included limit incurs overage charges. Check your usage statistics in the dashboard."],
        ["TICK-015", "CUST-114", "Can I downgrade my plan?", "Plan Upgrade", "Plan downgrades take effect at your next billing cycle. You can initiate this in the Billing section of your account."],
        ["TICK-016", "CUST-115", "I lost my phone and can't access my 2FA codes.", "Security", "Use your backup recovery codes to log in. If you don't have them, contact support immediately for account recovery."],
        ["TICK-017", "CUST-116", "The password reset email isn't arriving.", "Password Reset", "Check your spam folder and ensure you're using the correct email address. If still not received, contact support for manual reset."],
        ["TICK-018", "CUST-117", "I accidentally deleted important data. Can you restore it?", "Data Recovery", "We maintain backups for 30 days. Please provide the specific data and timeframe, and we'll check if restoration is possible."],
        ["TICK-019", "CUST-118", "My account was charged twice this month.", "Billing", "This appears to be a duplicate charge. I've initiated a refund for the duplicate payment. You should see it within 3-5 business days."],
        ["TICK-020", "CUST-119", "The app is very slow on my Android device.", "Mobile App", "Clear the app cache in your device settings. Also ensure you have sufficient storage space and close other running apps."],
        ["TICK-021", "CUST-120", "How do I change my email address?", "General Inquiry", "Go to Account Settings and update your email address. You'll receive a confirmation email at the new address to verify the change."],
        ["TICK-022", "CUST-121", "I'm getting 401 Unauthorized errors with the API.", "API Integration", "This indicates an invalid API key. Regenerate your API key in the dashboard and ensure it's correctly included in your requests."],
        ["TICK-023", "CUST-122", "Can I get a refund for last month's charges?", "Billing", "Refunds are processed on a case-by-case basis. Please provide more details about why you're requesting a refund."],
        ["TICK-024", "CUST-123", "I want to delete my account permanently.", "Account Management", "Account deletion is permanent and cannot be undone. If you're sure, please confirm via email and we'll process the deletion."],
        ["TICK-025", "CUST-124", "The data export is taking too long.", "Data Export", "Large exports can take up to 24 hours to process. You'll receive an email notification when your export is ready for download."],
        ["TICK-026", "CUST-125", "I'm hitting API rate limits too quickly.", "API Integration", "Consider upgrading your plan for higher rate limits, or implement request throttling in your application to stay within limits."],
        ["TICK-027", "CUST-126", "Can I use SMS for two-factor authentication?", "Security", "Yes, SMS backup can be configured as a secondary 2FA method in your Security Settings, though we recommend using an authenticator app."],
        ["TICK-028", "CUST-127", "I need to update my payment method.", "Billing", "Go to Billing > Payment Methods, add your new payment method, and set it as the default for future charges."],
        ["TICK-029", "CUST-128", "The mobile app won't sync my latest changes.", "Mobile App", "Check your internet connection and try pulling down to refresh. If the issue persists, log out and log back in."],
        ["TICK-030", "CUST-129", "I want to stop receiving marketing emails.", "Email Notifications", "Update your notification preferences in Settings > Notifications and disable the 'Marketing' category."],
        ["TICK-031", "CUST-130", "My team member can't access their account.", "General Inquiry", "Have them try resetting their password. If they're still unable to access, check if their account is active in your team settings."],
        ["TICK-032", "CUST-131", "I'm seeing 429 Too Many Requests errors.", "API Integration", "You've exceeded your API rate limit. Wait for the rate limit to reset or upgrade your plan for higher limits."],
        ["TICK-033", "CUST-132", "How do I cancel my subscription?", "Plan Management", "You can cancel your subscription in the Billing section. Your access will continue until the end of your current billing period."],
        ["TICK-034", "CUST-133", "I need to change my company name on the invoice.", "Billing", "Please provide the correct company name and we'll update your billing information for future invoices."],
        ["TICK-035", "CUST-134", "The app crashes when I try to upload files.", "Mobile App", "This may be due to file size limits or insufficient storage. Try uploading smaller files or clearing the app cache."],
        ["TICK-036", "CUST-135", "I can't find my downloaded data export.", "Data Export", "Check your email for the download link. The export links expire after 7 days, so you may need to request a new export."],
        ["TICK-037", "CUST-136", "Is there an API endpoint for user management?", "API Integration", "Yes, we have user management endpoints. Check the 'User Management' section in our API documentation for details."],
        ["TICK-038", "CUST-137", "My authenticator app was accidentally deleted.", "Security", "You can use your backup recovery codes to log in, then set up 2FA again with a new authenticator app."],
        ["TICK-039", "CUST-138", "I need a receipt for my payment.", "Billing", "All receipts are automatically emailed after payment. You can also download them from the Billing History section."],
        ["TICK-040", "CUST-139", "The website is loading very slowly.", "Technical", "We're investigating reports of slow loading times. Try clearing your browser cache or using a different browser as a temporary workaround."],
        ["TICK-041", "CUST-140", "How do I remove a team member?", "General Inquiry", "Go to Team Settings, find the member you want to remove, and click the 'Remove' button next to their name."],
        ["TICK-042", "CUST-141", "I'm getting SSL certificate errors.", "Technical", "This may be a temporary issue. Try refreshing the page or clearing your browser cache. If it persists, contact our technical team."],
        ["TICK-043", "CUST-142", "Can I get usage analytics for my API calls?", "API Integration", "Yes, detailed API usage analytics are available in your dashboard under the 'Analytics' section."],
        ["TICK-044", "CUST-143", "I forgot to save my backup codes for 2FA.", "Security", "For security reasons, backup codes can't be retrieved. You'll need to disable and re-enable 2FA to get new codes."],
        ["TICK-045", "CUST-144", "My trial period is ending. What happens next?", "Plan Management", "Your trial will convert to a Free plan unless you upgrade. You can upgrade anytime in the Billing section to maintain premium features."],
        ["TICK-046", "CUST-145", "I need help with webhook configuration.", "API Integration", "Check our webhook documentation for setup instructions. Ensure your endpoint is accessible and returns a 200 status code."],
        ["TICK-047", "CUST-146", "The mobile app isn't showing the latest updates.", "Mobile App", "Force close the app and restart it. If that doesn't work, check if there's an app update available in your app store."],
        ["TICK-048", "CUST-147", "I want to switch from monthly to annual billing.", "Billing", "You can change your billing cycle in the Billing section. Annual billing offers a discount compared to monthly payments."],
        ["TICK-049", "CUST-148", "How do I enable email notifications for my team?", "Email Notifications", "Team notification settings can be configured in Team Settings. Each member can also customize their individual preferences."],
        ["TICK-050", "CUST-149", "I'm having trouble with file upload limits.", "Technical", "Free plans have a 10MB file limit, Pro plans allow 100MB. Check your plan limits or consider upgrading for larger file uploads."],
        ["TICK-051", "CUST-150", "How do I enable dark mode in the app?", "General Inquiry", "Dark mode can be enabled in the app settings under 'Appearance'. You can also set it to follow your system preference."],
        ["TICK-052", "CUST-151", "My data export file seems corrupted.", "Data Export", "Please try downloading the export again. If the issue persists, request a new export as the file may have been corrupted during transfer."],
        ["TICK-053", "CUST-152", "Can I set different permissions for team members?", "General Inquiry", "Yes, go to Team Settings and click on a member's name to adjust their role and permissions. We offer Admin, Editor, and Viewer roles."],
        ["TICK-054", "CUST-153", "I'm getting timeout errors when uploading large files.", "Technical", "Large file uploads may timeout on slower connections. Try uploading smaller files or check if your internet connection is stable."]
    ]

    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filepath = os.path.join(output_dir, "resolved_tickets.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    print(f"✅ Mock database created at '{filepath}' with {len(data)-1} tickets")

if __name__ == "__main__":
    generate_mock_data()