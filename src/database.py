import sqlite3
from typing import List, Tuple
from logger import logger

class Database:
    def __init__(self, db_name: str = 'game_history.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_rounds (
                _sk INTEGER PRIMARY KEY AUTOINCREMENT,
                character_name TEXT,
                model_name TEXT,
                questions_asked_count INTEGER,
                did_succeeded_indicator BOOLEAN
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history (
                _sk INTEGER PRIMARY KEY AUTOINCREMENT,
                game_round_sk INTEGER,
                question_number INTEGER,
                question_text TEXT,
                answer_text TEXT,
                FOREIGN KEY (game_round_sk) REFERENCES game_rounds (_sk)
            )
        ''')
        self.conn.commit()

    def insert_game_round(self, character_name: str, model_name: str) -> int:
        self.cursor.execute('''
            INSERT INTO game_rounds (character_name, model_name)
            VALUES (?, ?)
        ''', (character_name, model_name))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_game_round(self, round_sk: int, questions_asked_count: int, did_succeeded_indicator: bool):
        self.cursor.execute('''
            UPDATE game_rounds
            SET questions_asked_count = ?, did_succeeded_indicator = ?
            WHERE _sk = ?
        ''', (questions_asked_count, did_succeeded_indicator, round_sk))
        self.conn.commit()

    def insert_conversation_history(self, game_round_sk: int, history: List[Tuple[int, str, str]]):
        self.cursor.executemany('''
            INSERT INTO conversation_history (game_round_sk, question_number, question_text, answer_text)
            VALUES (?, ?, ?, ?)
        ''', [(game_round_sk, qnum, q, a) for qnum, q, a in history])
        self.conn.commit()

    def close(self):
        self.conn.close()

    def remove_game_round(self, round_sk: int):
        try:
            # First, delete related conversation history
            self.cursor.execute('''
                DELETE FROM conversation_history
                WHERE game_round_sk = ?
            ''', (round_sk,))

            # Then, delete the game round
            self.cursor.execute('''
                DELETE FROM game_rounds
                WHERE _sk = ?
            ''', (round_sk,))

            self.conn.commit()
            logger.info(f"Successfully removed game round with _sk: {round_sk} and its related conversation history.")
        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Error removing game round with _sk: {round_sk}. Error: {e}")
