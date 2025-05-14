# ORM Practice
from sqlalchemy import create_engine, MetaData, Integer, Float, Column, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv
import os

# An ORM maps python classes to tables in a database
# Defining tables as classes

'''
Session Methods
    session.add(obj)  --> Adds a single object to the session
    session.add_all([objs]) --> Adds a list of objects to the session
    session.commit() --> Commit transaction
    session.delete(obj) --> Delete a specific object
    session.close() --> Close the session
    session.merge(obj) --> Merge a detached object back into the session
    session.get(Model, id) -->Fetch a single object by primary key (faster than query/filter).
'''
# Load secret
load_dotenv("secrets.env")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Create engine
engine = create_engine(
    f'postgresql+psycopg2://postgres:{POSTGRES_PASSWORD}@localhost:5432/sqltutorial',
    echo=False
)

Base = declarative_base()

#defining a table

class Person(Base):
    __tablename__ = 'people' # name of table
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

    things = relationship('Thing', back_populates='person')

class Thing(Base):
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    value = Column(Float)
    owner = Column(Integer, ForeignKey('people.id'))

    person = relationship('Person', back_populates='things')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Clear old data
session.query(Thing).delete()   # equivalent to --> conn.execute(things.delete())
session.query(Person).delete()  # equivalent to --> conn.execute(people.delete())
session.commit()    # equivalent to --> conn.commit()

new_person = Person(name='Sam', age=80)
session.add(new_person)
session.flush() # Temporary commit

new_thing = Thing(description='Camera', value=500, owner=new_person.id) # Dynamically gets the ID
session.add(new_thing)

session.commit()

print(new_person.things)
print(new_thing.person.name)

result = session.query(Person.name, Person.age).all() # returns all persons name and age in database in tuples

print(result)

results = session.query(Thing).filter(Thing.value > 10).all() # can use filter function like so

print(results)


# Joins
result_2 = session.query(Person.name, Thing.description).join(Thing).all()

print(result_2)

session.close()