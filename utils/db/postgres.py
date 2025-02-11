from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                result = None

                if fetch or fetchval or fetchrow or execute:
                    if fetch:
                        result = await connection.fetch(command, *args)
                    elif fetchval:
                        result = await connection.fetchval(command, *args)
                    elif fetchrow:
                        result = await connection.fetchrow(command, *args)
                    elif execute:
                        result = await connection.execute(command, *args)
                else:
                    raise ValueError("No valid action was taken for the query")

                return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY UNIQUE,
        full_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NULL,
        is_premium BOOLEAN NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        )
        """
        await self.execute(sql, execute=True)

    async def create_table_expense(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Expenses (
        id SERIAL PRIMARY KEY UNIQUE,
        amount NUMERIC(15, 3) NOT NULL,
        reason VARCHAR(255) NULL,
        date TIMESTAMP NOT NULL,
        user_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    # New table for Incomes
    async def create_table_income(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Incomes (
        id SERIAL PRIMARY KEY UNIQUE,
        amount NUMERIC(15, 3) NOT NULL,
        reason VARCHAR(255) NULL,
        date TIMESTAMP NOT NULL,
        user_id BIGINT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def add_user(self, full_name, username, telegram_id, is_premium=False):
        sql = "INSERT INTO users (full_name, username, telegram_id, is_premium) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(
            sql, full_name, username, telegram_id, is_premium, fetchrow=True
        )

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

    # Methods for Expenses
    async def add_expense(self, amount, reason, date, user_id):
        sql = "INSERT INTO Expenses (amount, reason, date, user_id) VALUES($1, $2, $3, $4) returning *"
        await self.execute(sql, amount, reason, date, user_id, fetchrow=True)

    async def select_all_expenses(self, user_id):
        sql = "SELECT SUM(amount) FROM Expenses WHERE user_id = $1"
        return await self.execute(sql, user_id, fetchval=True)

    async def select_all_expenses_file(self, user_id):
        sql = "SELECT * FROM Expenses WHERE user_id = $1"
        return await self.execute(sql, user_id, fetch=True)

    # Methods for Incomes
    async def add_income(self, amount, reason, date, user_id):
        sql = "INSERT INTO Incomes (amount, reason, date, user_id) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, amount, reason, date, user_id, fetchrow=True)

    async def select_all_incomes(self, user_id):
        sql = "SELECT SUM(amount) FROM Incomes WHERE user_id = $1"
        return await self.execute(sql, user_id, fetchval=True)

    async def select_all_incomes_file(self, user_id):
        sql = "SELECT * FROM Incomes WHERE user_id = $1"
        return await self.execute(sql, user_id, fetch=True)

    async def get_category_stats(self, user_id):
        sql = """
        SELECT reason, SUM(amount) as total 
        FROM expenses 
        WHERE user_id = $1
        GROUP BY reason 
        ORDER BY total DESC
        """
        return await self.execute(sql, user_id, fetch=True)

    async def get_general_stat(self, user_id):
        sql = """
        SELECT 
        (COALESCE((SELECT SUM(amount) FROM Incomes WHERE user_id = $1), 0) - 
        COALESCE((SELECT SUM(amount) FROM Expenses WHERE user_id = $1), 0)) 
        AS general_balance;
        """
        return await self.execute(sql, user_id, fetch=True)
