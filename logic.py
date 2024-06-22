from config import DATABASE

class DB_Manager:
    def __init__(self):
        self.cursor = DATABASE.cursor()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY,
            project_name TEXT NOT NULL,
            project_disc TEXT,
            project_link TEXT,
            status_id INTEGER,
            FOREIGN KEY (status_id) REFERENCES status(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY,
            skillname TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_skills (
            project_id INTEGER,
            skills_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(project_id),
            FOREIGN KEY (skills_id) REFERENCES skills(id)
        )
        """)

        DATABASE.commit()

    def insert_data(self, table, cols, data):
        col_names = ', '.join(cols)
        placeholders = ', '.join(['?' for _ in cols])
        sql = f'INSERT INTO {table} ({col_names}) VALUES ({placeholders})'
        self.default_sql(sql, data)

    def delete_data(self, table, col, data):
        sql = f'DELETE FROM {table} WHERE {col} = ?'
        self.default_sql(sql, (data,))

    def update_data(self, table, col, new_val, data):
        sql = f"UPDATE {table} SET {col} = ? WHERE {data[0]} = ?"
        self.default_sql(sql, (new_val, data[1]))

    def select_data(self, table, data):
        sql = f"SELECT * FROM {table} WHERE {data[0]} = ?"
        self.default_sql(sql, (data[1],))

    def default_sql(self, sql, data=()):
        self.cursor.execute(sql, data)
        DATABASE.commit()

if __name__ == '__main__':
    manager = DB_Manager()
    manager.create_tables()
    manager.insert_data('skills', ('skillname',), ('1111',))
