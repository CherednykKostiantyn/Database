from model import Model
from view import View

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            choice_table = self.select_table()
            if choice_table == '1':
                self.handle_table_operations(1)
            elif choice_table == '2':
                self.handle_table_operations(2)
            elif choice_table == '3':
                self.handle_table_operations(3)
            elif choice_table == '4':
                self.handle_table_operations(4)
            elif choice_table == '5':
                self.handle_table_operations(5)
            elif choice_table == '6':
                self.handle_table_operations(6)
            elif choice_table == '7':
                break

    def handle_table_operations(self, choice_table):
        while True:
            choice = self.show_menu()
            if choice == '1':
                self.add_line(choice_table)
            elif choice == '2':
                self.View(choice_table)
            elif choice == '3':
                self.update_line(choice_table)
            elif choice == '4':
                self.delete_line(choice_table)
            elif choice == '5':
                self.generate_random_strings(choice_table)
            elif choice == '6':
                self.search()
            elif choice == '7':
                break

    def select_table(self):
        self.view.show_message("\nSelect table:")
        self.view.show_message("1. Journal")
        self.view.show_message("2. Research")
        self.view.show_message("3. Author")
        self.view.show_message("4. Author_Journal")
        self.view.show_message("5. Author_Research")
        self.view.show_message("6. Publication")
        self.view.show_message("7. Quit")
        return input("Enter your choice: ")

    def show_menu(self):
        self.view.show_message("\nSelect operation:")
        self.view.show_message("1. Add line")
        self.view.show_message("2. View line")
        self.view.show_message("3. Update line")
        self.view.show_message("4. Delete line")
        self.view.show_message("5. Generate random")
        self.view.show_message("6. Search")
        self.view.show_message("7. Quit to Select table")
        return input("Enter your choice: ")


    def add_line(self, choice_table):
        if choice_table == 1:
            journal_name, ISSN, year_established = self.view.get_line_input(choice_table)
            self.model.add_journal(journal_name, ISSN, year_established)
            self.view.show_message("Line added successfully!")
        elif choice_table == 2:
            title, description, date = self.view.get_line_input(choice_table)
            self.model.add_research(title, description, date)
            self.view.show_message("Line added successfully!")
        elif choice_table == 3:
            firstname, surname, email = self.view.get_line_input(choice_table)
            self.model.add_author(firstname, surname, email)
            self.view.show_message("Line added successfully!")
        elif choice_table == 4:
            author_id, journal_id = self.view.get_line_input(choice_table)
            self.model.add_author_journal(author_id, journal_id)
            self.view.show_message("Line added successfully!")
        elif choice_table == 5:
            author_id, research_id = self.view.get_line_input(choice_table)
            self.model.add_research_author(author_id, research_id)
            self.view.show_message("Line added successfully!")
        elif choice_table == 6:
            research_id, journal_id, publication_date = self.view.get_line_input(choice_table)
            self.model.add_publication(research_id, journal_id, publication_date)
            self.view.show_message("Line added successfully!")

    def View(self, choice_table):
        if choice_table == 1:
            lines = self.model.view_table(1)
        elif choice_table == 2:
            lines = self.model.view_table(2)
        elif choice_table == 3:
            lines = self.model.view_table(3)
        elif choice_table == 4:
            lines = self.model.view_table(4)
        elif choice_table == 5:
            lines = self.model.view_table(5)
        elif choice_table == 6:
            lines = self.model.view_table(6)
        else:
            self.view.show_message("Error: view_line")
            return
        self.view.show_lines(lines, choice_table)

    def update_line(self, choice_table):
        if choice_table == 1:
            journal_id = self.view.get_line_id()
            journal_name, ISSN, YearEstablished = self.view.get_line_input(choice_table)
            self.model.update_journal(journal_id, journal_name, ISSN, YearEstablished)
            self.view.show_message("Line updated successfully!")
        elif choice_table == 2:
            research_id = self.view.get_line_id()
            title, description, date = self.view.get_line_input(choice_table)
            self.model.update_research(research_id, title, description, date)
            self.view.show_message("Line updated successfully!")
        elif choice_table == 3:
            author_id = self.view.get_line_id()
            firstname, surname, email = self.view.get_line_input(choice_table)
            self.model.update_author(author_id, firstname, surname, email)
            self.view.show_message("Line updated successfully!")
        elif choice_table == 4:
            old_author_id, old_journal_id, new_author_id, new_journal_id = self.view.get_line_in_author_journal()
            self.model.update_author_journal(old_author_id, old_journal_id, new_author_id, new_journal_id)
            self.view.show_message("Line updated successfully!")
        elif choice_table == 5:
            old_author_id, old_research_id, new_author_id, new_research_id = self.view.get_line_in_author_research()
            self.model.update_author_research(old_author_id, old_research_id, new_author_id, new_research_id)
            self.view.show_message("Line updated successfully!")
        elif choice_table == 6:
            old_research_id, old_journal_id, new_research_id, new_journal_id, new_date = self.view.get_line_in_publication()
            self.model.update_publication(old_research_id, old_journal_id, new_research_id, new_journal_id, new_date)
            self.view.show_message("Line updated successfully!")

    def delete_line(self, choice_table):
        if choice_table == 1:
            journal_id = self.view.get_line_id()
            self.model.delete_journal(journal_id)
            self.view.show_message("Line deleted successfully!")
        elif choice_table == 2:
            research_id = self.view.get_line_id()
            self.model.delete_research(research_id)
            self.view.show_message("Line deleted successfully!")
        elif choice_table == 3:
            author_id = self.view.get_line_id()
            self.model.delete_author(author_id)
            self.view.show_message("Line deleted successfully!")
        elif choice_table == 4:
            author_id, journal_id = self.view.get_line_input(choice_table)
            self.model.delete_author_journal(author_id, journal_id)
            self.view.show_message("Line deleted successfully!")
        elif choice_table == 5:
            author_id, research_id = self.view.get_line_input(choice_table)
            self.model.delete_author_research(author_id, research_id)
            self.view.show_message("Line deleted successfully!")
        elif choice_table == 6:
            research_id, journal_id = self.view.get_line_input(choice_table)
            self.model.delete_publication(research_id, journal_id)
            self.view.show_message("Line deleted successfully!")

    def generate_random_strings(self, choice_table):
        if choice_table == 1:
            count = int(input("Enter rows for Journal: "))
            self.model.random_insert_journal(count)
            self.view.show_message(f"{count} rows added to Journal.")
        elif choice_table == 2:
            count = int(input("Enter rows for Research: "))
            self.model.random_insert_research(count)
            self.view.show_message(f"{count} rows added to Research.")
        elif choice_table == 3:
            count = int(input("Enter rows for Author: "))
            self.model.random_insert_author(count)
            self.view.show_message(f"{count} rows added to Author.")
        elif choice_table == 4:
            count = int(input("Enter rows for Author_Journal: "))
            self.model.random_insert_author_journal(count)
            self.view.show_message(f"{count} rows added to Author_Journal.")
        elif choice_table == 5:
            count = int(input("Enter rows for Author_Research: "))
            self.model.random_insert_author_research(count)
            self.view.show_message(f"{count} rows added to Author_Research.")
        elif choice_table == 6:
            count = int(input("Enter rows for Publication: "))
            self.model.random_insert_publication(count)
            self.view.show_message(f"{count} rows added to Publication.")

    def search(self):
        self.view.show_message("Enter search criteria (leave blank to skip):")
        journal_name_filter = input("Journal Name : ") or None
        issn_filter = input("ISSN : ") or None
        year_established_filter = input("YearEstablished : ") or None
        research_title_filter = input("Research Title : ") or None
        description_filter = input("description: ") or None
        author_firstname_filter = input("Author Firstname: ") or None
        author_surname_filter = input("Author Surname: ") or None

        data = self.model.search(
            journal_name_filter,
            issn_filter,
            year_established_filter,
            research_title_filter,
            description_filter,
            author_firstname_filter,
            author_surname_filter,
        )
        self.view.show_search_results(data, "Search Results")
