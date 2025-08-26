# Google Calendar Booking Bot

A Python-based chatbot that integrates with Google Calendar API to automatically find available time slots and book demo meetings with participants. The bot specifically looks for 30-minute slots between 6:00 PM and 8:00 PM Iran Standard Time (IRST) and creates Google Meet events with email invitations and reminders.

## Features

- 🗓️ **Smart Scheduling**: Automatically finds free 30-minute time slots in your Google Calendar
- 🕐 **Time Zone Support**: Operates in Iran Standard Time (UTC+3:30)
- 👥 **Multi-participant Support**: Add multiple participants via email addresses
- 📧 **Automated Notifications**: Sends email invitations to all participants
- 📅 **Google Meet Integration**: Automatically creates Google Meet links for virtual meetings
- ⏰ **Reminder System**: Sets up email and popup reminders 30 minutes before the meeting
- 📊 **Conflict Detection**: Checks existing calendar events to avoid double-booking

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.7+** installed on your system
2. **Google Account** with Google Calendar access
3. **Google Cloud Console project** with Calendar API enabled

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/farhadkazemian/GoogleCalendarBookingBot.git
   cd GoogleCalendarBookingBot
   ```

2. **Install required Python packages:**
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

## Google API Setup

### Step 1: Enable Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click on it and press "Enable"

### Step 2: Create Credentials

1. In Google Cloud Console, go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application" as the application type
4. Name your OAuth 2.0 client (e.g., "Calendar Booking Bot")
5. Download the credentials JSON file
6. Rename it to `credentials.json` and place it in the project root directory

### Step 3: Set up OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External" user type (unless you're using Google Workspace)
3. Fill in the required information:
   - App name
   - User support email
   - Developer contact information
4. Add your email to the test users list
5. Add the following scope: `https://www.googleapis.com/auth/calendar`

## Usage

### Running the Application

1. **Start the booking bot:**
   ```bash
   python BookingApp.py
   ```

2. **First-time setup:**
   - A browser window will open for Google authentication
   - Sign in with your Google account
   - Grant permission to access your Google Calendar
   - The authentication token will be saved locally for future use

3. **Interactive booking process:**
   - The bot will display available 30-minute slots for the next 7 days
   - Choose a time slot by entering the corresponding number
   - Enter participant email addresses (comma-separated)
   - Confirm the booking

### Example Interaction

```
Welcome to the Demo Booking Chatbot!
Here are the available 30-minute slots for the next 7 days (in IRST):
1. 2025-08-27 18:00 to 18:30
2. 2025-08-27 18:30 to 19:00
3. 2025-08-28 18:00 to 18:30
4. 2025-08-28 19:30 to 20:00

Please select a slot (enter the number): 2
Enter participant email addresses (comma-separated): client@example.com, manager@company.com
Demo booked successfully! Event ID: abc123xyz
Google Meet Link: https://meet.google.com/abc-defg-hij
```

## Configuration

### Time Slots
The bot is configured to find available slots:
- **Time Range**: 6:00 PM to 8:00 PM (18:00 - 20:00)
- **Duration**: 30 minutes per slot
- **Time Zone**: Iran Standard Time (UTC+3:30)
- **Days Ahead**: 7 days from current date

### Meeting Details
Default meeting settings:
- **Title**: "ITvisa Meeting"
- **Description**: "We are looking forward to show the demo!"
- **Reminders**: Email and popup notifications 30 minutes before
- **Video Conference**: Google Meet automatically included

## File Structure

```
GoogleCalendarBookingBot/
├── BookingApp.py          # Main application file
├── credentials.json       # Google API credentials (not included)
├── token.pickle          # Authentication token (auto-generated)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Security Notes

- `credentials.json` contains sensitive API credentials and should never be committed to version control
- `token.pickle` stores your authentication token and is automatically generated
- Both files are included in `.gitignore` for security

## Troubleshooting

### Common Issues

1. **"credentials.json not found"**
   - Ensure you've downloaded and renamed the credentials file correctly
   - Place it in the same directory as `BookingApp.py`

2. **"Token has been expired or revoked"**
   - Delete `token.pickle` and run the application again
   - You'll need to re-authenticate with Google

3. **"No free slots available"**
   - Check your calendar for conflicting events in the 6-8 PM time range
   - The bot looks 7 days ahead - busy schedules might not have free slots

4. **"Permission denied" errors**
   - Verify that the Google Calendar API is enabled in your Google Cloud project
   - Check that the OAuth consent screen is properly configured

### Debug Mode

To see more detailed information about available slots and conflicts, you can modify the `get_free_slots()` function to print debug information.

## Customization

### Changing Time Range
To modify the booking hours, edit the `get_free_slots()` function:
```python
# Change from 18 (6 PM) to your desired start hour
day_start = (now + timedelta(days=day)).astimezone(IRST).replace(hour=18, minute=0, second=0, microsecond=0)
# Change range(4) to adjust number of 30-minute slots
for i in range(4):  # Four 30-minute slots = 2 hours
```

### Modifying Meeting Details
Update the `book_demo()` function to change:
- Meeting title (`summary`)
- Description
- Reminder timing
- Time zone

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the [Google Calendar API documentation](https://developers.google.com/calendar/api/guides/overview)
3. Open an issue in this repository

---

**Note**: This bot is specifically designed for demo bookings in Iran Standard Time. Modify the timezone settings in the code if you're in a different region.