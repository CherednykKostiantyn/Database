class View:
    def show_lines(self, lines, choice_table):
        print("Lines:")
        if choice_table == 1:
            for line in lines:
                print(f"Journal ID: {line[0]}, Journal Name: {line[1]}, ISSN: {line[2]}, Year Established: {line[3]}")
        elif choice_table == 2:
            for line in lines:
                print(f"Research ID: {line[0]}, Title: {line[1]}, Description: {line[2]}, Date: {line[3]}")
        elif choice_table == 3:
            for line in lines:
                print(f"Author ID: {line[0]}, Firstname: {line[1]}, Surname: {line[2]}, Email: {line[3]}")
        elif choice_table == 4:
            for line in lines:
                print(f"Author ID: {line[0]}, Journal ID: {line[1]}")
        elif choice_table == 5:
            for line in lines:
                print(f"Author ID: {line[0]}, Research ID: {line[1]}")
        elif choice_table == 6:
            for line in lines:
                print(f"Research ID: {line[0]}, Journal ID: {line[1]}, Publication Date: {line[2]}")
        else:
            self.show_message("Error: Invalid table choice for displaying lines.")

    def get_line_input(self, choice_table):
        if choice_table == 1:
            while True:
                journal_name = input("Enter Journal Name: ")
                ISSN = input("Enter ISSN: ")
                year_established = input("Enter Year Established: ")
                if journal_name and ISSN and year_established.isdigit():
                    return journal_name, ISSN, year_established
                else:
                    self.show_message("Error: Invalid input! Please ensure all fields are correctly filled.")
        elif choice_table == 2:
            while True:
                title = input("Enter Title: ")
                description = input("Enter Description: ")
                date = input("Enter Date (YYYY-MM-DD): ")
                if title and description and date:
                    return title, description, date
                else:
                    self.show_message("Error: Invalid input! Please ensure all fields are correctly filled.")
        elif choice_table == 3:
            while True:
                firstname = input("Enter Firstname: ")
                surname = input("Enter Surname: ")
                email = input("Enter Email: ")
                if firstname and surname and email:
                    return firstname, surname, email
                else:
                    self.show_message("Error: Invalid input! Please ensure all fields are correctly filled.")
        elif choice_table == 4:
            while True:
                author_id = input("Enter Author_id: ")
                journal_id = input("Enter Journal_id: ")
                if author_id and journal_id:
                    return  author_id, journal_id
                else:
                    self.show_message("Error: Invalid input! Please ensure all fields are correctly filled.")
        elif choice_table == 5:
            while True:
                author_id = input("Enter Author_id: ")
                research_id = input("Enter Research_id: ")
                if author_id and research_id:
                    return author_id, research_id
                else:
                    self.show_message("Error: Invalid input! Please ensure all fields are correctly filled.")
        elif choice_table == 6:
            while True:
                research_id, journal_id, publication_date
                research_id = input("Enter Research_id: ")
                journal_id = input("Enter Journal_id: ")
                publication_date = input("Enter Date: ")
                if research_id and journal_id and publication_date:
                    return research_id, journal_id, publication_date
                else:
                    self.show_message("Error: Invalid input! Please ensure all fields are correctly filled.")
        else:
            self.show_message("Error: Invalid input! Please ensure all fields are correctly filled.")

    def get_line_in_author_journal(self):
        while True:
            self.show_message("Since this table uses a composite key, please provide the current (old) and new values.")
            old_author_id = input("Enter old_author_id: ")
            old_journal_id = input("Enter old_journal_id: ")
            new_author_id = input("Enter new_author_id: ")
            new_journal_id = input("Enter new_journal_id: ")
            if old_author_id and old_journal_id and old_author_id.isdigit() and old_journal_id.isdigit() and new_author_id and new_journal_id and new_author_id.isdigit() and new_journal_id.isdigit():
                return old_author_id, old_journal_id, new_author_id, new_journal_id
            else:
                self.show_message("Error: Something is clearly wrong -_-")

    def get_line_in_author_research(self):
        while True:
            self.show_message("Since this table uses a composite key, please provide the current (old) and new values.")
            old_author_id = input("Enter old_author_id: ")
            old_research_id = input("Enter old_research_id: ")
            new_author_id = input("Enter new_author_id: ")
            new_research_id = input("Enter new_research_id: ")
            if old_author_id and old_research_id and old_author_id.isdigit() and old_research_id.isdigit() and new_author_id and new_research_id and new_author_id.isdigit() and new_research_id.isdigit():
                return old_author_id, old_research_id, new_author_id, new_research_id
            else:
                self.show_message("Error: Something is clearly wrong -_-")

    def get_line_in_publication(self):
        while True:
            self.show_message("Since this table uses a composite key, please provide the current (old) and new values.")
            old_research_id = input("Enter old_research_id: ")
            old_journal_id = input("Enter old_journal_id: ")
            new_research_id = input("Enter new_research_id: ")
            new_journal_id = input("Enter new_journal_id: ")
            new_publication_date = input("Enter new_publication_date (YYYY-MM-DD): ")
            if old_research_id and old_journal_id and old_research_id.isdigit() and old_journal_id.isdigit() and new_research_id and new_journal_id and new_research_id.isdigit() and new_journal_id.isdigit() and new_publication_date:
                return old_research_id, old_journal_id, new_research_id, new_journal_id, new_publication_date
            else:
                self.show_message("Error: Something is clearly wrong -_-")

    def get_line_id(self):
        while True:
            check = input("Enter line ID: ").strip()
            if check.isdigit():
                return int(check)
            else:
                self.show_message("Error: ID must be a number!")


    def show_message(self, message):
        print(message)

    def show_search_results(self, lines, header):
        print(f"\n{header}")
        if lines:
            headers = [
                "Journal Name", "ISSN", "Year Established",
                "Research Title", "Research Description",
                "Author Firstname", "Author Surname"
            ]

            column_widths = [max(len(str(row[i])) for row in lines) for i in range(len(headers))]
            column_widths = [max(column_widths[i], len(headers[i])) for i in range(len(headers))]

            header_row = "  ".join(f"{headers[i]:<{column_widths[i]}}" for i in range(len(headers)))
            print(header_row)


            for line in lines:
                print("  ".join(f"{str(line[i]):<{column_widths[i]}}" for i in range(len(line))))
        else:
            print("No results found.")

