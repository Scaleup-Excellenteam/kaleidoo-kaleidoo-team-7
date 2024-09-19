import DatabaseManager

class DatabaseManagerSingelton:
    _instance = None

    @staticmethod
    def get_instance():
        """
        Returns the single instance of the Database class.
        If no instance exists, it creates one.
        """
        if DatabaseManagerSingelton._instance is None:
            DatabaseManagerSingelton._instance = DatabaseManager.DatabaseManager(db_path='application_data.db')
        return DatabaseManagerSingelton._instance

    @staticmethod
    def close_instance():
        """
        Closes the instance of TextProcessor if it exists.
        """
        if DatabaseManagerSingelton._instance is not None:
            DatabaseManagerSingelton._instance.close()
            DatabaseManagerSingelton._instance = None
