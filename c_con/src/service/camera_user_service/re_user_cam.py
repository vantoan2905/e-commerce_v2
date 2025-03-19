class ReUserCamera:
    def __init__(self, conn):
        """
        Initialize the ReUserCamera class with a database connection.
        
        Parameters:
            conn: A database connection object used to interact with the database.
        """
        self.conn = conn

    def _execute(
        self, query: str, params: tuple = (), fetchone: bool = False, commit: bool = False
    ) -> any:
        """
        Execute a SQL query using a context-managed cursor.

        Parameters:
            query (str): The SQL query to execute.
            params (tuple): Parameters for the query.
            fetchone (bool): If True, fetch and return only one record.
                             Otherwise, fetch all records.
            commit (bool): If True, commit the transaction and return the number of affected rows.
        
        Returns:
            If commit is False, returns a tuple (if fetchone=True) or a list of tuples (if fetchone=False).
            If commit is True, returns the number of affected rows.
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                if commit:
                    affected = cursor.rowcount
                else:
                    result = cursor.fetchone() if fetchone else cursor.fetchall()
            if commit:
                self.conn.commit()
                return affected
            else:
                return result
        except Exception as e:
            if commit:
                self.conn.rollback()
            raise e

    def get_all_user_cameras(self) -> list:
        """
        Retrieve all records from the user_camera table.

        Returns:
            list: A list of tuples, each representing a record in the user_camera table.
        """
        query = "SELECT * FROM user_camera"
        return self._execute(query)

    def get_user_camera_by_id(self, user_id: int, camera_id: int) -> tuple:
        """
        Retrieve a specific user_camera record based on user_id and camera_id.

        Parameters:
            user_id (int): The user's ID.
            camera_id (int): The camera's ID.

        Returns:
            tuple: A tuple representing the user_camera record, or None if not found.
        """
        query = "SELECT * FROM user_camera WHERE user_id = %s AND camera_id = %s"
        return self._execute(query, (user_id, camera_id), fetchone=True)

    def add_user_camera(self, user_id: int, camera_id: int, created_at) -> bool:
        """
        Insert a new record into the user_camera table.

        Parameters:
            user_id (int): The user's ID.
            camera_id (int): The camera's ID.
            created_at: The creation timestamp.
        
        Returns:
            bool: True if the insertion was successful (i.e. at least one row was affected), False otherwise.
        """
        query = "INSERT INTO user_camera (user_id, camera_id, created_at) VALUES (%s, %s, %s)"
        try:
            affected = self._execute(query, (user_id, camera_id, created_at), commit=True)
            return affected > 0
        except Exception as e:
            # Replace the print statement with proper logging if needed.
            print(f"Error adding user_camera: {e}")
            return False
