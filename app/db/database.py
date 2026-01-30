from dotenv import load_dotenv
import psycopg2
import sys
import os

from app.utils.logger import get_logger

logger = get_logger()

load_dotenv()

class Database:
    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        """
        Connect to database and return connection
        """
        logger.info("connecting to Database")
        try:
            load_dotenv()
            conn = psycopg2.connect(
                    host = os.getenv("POSTGRES_HOST"),
                    dbname = os.getenv("POSTGRES_DB"),
                    user = os.getenv("POSTGRES_USER"),
                    password = os.getenv("POSTGRES_PASSWORD"),
                    port = os.getenv("POSTGRES_PORT")
                )
            logger.info("connection success")
        except psycopg2.OperationalError as e:
            logger.error(f"Could not connect to Database: {e}")
            sys.exit(1)

        return conn
    

    def check_email_or_contact_exists(self, email: str, contact: str) -> bool:
        """
        Check if email or contact already exists
        """
        logger.info("Checking if email or contact exists")
        try:
            with self.conn.cursor() as cursor:
                query = """
                    SELECT 1
                FROM users
                WHERE email = %s OR contact = %s
                LIMIT 1
                """
                cursor.execute(query, (email, contact))
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Error checking email/contact existence: {e}")
            return True

        
    def insert_user_data(self, data: dict):
        """
        Insert new user into users table
        """
        logger.info("Inserting new user into database")
        try:
            with self.conn.cursor() as cursor:
                query = """
                    INSERT INTO users (email, contact, hashed_password, role_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """
                cursor.execute(
                    query,
                    (
                        data["email"],
                        data["contact"],
                        data["hashed_password"],
                        data["role_id"]
                    )
                )
                user_id = cursor.fetchone()[0]
                self.conn.commit()
                return user_id
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error inserting user data: {e}")
            return None

    def get_user_by_email(self, email: str):
        try:
            with self.conn.cursor() as cursor:
                query = """
                    SELECT id,hashed_password
                    FROM users
                    WHERE email = %s
                    LIMIT 1
                """
                cursor.execute(query, (email,))
                return cursor.fetchone()   
        except Exception as e:
            logger.error(f"Error fetching user by email: {e}")
            return None
        
    def list_all_companies(self):
        try:
            with self.conn.cursor() as cursor:
                query = """
                    SELECT company_name, company_type, industry
                    FROM companies
                """
                cursor.execute(query)

                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                return [dict(zip(columns, row)) for row in rows]

        except Exception as e:
            logger.error(f"Error fetching companies: {e}")
            return []

