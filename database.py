"""Save json data from data.json to MySQL database."""
import json
import mysql.connector
import config


def replace_apostrophe(query):
    """Replace apostrophe with double apostrophe."""
    return query.replace("'", "\'")


class Database:
    """Migrate data from json file to MySQL database."""

    def __init__(self, filename):
        self.filename = filename
        self.db, self.cursor = self.connect_db()
        self.data = self.read_json()
        self.create_table()
        try:
            self.save_data()
        except mysql.connector.errors.IntegrityError:
            print('Data already exists in database.')

    def read_json(self):
        """Read json file."""
        with open(self.filename, 'r') as f:
            return json.load(f)

    def connect_db(self):
        """Connect to MySQL database."""
        self.db = mysql.connector.connect(
            host=config.HOST,
            user=config.USER,
            passwd=config.PASSWORD,
            database=config.DATABASE
        )
        self.cursor = self.db.cursor()
        return self.db, self.cursor

    def create_table(self):
        """Create table in MySQL database."""
        # countries table
        with open('./SQL/create_table_countries.sql', 'r') as f:
            self.cursor.execute(f.read())
        # states table
        with open('./SQL/create_table_states.sql', 'r') as f:
            self.cursor.execute(f.read())
        # cities table
        with open('./SQL/create_table_cities.sql', 'r') as f:
            self.cursor.execute(f.read())
        self.db.commit()

    def save_data(self):
        """Save data to MySQL database."""

        for country in self.data:
            # insert country
            country_tuple = (
                country['id'],
                country['name'],
                country['iso3'],
                country['iso2'],
                country['numeric_code'],
                country['phone_code'],
                country['currency'],
                country['currency_name'],
                country['currency_symbol'],
                country['tld'],
                country['capital'],
                country['region'],
                country['subregion'],
                country['native'],
                country['latitude'],
                country['longitude'],
                country['emoji'],
                country['emojiU']
            )
            query = '''
                INSERT 
                    INTO 
                        cities_db.countries(
                            id,
                            country_name, 
                            iso3, 
                            iso2, 
                            numeric_code, 
                            phone_code, 
                            currency_code, 
                            currency_name, 
                            currency_symbol, 
                            tld, 
                            capital, 
                            region, 
                            subregion, 
                            native_name, 
                            latitude, 
                            longitude, 
                            emoji, 
                            emojiU
                        )
                        VALUES (
                        %d, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"
                     )
            ''' % country_tuple
            # replace apostrophe with double apostrophe
            query = replace_apostrophe(query)
            self.cursor.execute(query)
            country_id = self.cursor.lastrowid
            # insert state
            for state in country['states']:
                state_tuple = (
                    state['id'],
                    country['id'],
                    state['name'],
                    state['state_code'],
                    state['latitude'],
                    state['longitude']
                )
                query = '''
                    INSERT 
                        INTO 
                            cities_db.states(
                                id,
                                country_id,
                                state_name,
                                state_code,
                                latitude,
                                longitude)
                        VALUES (
                            %d, %d, "%s", "%s", "%s", "%s"
                        )
                    ''' % state_tuple
                # replace apostrophe with double apostrophe
                query = replace_apostrophe(query)
                self.cursor.execute(query)
                state_id = self.cursor.lastrowid
                # insert city
                for city in state['cities']:
                    city_tuple = (
                        city['id'],
                        city['name'],
                        country['id'],
                        state['id'],
                        city['latitude'],
                        city['longitude']
                    )
                    query = '''
                        INSERT 
                            INTO 
                            cities_db.cities(
                                id,
                                city_name, 
                                country_id, 
                                state_id, 
                                latitude, 
                                longitude
                            ) 
                            VALUES (
                                %d, "%s", %d, %d, "%s", "%s"
                            )
                        ''' % city_tuple
                    # replace apostrophe with double apostrophe
                    query = replace_apostrophe(query)
                    self.cursor.execute(query)
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def get_country_data(self):
        """Get country data from MySQL database."""
        self.cursor.execute('''
            SELECT * FROM cities_db.countries
        ''')
        return self.cursor.fetchall()

    def get_state_data(self, country_id):
        """Get state data from MySQL database."""
        country_id = int(country_id)
        query = '''
            SELECT * FROM cities_db.states WHERE country_id = %d
        ''' % country_id
        print(query)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_city_data(self, state_id):
        """Get city data from MySQL database."""
        state_id = int(state_id)
        query = '''
            SELECT * FROM cities_db.cities WHERE state_id = %d
        ''' % state_id
        self.cursor.execute(query)
        return self.cursor.fetchall()
