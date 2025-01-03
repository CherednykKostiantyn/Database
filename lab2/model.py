from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
import random
from datetime import datetime

Base = declarative_base()

class Journal(Base):
    __tablename__ = 'journal'

    journal_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, name="journal_name")
    issn = Column(String, nullable=False, name="ISSN")
    year_established = Column(Integer, nullable=False, name="YearEstablished")

    author_journals = relationship('AuthorJournal', back_populates='journal')
    publications = relationship('Publication', back_populates='journal')

class Research(Base):
    __tablename__ = 'research'

    research_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, name="title")
    description = Column(Text, nullable=False, name="description")
    date = Column(Date, nullable=False, name="date")

    research_authors = relationship('ResearchAuthor', back_populates='research')
    publications = relationship('Publication', back_populates='research')

class Author(Base):
    __tablename__ = 'author'

    author_id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False, name="firstname")
    surname = Column(String, nullable=False, name="surname")
    email = Column(String, nullable=False, name="email")

    author_journals = relationship('AuthorJournal', back_populates='author')
    research_authors = relationship('ResearchAuthor', back_populates='author')

class AuthorJournal(Base):
    __tablename__ = 'author_journal'

    author_journal_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('author.author_id'), nullable=False,)
    journal_id = Column(Integer, ForeignKey('journal.journal_id'), nullable=False)

    author = relationship('Author', back_populates='author_journals')
    journal = relationship('Journal', back_populates='author_journals')

class ResearchAuthor(Base):
    __tablename__ = 'research_author'

    research_author_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('author.author_id'), nullable=False)
    research_id = Column(Integer, ForeignKey('research.research_id'), nullable=False)

    author = relationship('Author', back_populates='research_authors')
    research = relationship('Research', back_populates='research_authors')

class Publication(Base):
    __tablename__ = 'publication'

    publication_id = Column(Integer, primary_key=True)
    research_id = Column(Integer, ForeignKey('research.research_id'), nullable=False)
    journal_id = Column(Integer, ForeignKey('journal.journal_id'), nullable=False)
    date = Column(Date, default=func.current_date())

    research = relationship('Research', back_populates='publications')
    journal = relationship('Journal', back_populates='publications')

class Model:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:1111@localhost:5432/postgres')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_journal(self, journal_name, ISSN, YearEstablished):
        journal = Journal(name=journal_name, issn=ISSN, year_established=YearEstablished)
        self.session.add(journal)
        self.session.commit()

    def add_research(self, title, description, date):
        research = Research(title=title, description=description, date=date)
        self.session.add(research)
        self.session.commit()

    def add_author(self, firstname, surname, email):
        author = Author(firstname=firstname, surname=surname, email=email)
        self.session.add(author)
        self.session.commit()

    def add_author_journal(self, author_id, journal_id):
        author = self.session.query(Author).filter_by(author_id=author_id).first()
        journal = self.session.query(Journal).filter_by(journal_id=journal_id).first()
        if author and journal:
            author_journal = AuthorJournal(author=author, journal=journal)
            self.session.add(author_journal)
            self.session.commit()
        else:
            print("Error: Author or Journal not found.")

    def add_research_author(self, author_id, research_id):
        author = self.session.query(Author).filter_by(author_id=author_id).first()
        research = self.session.query(Research).filter_by(research_id=research_id).first()
        if author and research:
            research_author = ResearchAuthor(author=author, research=research)
            self.session.add(research_author)
            self.session.commit()
        else:
            print("Error: Author or Research not found.")

    def add_publication(self, research_id, journal_id, publication_date):
        research = self.session.query(Research).filter_by(research_id=research_id).first()
        journal = self.session.query(Journal).filter_by(journal_id=journal_id).first()

        if research and journal:
            publication = Publication(research_id=research_id, journal_id=journal_id, date=publication_date)
            self.session.add(publication)
            self.session.commit()
        else:
            print("Error: Research or Journal not found.")

    def update_journal(self, journal_id, journal_name, ISSN, YearEstablished):
        journal = self.session.query(Journal).filter_by(journal_id=journal_id).first()
        if journal:
            journal.name = journal_name
            journal.issn = ISSN
            journal.year_established = YearEstablished
            self.session.commit()
            print(f"Journal with ID {journal_id} updated successfully.")
        else:
            print(f"Journal with ID {journal_id} not found.")

    def update_research(self, research_id, title, description, date):
        research = self.session.query(Research).filter_by(research_id=research_id).first()

        if research:
            research.title = title
            research.description = description
            research.date = date
            self.session.commit()
            print(f"Research with ID {research_id} updated successfully.")
        else:
            print(f"Research with ID {research_id} not found.")

    def update_author(self, author_id, firstname, surname, email):
        author = self.session.query(Author).filter_by(author_id=author_id).first()

        if author:
            author.firstname = firstname
            author.surname = surname
            author.email = email
            self.session.commit()
            print(f"Author with ID {author_id} updated successfully.")
        else:
            print(f"Author with ID {author_id} not found.")

    def update_author_journal(self, old_author_id, old_journal_id, new_author_id, new_journal_id):
        author_journal = self.session.query(AuthorJournal).filter_by(
            author_id=old_author_id, journal_id=old_journal_id
        ).first()

        if author_journal:
            new_author = self.session.query(Author).filter_by(author_id=new_author_id).first()
            new_journal = self.session.query(Journal).filter_by(journal_id=new_journal_id).first()

            if new_author and new_journal:
                author_journal.author_id = new_author_id
                author_journal.journal_id = new_journal_id
                self.session.commit()
                print("AuthorJournal entry updated successfully.")
            else:
                print("Error: New author or journal not found.")
        else:
            print("Error: AuthorJournal entry not found.")

    def update_author_research(self, old_author_id, old_research_id, new_author_id, new_research_id):
        research_author = self.session.query(ResearchAuthor).filter_by(
            author_id=old_author_id, research_id=old_research_id
        ).first()

        if research_author:
            new_author = self.session.query(Author).filter_by(author_id=new_author_id).first()
            new_research = self.session.query(Research).filter_by(research_id=new_research_id).first()

            if new_author and new_research:
                research_author.author_id = new_author_id
                research_author.research_id = new_research_id
                self.session.commit()
                print("ResearchAuthor entry updated successfully.")
            else:
                print("Error: New author or research not found.")
        else:
            print("Error: ResearchAuthor entry not found.")

    def update_publication(self, old_research_id, old_journal_id, new_research_id, new_journal_id, new_date):
        publication = self.session.query(Publication).filter_by(
            research_id=old_research_id, journal_id=old_journal_id
        ).first()

        if publication:
            new_research = self.session.query(Research).filter_by(research_id=new_research_id).first()
            new_journal = self.session.query(Journal).filter_by(journal_id=new_journal_id).first()

            if new_research and new_journal:
                publication.research_id = new_research_id
                publication.journal_id = new_journal_id
                publication.date = new_date
                self.session.commit()
                print("Publication entry updated successfully.")
            else:
                print("Error: New research or journal not found.")
        else:
            print("Error: Publication entry not found.")

    def delete_journal(self, journal_id):
        journal = self.session.query(Journal).filter_by(journal_id=journal_id).first()
        if journal:
            self.session.delete(journal)
            self.session.commit()
            print(f"Journal with ID {journal_id} deleted successfully.")
        else:
            print(f"Journal with ID {journal_id} not found.")

    def delete_research(self, research_id):
        publication = self.session.query(Publication).filter_by(research_id=research_id).first()
        if publication:
            print(f"Research with ID {research_id} is associated with a publication and cannot be deleted.")
            return
        research = self.session.query(Research).filter_by(research_id=research_id).first()
        if research:
            self.session.delete(research)
            self.session.commit()
            print(f"Research with ID {research_id} deleted successfully.")
        else:
            print(f"Research with ID {research_id} not found.")

    def delete_author(self, author_id):
        author_journal = self.session.query(AuthorJournal).filter_by(author_id=author_id).first()
        if author_journal:
            print(f"Author with ID {author_id} is associated with journals and cannot be deleted.")
            return
        research_author = self.session.query(ResearchAuthor).filter_by(author_id=author_id).first()
        if research_author:
            print(f"Author with ID {author_id} is associated with research and cannot be deleted.")
            return
        author = self.session.query(Author).filter_by(author_id=author_id).first()
        if author:
            self.session.delete(author)
            self.session.commit()
            print(f"Author with ID {author_id} deleted successfully.")
        else:
            print(f"Author with ID {author_id} not found.")

    def delete_author_journal(self, author_journal_id):
        author_journal = self.session.query(AuthorJournal).filter_by(author_journal_id=author_journal_id).first()
        if author_journal:
            self.session.delete(author_journal)
            self.session.commit()
            print(f"AuthorJournal entry with ID {author_journal_id} deleted successfully.")
        else:
            print(f"AuthorJournal entry with ID {author_journal_id} not found.")

    def delete_research_author(self, research_author_id):
        research_author = self.session.query(ResearchAuthor).filter_by(research_author_id=research_author_id).first()
        if research_author:
            self.session.delete(research_author)
            self.session.commit()
            print(f"ResearchAuthor entry with ID {research_author_id} deleted successfully.")
        else:
            print(f"ResearchAuthor entry with ID {research_author_id} not found.")

    def delete_publication(self, publication_id):
        publication = self.session.query(Publication).filter_by(publication_id=publication_id).first()
        if publication:
            self.session.delete(publication)
            self.session.commit()
            print(f"Publication with ID {publication_id} deleted successfully.")
        else:
            print(f"Publication with ID {publication_id} not found.")

    def view_table(self, choice_table):
        table_mapping = {
            1: Journal,
            2: Research,
            3: Author,
            4: AuthorJournal,
            5: ResearchAuthor,
            6: Publication
        }

        model_class = table_mapping.get(choice_table)
        if not model_class:
            print("Invalid table choice.")
            return []

        try:
            results = self.session.query(model_class).all()

            if choice_table == 1:
                return [(obj.journal_id, obj.journal_name, obj.ISSN, obj.YearEstablished) for obj in results]
            elif choice_table == 2:
                return [(obj.research_id, obj.title, obj.description, obj.date) for obj in results]
            elif choice_table == 3:
                return [(obj.author_id, obj.firstname, obj.surname, obj.email) for obj in results]
            elif choice_table == 4:
                return [(obj.author_journal_id, obj.author_id, obj.journal_id) for obj in results]
            elif choice_table == 5:
                return [(obj.research_author_id, obj.research_id, obj.author_id) for obj in results]
            elif choice_table == 6:  
                return [(obj.publication_id, obj.research_id, obj.journal_id, obj.date) for obj in results]

        except Exception as e:
            print(f"An error occurred while fetching data: {e}")
            return []

    def random_insert_journal(self, count):
        journals = [
            Journal(
                name=f"Journal {random.randint(1, 100000)}",
                issn=f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                year_established=random.randint(1900, 2024)
            ) for _ in range(count)
        ]
        self.session.add_all(journals)
        self.session.commit()

    def random_insert_research(self, count):
        researches = [
            Research(
                title=f"Research {random.randint(1, 100000)}",
                description=f"Description of research {random.randint(1, 100000)}",
                date=datetime.strptime(f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}", "%Y-%m-%d")
            ) for _ in range(count)
        ]
        self.session.add_all(researches)
        self.session.commit()

    def random_insert_author(self, count):
        authors = [
            Author(
                firstname=f"Firstname{random.randint(1, 100000)}",
                surname=f"Surname{random.randint(1, 100000)}",
                email=f"email{random.randint(1, 100000)}@gmail.com"
            ) for _ in range(count)
        ]
        self.session.add_all(authors)
        self.session.commit()

    def random_insert_author_journal(self, count):
        authors = self.session.query(Author).all()
        journals = self.session.query(Journal).all()

        if not authors or not journals:
            print("Error: Author or Journal table is empty.")
            return

        combinations = [
            (random.choice(authors), random.choice(journals)) for _ in range(count)
        ]
        author_journals = [
            AuthorJournal(
                author=author,
                journal=journal
            ) for author, journal in combinations
        ]
        self.session.add_all(author_journals)
        self.session.commit()

    def random_insert_author_research(self, count):
        authors = self.session.query(Author).all()
        researches = self.session.query(Research).all()

        if not authors or not researches:
            print("Error: Author or Research table is empty.")
            return

        combinations = [
            (random.choice(authors), random.choice(researches)) for _ in range(count)
        ]
        research_authors = [
            ResearchAuthor(
                author=author,
                research=research
            ) for author, research in combinations
        ]
        self.session.add_all(research_authors)
        self.session.commit()

    def random_insert_publication(self, count):
        researches = self.session.query(Research).all()
        journals = self.session.query(Journal).all()

        if not researches or not journals:
            print("Error: Research or Journal table is empty.")
            return

        combinations = [
            (random.choice(researches), random.choice(journals)) for _ in range(count)
        ]
        publications = [
            Publication(
                research=research,
                journal=journal
            ) for research, journal in combinations
        ]
        self.session.add_all(publications)
        self.session.commit()

    def search(self, journal_name_filter=None, issn_filter=None, year_established_filter=None,
               research_title_filter=None, description_filter=None, author_firstname_filter=None,
               author_surname_filter=None):
        query = self.session.query(
            Journal.name.label('journal_name'),
            Journal.issn,
            Journal.year_established,
            Research.title.label('research_title'),
            Research.description.label('research_description'),
            Author.firstname.label('author_firstname'),
            Author.surname.label('author_surname')
        ).join(Publication, Journal.journal_id == Publication.journal_id, isouter=True) \
         .join(Research, Publication.research_id == Research.research_id, isouter=True) \
         .join(ResearchAuthor, Research.research_id == ResearchAuthor.research_id, isouter=True) \
         .join(Author, ResearchAuthor.author_id == Author.author_id, isouter=True)

        if journal_name_filter:
            query = query.filter(Journal.name.ilike(f"%{journal_name_filter}%"))
        if issn_filter:
            query = query.filter(Journal.issn == issn_filter)
        if year_established_filter:
            query = query.filter(Journal.year_established == year_established_filter)
        if research_title_filter:
            query = query.filter(Research.title.ilike(f"%{research_title_filter}%"))
        if description_filter:
            query = query.filter(Research.description.ilike(f"%{description_filter}%"))
        if author_firstname_filter:
            query = query.filter(Author.firstname.ilike(f"%{author_firstname_filter}%"))
        if author_surname_filter:
            query = query.filter(Author.surname.ilike(f"%{author_surname_filter}%"))

        results = query.all()
        return results