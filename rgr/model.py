import psycopg2
import random


class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='1111',
            host='localhost',
            port=5432
        )
        self.tables()

    def tables(self):
        c = self.conn.cursor()

        c.execute('''
                CREATE TABLE IF NOT EXISTS Journal (
                    journal_id SERIAL PRIMARY KEY,
                    journal_name TEXT NOT NULL,
                    ISSN TEXT NOT NULL,
                    YearEstablished INTEGER
                )
            ''')

        c.execute('''
                CREATE TABLE IF NOT EXISTS Research (
                    research_id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    date DATE
                )
            ''')

        c.execute('''
                CREATE TABLE IF NOT EXISTS Author (
                    author_id SERIAL PRIMARY KEY,
                    firstname TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            ''')

        c.execute('''
                CREATE TABLE IF NOT EXISTS Author_Journal (
                    author_journal_id SERIAL PRIMARY KEY,
                    author_id INTEGER NOT NULL,
                    journal_id INTEGER NOT NULL,
                    FOREIGN KEY (author_id) REFERENCES Author(author_id) ON DELETE CASCADE,
                    FOREIGN KEY (journal_id) REFERENCES Journal(journal_id) ON DELETE CASCADE
                )
            ''')

        c.execute('''
                CREATE TABLE IF NOT EXISTS Research_Author (
                    research_author_id SERIAL PRIMARY KEY,
                    author_id INTEGER NOT NULL,
                    research_id INTEGER NOT NULL,
                    FOREIGN KEY (author_id) REFERENCES Author(author_id) ON DELETE CASCADE,
                    FOREIGN KEY (research_id) REFERENCES Research(research_id) ON DELETE CASCADE
                )
            ''')

        c.execute('''
                CREATE TABLE IF NOT EXISTS Publication (
                    publication_id SERIAL PRIMARY KEY,
                    research_id INTEGER NOT NULL,
                    journal_id INTEGER NOT NULL,
                    date DATE,
                    FOREIGN KEY (research_id) REFERENCES Research(research_id) ON DELETE CASCADE,
                    FOREIGN KEY (journal_id) REFERENCES Journal(journal_id) ON DELETE CASCADE
                )
            ''')

        self.conn.commit()

    def add_journal(self, journal_name, ISSN, YearEstablished):
        c = self.conn.cursor()
        c.execute('INSERT INTO Journal (journal_name, ISSN, YearEstablished) VALUES (%s, %s, %s)',
                  (journal_name, ISSN, YearEstablished))
        self.conn.commit()

    def add_research(self, title, description, date):
        c = self.conn.cursor()
        c.execute('INSERT INTO Research (title, description, date) VALUES (%s, %s, %s)', (title, description, date))
        self.conn.commit()

    def add_author(self, firstname, surname, email):
        c = self.conn.cursor()
        c.execute('INSERT INTO Author (firstname, surname, email) VALUES (%s, %s, %s)', (firstname, surname, email))
        self.conn.commit()

    def add_author_journal(self, author_id, journal_id):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM Author WHERE author_id = %s', (author_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: Author_id {author_id} does not exist.")
            return 0
        c.execute('SELECT COUNT(*) FROM Journal WHERE journal_id = %s', (journal_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: Journal_id {journal_id} does not exist.")
            return 0
        c.execute('INSERT INTO Author_Journal (author_id, journal_id) VALUES (%s, %s)', (author_id, journal_id))
        self.conn.commit()

    def add_research_author(self, author_id, research_id):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM Author WHERE author_id = %s', (author_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: Author_id {author_id} does not exist.")
            return 0
        c.execute('SELECT COUNT(*) FROM Research WHERE research_id = %s', (research_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: Research_id {research_id} does not exist.")
            return 0
        c.execute('INSERT INTO Research_Author (author_id, research_id) VALUES (%s, %s)', (author_id, research_id))
        self.conn.commit()

    def add_publication(self, research_id, journal_id, date):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM Research WHERE research_id = %s', (research_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: Research_id {research_id} does not exist.")
            return 0
        c.execute('SELECT COUNT(*) FROM Journal WHERE journal_id = %s', (journal_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: Journal_id {journal_id} does not exist.")
            return 0
        c.execute('INSERT INTO Publication (research_id, journal_id, date) VALUES (%s, %s, %s)',
                  (research_id, journal_id, date))
        self.conn.commit()



    def update_journal(self, journal_id, journal_name, ISSN, YearEstablished):
        c = self.conn.cursor()
        c.execute('UPDATE Journal SET journal_name=%s, ISSN=%s, YearEstablished=%s WHERE journal_id=%s',
                  (journal_name, ISSN, YearEstablished, journal_id))
        self.conn.commit()

    def update_research(self, research_id, title, description, date):
        c = self.conn.cursor()
        c.execute('UPDATE Research SET title=%s, description=%s, date=%s WHERE research_id=%s',
                  (title, description, date, research_id))
        self.conn.commit()

    def update_author(self, author_id, firstname, surname, email):
        c = self.conn.cursor()
        c.execute('UPDATE Author SET firstname=%s, surname=%s, email=%s WHERE author_id=%s',
                  (firstname, surname, email, author_id))
        self.conn.commit()

    def update_author_journal(self, old_author_id, old_journal_id, new_author_id, new_journal_id):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM Author WHERE author_id = %s', (new_author_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: new_author_id {new_author_id} does not exist.")
            return 0
        c.execute('SELECT COUNT(*) FROM Journal WHERE journal_id = %s', (new_journal_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: new_journal_id {new_journal_id} does not exist.")
            return 0
        c.execute('UPDATE Author_Journal SET author_id=%s, journal_id=%s WHERE author_id=%s AND journal_id=%s',
                  (new_author_id, new_journal_id, old_author_id, old_journal_id))
        self.conn.commit()

    def update_author_research(self, old_author_id, old_research_id, new_author_id, new_research_id):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM Author WHERE author_id = %s', (new_author_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: new_author_id {new_author_id} does not exist.")
            return 0
        c.execute('SELECT COUNT(*) FROM Research WHERE research_id = %s', (new_research_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: new_research_id {new_research_id} does not exist.")
            return 0
        c.execute('UPDATE Research_Author SET author_id=%s, research_id=%s WHERE author_id=%s AND research_id=%s',
                  (new_author_id, new_research_id, old_author_id, old_research_id))
        self.conn.commit()

    def update_publication(self, old_research_id, old_journal_id, new_research_id, new_journal_id, new_date):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM Research WHERE research_id = %s', (new_research_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: new_research_id {new_research_id} does not exist.")
            return 0
        c.execute('SELECT COUNT(*) FROM Journal WHERE journal_id = %s', (new_journal_id,))
        if c.fetchone()[0] == 0:
            print(f"Error: new_journal_id {new_journal_id} does not exist.")
            return 0
        c.execute(
            'UPDATE Publication SET research_id=%s, journal_id=%s, date=%s WHERE research_id=%s AND journal_id=%s',
            (new_research_id, new_journal_id, new_date, old_research_id, old_journal_id))
        self.conn.commit()

    def delete_journal(self, journal_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM Journal WHERE journal_id=%s', (journal_id,))
        self.conn.commit()

    def delete_research(self, research_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Publication WHERE research_id=%s', (research_id,))
        publications = c.fetchall()
        if publications:
            return
        c.execute('DELETE FROM Research WHERE research_id=%s', (research_id,))
        self.conn.commit()

    def delete_author(self, author_id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM Author_Journal WHERE author_id=%s', (author_id,))
        author_journals = c.fetchall()
        if author_journals:
            return
        c.execute('SELECT * FROM Research_Author WHERE author_id=%s', (author_id,))
        research_authors = c.fetchall()
        if research_authors:
            return
        c.execute('DELETE FROM Author WHERE author_id=%s', (author_id,))
        self.conn.commit()

    def delete_author_journal(self, author_journal_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM Author_Journal WHERE author_journal_id=%s', (author_journal_id,))
        self.conn.commit()

    def delete_research_author(self, research_author_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM Research_Author WHERE research_author_id=%s', (research_author_id,))
        self.conn.commit()

    def delete_publication(self, publication_id):
        c = self.conn.cursor()
        c.execute('DELETE FROM Publication WHERE publication_id=%s', (publication_id,))
        self.conn.commit()

    def view_table(self, choice_table):
        c = self.conn.cursor()
        if choice_table == 1:
            c.execute('SELECT * FROM journal')
        elif choice_table == 2:
            c.execute('SELECT * FROM research')
        elif choice_table == 3:
            c.execute('SELECT * FROM author')
        elif choice_table == 4:
            c.execute('SELECT * FROM author_journal')
        elif choice_table == 5:
            c.execute('SELECT * FROM research_author')
        elif choice_table == 6:
            c.execute('SELECT * FROM publication')
        else:
            print("get_all_line error")
        return c.fetchall()

    def random_insert_journal(self, count):
        c = self.conn.cursor()
        query = f"INSERT INTO Journal (journal_name, ISSN, YearEstablished) SELECT 'Journal' || trunc(1 + random()*100)::int,  trunc(1 + random()*1000)::int, trunc(1900 + random()*100)::int FROM generate_series(1, {count})"
        c.execute(query)
        self.conn.commit()

    def random_insert_research(self, count):
        c = self.conn.cursor()
        for _ in range(count):
            title = f'Research {random.randint(1, 1000)}'
            description = f'Description of research {random.randint(1, 1000)}'
            date = f'2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'
            c.execute('INSERT INTO Research (title, description, date) VALUES (%s, %s, %s)', (title, description, date))
        self.conn.commit()

    def random_insert_author(self, count):
        c = self.conn.cursor()
        for _ in range(count):
            firstname = f'Firstname{random.randint(1, 1000)}'
            surname = f'Surname{random.randint(1, 1000)}'
            email = f'{firstname.lower()}@gmail.com'
            c.execute('INSERT INTO Author (firstname, surname, email) VALUES (%s, %s, %s)', (firstname, surname, email))
        self.conn.commit()

    def random_insert_author_journal(self, count):
        c = self.conn.cursor()
        c.execute('SELECT author_id FROM Author')
        author_ids = [row[0] for row in c.fetchall()]
        c.execute('SELECT journal_id FROM Journal')
        journal_ids = [row[0] for row in c.fetchall()]

        if not author_ids or not journal_ids:
            print("Error: Author or Journal table is empty.")
            return

        combinations = [(author_id, journal_id) for author_id in author_ids for journal_id in journal_ids]
        if len(combinations) < count:
            print(f"Error: Not enough unique combinations. Maximum possible is {len(combinations)}.")
            return

        random.shuffle(combinations)
        unique_combinations = combinations[:count]

        c.executemany('INSERT INTO Author_Journal (author_id, journal_id) VALUES (%s, %s)', unique_combinations)
        self.conn.commit()

    def random_insert_author_research(self, count):
        c = self.conn.cursor()
        c.execute('SELECT author_id FROM Author')
        author_ids = [row[0] for row in c.fetchall()]
        c.execute('SELECT research_id FROM Research')
        research_ids = [row[0] for row in c.fetchall()]

        if not author_ids or not research_ids:
            print("Error: Author or Research table is empty.")
            return

        combinations = [(author_id, research_id) for author_id in author_ids for research_id in research_ids]
        if len(combinations) < count:
            print(f"Error: Not enough unique combinations. Maximum possible is {len(combinations)}.")
            return

        random.shuffle(combinations)
        unique_combinations = combinations[:count]

        c.executemany('INSERT INTO Research_Author (author_id, research_id) VALUES (%s, %s)', unique_combinations)
        self.conn.commit()

    def random_insert_publication(self, count):
        c = self.conn.cursor()
        c.execute('SELECT research_id FROM Research')
        research_ids = [row[0] for row in c.fetchall()]
        c.execute('SELECT journal_id FROM Journal')
        journal_ids = [row[0] for row in c.fetchall()]

        if not research_ids or not journal_ids:
            print("Error: Research or Journal table is empty.")
            return

        combinations = [(research_id, journal_id) for research_id in research_ids for journal_id in journal_ids]
        if len(combinations) < count:
            print(f"Error: Not enough unique combinations. Maximum possible is {len(combinations)}.")
            return

        random.shuffle(combinations)
        unique_combinations = combinations[:count]

        c.executemany('INSERT INTO Publication (research_id, journal_id, date) VALUES (%s, %s, CURRENT_DATE)',
                      unique_combinations)
        self.conn.commit()

    def search(self, journal_name_filter=None, issn_filter=None, year_established_filter=None,
                            research_title_filter=None, description_filter=None, author_firstname_filter=None,
                            author_surname_filter=None):
        query = '''
            SELECT 
                j.journal_name, 
                j.ISSN, 
                j.YearEstablished,
                r.title AS research_title, 
                r.description AS research_description, 
                a.firstname AS author_firstname, 
                a.surname AS author_surname
            FROM public.Journal j
            LEFT JOIN public.Publication p ON j.journal_id = p.journal_id
            LEFT JOIN public.Research r ON p.research_id = r.research_id
            LEFT JOIN public.Research_Author ra ON r.research_id = ra.research_id
            LEFT JOIN public.Author a ON ra.author_id = a.author_id
            WHERE
                (%s IS NULL OR j.journal_name ILIKE %s)
                AND (%s IS NULL OR j.ISSN = %s)
                AND (%s IS NULL OR j.YearEstablished = %s)
                AND (%s IS NULL OR r.title ILIKE %s)
                AND (%s IS NULL OR r.description ILIKE %s)
                AND (%s IS NULL OR a.firstname ILIKE %s)
                AND (%s IS NULL OR a.surname ILIKE %s);
        '''

        c = self.conn.cursor()
        c.execute(query, (
            journal_name_filter, journal_name_filter,
            issn_filter, issn_filter,
            year_established_filter, year_established_filter,
            research_title_filter, research_title_filter,
            description_filter, description_filter,
            author_firstname_filter, author_firstname_filter,
            author_surname_filter, author_surname_filter
        ))
        return c.fetchall()
