from datetime import datetime

def format_date(date_str):
    try:
        date_formats = [
            "%Y-%m-%d",      # 2024-01-15
            "%m/%d/%Y",      # 01/15/2024
            "%d/%m/%Y",      # 15/01/2024
            "%m-%d-%Y",      # 01-15-2024
            "%d-%m-%Y",      # 15-01-2024
            "%Y/%m/%d",      # 2024/01/15
            "%B %d, %Y",     # January 15, 2024
            "%b %d, %Y",     # Jan 15, 2024
            "%d %B %Y",      # 15 January 2024
            "%d %b %Y",      # 15 Jan 2024
        ]

        parsed_date = None
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
            except ValueError:
                continue

        if parsed_date is None:
            print(f"Error: Could not parse date '{date_str}'")
            print("Supported formats: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY, MM-DD-YYYY, DD-MM-YYYY, YYYY/MM/DD")
            print("                  'January 15, 2024', 'Jan 15, 2024', '15 January 2024', '15 Jan 2024'")
            return

        formatted_date = parsed_date.strftime("%m/%d/%Y")
        return formatted_date

    except Exception as e:
        print(f"Error while parsing date: {e}")
        return ""


