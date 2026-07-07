class Email:
    def __init__(self, email_address, subject_line, email_content):
        self.email_address = email_address
        self.subject_line = subject_line
        self.email_content = email_content
        # New emails default to unread
        self.has_been_read = False

    def mark_as_read(self):
        """
        Updates the 'has_been_read' attribute from False to True.
        """
        self.has_been_read = True



# Global inbox list to store Email objects
inbox = []

def populate_inbox():
    email1 = Email("hyperion@bootcamp.com", "Welcome to HyperionDev!", "We are thrilled to have you onboard for your engineering journey.")
    email2 = Email("tutor@bootcamp.com", "Great work on the bootcamp!", "You're making great progress!")
    email3 = Email("noreply@bootcamp.com", "Your excellent marks!", "You're doing amazing, keep it up!")
    inbox.extend([email1, email2, email3])

def list_emails():
    """
    Displays all email subject lines with their corresponding index numbers.

    The index number can be used to select specific emails.
    """

    print("\nInbox:")
    for index, email in enumerate(inbox):
        status = "[Unread]" if not email.has_been_read else "[Read]"
        print(f"{index}\t{status} {email.subject_line}")


def read_email(index):
    """
    Displays the content of the email at the specified index and marks it as read.

    Args:
        index (int): The index of the email to read.
    """

    selected_email = inbox[index]

    # Display the email details
    print("\n===============================")
    print(f"From:    {selected_email.email_address}")
    print(f"Subject: {selected_email.subject_line}")
    print("--------------------------------")
    print(selected_email.email_content)
    print("===============================")

    # Mark the email as read
    selected_email.mark_as_read()

    print(f"\nEmail from {selected_email.email_address} marked as read.")   


# Automatically populate the inbox with sample emails when the module is imported
populate_inbox()

print("Welcome to your OOP email simulator Application!")

while True:
    print("\nEmail Client Menu:")
    print("1. Read an email")
    print("2. View unread emails")
    print("3. Quit application")

    choice = input("\nPlease select an option (1-3): ").strip()

    if choice == "1":
        list_emails()
        if not inbox:
            print("Your inbox is empty. No emails to read.")
            continue

        try:
            selection = int(input("\nEnter the number/index of the email you wish to read: "))
            read_email(selection)
        except ValueError:
            print("\n[Invalid input]. Please type a valid numerical index integer.")
    elif choice == "2":
        print("\n------- Unread Emails ---")
        has_unread = False

        # Accessing class instances to check 'has_been_unread' state directly
        for email in inbox:
            if not email.has_been_read:
                print(f". {email.subject_line}")
                has_unread = True

        if not has_unread:
            print("You have no unread emails! Your inbox is fully up to date.")

    elif choice == "3":
        print("\nShutting down the email simulator. Goodbye!")
        break
    else:
        print("\n[Invalid Selection]. Please choose a valid menu item options (1, 2, or 3).")