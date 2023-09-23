from abc import ABC, abstractmethod

class UserView(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_notes(self, notes):
        pass

    @abstractmethod
    def display_commands(self, commands):
        pass

class ConsoleUserView(UserView):
    def display_contacts(self, contacts):
        result = []
        for account in contacts:
            # Display contact information in the desired format
            result.append(
                "_" * 50 + "\n" +
                f"Name: {account['name']}\n" +
                f"Phones: {', '.join(account['phones'])}\n" +
                f"Birthday: {account['birthday']}\n" +
                f"Email: {account['email']}\n" +
                f"Status: {account['status']}\n" +
                f"Note: {account['note']}\n" +
                "_" * 50 + '\n'
            )
        print('\n'.join(result))

    def display_notes(self, notes):
        # Display notes in the desired format
        print("Notes:")
        for note in notes:
            print(note)
        print()

    def display_commands(self, commands):
        # Display available commands
        print("Available commands:")
        for command in commands:
            print(command)
        print()



