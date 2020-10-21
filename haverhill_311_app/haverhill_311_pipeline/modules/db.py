"""The database module is the interface to PostgreSQL db with 311 request data.
"""
import os
from typing import List, Optional

import boto3
import psycopg2 as psql
import psycopg2.extensions as psql_ext


def generate_db_auth_token(host: str, port: str, user: str, region: str):
    client = boto3.client('rds')
    token = client.generate_db_auth_token(
        DBHostname=host,
        Port=port,
        DBUsername=user,
        Region=region
    )
    return token


class QAlertDB:
    """QAlertDB class handles all database related operations.
    
        Example:

        with QAlertDB() as db:
            db.insert(record)
    """
    QALERT_TABLE = "qalert_requests"

    def __init__(self, host=None, port=None, user=None, password=None, region=None, database=None):
        self.host: str = host or os.environ['db_host']
        self.port: int = port or os.environ['db_port']
        self.user: str = user or os.environ['db_user']
        self.database: str = database or os.environ['db_database']
        self.password: Optional[str] = password or os.environ['db_password']
        self.region: Optional[str] = region or os.environ['db_region']

    def insert(self, record: dict):
        """Insert a QAlert request record into the qalert_requests table.
        
        Keyword arguments:
        record -- a QAlert request record to insert
        """
        columns = record.keys()
        values = [record[column] for column in columns]
        with self.conn.cursor() as cur:
            insert_statement = f'insert into {self.QALERT_TABLE} (%s) values %s'
            insert_statement = cur.mogrify(insert_statement, (psql_ext.AsIs(','.join(columns)), tuple(values)))
            cur.execute()

    def insert_many(self, records: List[dict]):
        """Insert multiple QAlert request records into the qalert_requests table.
        
        Keyword arguments:
        records -- a list of QAlert request record to insert
        """
        for record in records:
            self.insert(record=record)

    def get(self, record_id: str) -> Optional[tuple]:
        """Retreive a QAlert request record from qalert_requests table with given id.
        
        Keyword arguments:
        record_id -- id of the QAlert request record to retreive
        """
        select_statement = f'select * from {self.QALERT_TABLE} where id = {record_id};'
        with self.conn.cursor() as cur:
            cur.execute(select_statement)
            record = cur.fetchone()
        return record

    def _connect(self):
        """Establish connection with psql db."""
        if not self.password:
            self.password = generate_db_auth_token(
                host=self.host,
                port=self.port,
                user=self.user,
                region=self.region
            )
        self.conn = psql.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def _disconnect(self):
        """Kill connection with psql db."""
        self.conn.close()

    def __enter__(self):
        self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._disconnect()
