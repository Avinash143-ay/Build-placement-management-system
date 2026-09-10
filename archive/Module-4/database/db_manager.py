import os
import pickle
from typing import Dict, Optional, List, Any
from pathlib import Path
from table import Table

class Database:
    def __init__(self, name: str, persist_dir: str = 'db_persistence'):
        """
        Initialize a database with automatic loading of persisted tables.
        
        Args:
            name: Name of the database
            persist_dir: Directory to store table data (default: 'db_persistence')
        """
        self.name = name
        self.persist_dir = Path(persist_dir)
        self.tables: Dict[str, Table] = {}
        
        # Ensure persistence directory exists
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing tables automatically
        self.load_tables()
    
    def create_table(self, name: str, columns: Dict[str, type], primary_key: str, 
                    use_bplustree: bool = True, overwrite: bool = False) -> Table:
        """
        Create a new table with schema validation.
        
        Args:
            name: Table name
            columns: Dictionary of column names and types
            primary_key: Name of primary key column
            use_bplustree: Whether to use B+Tree indexing (default: True)
            overwrite: Whether to overwrite existing table (default: False)
            
        Returns:
            The created Table object
        """
        if not name.isidentifier():
            raise ValueError("Table name must be a valid Python identifier")
            
        if primary_key not in columns:
            raise ValueError(f"Primary key '{primary_key}' not in columns")
            
        if name in self.tables and not overwrite:
            raise ValueError(f"Table '{name}' already exists. Use overwrite=True to replace it.")
            
        if name in self.tables:
            self.delete_table(name)  # Clean up existing table
            
        table = Table(name, columns, primary_key, use_bplustree)
        self.tables[name] = table
        return table

    
    def delete_table(self, name: str) -> bool:
        """
        Delete a table and its persisted data.
        
        Args:
            name: Name of table to delete
            
        Returns:
            True if table was deleted, False if it didn't exist
        """
        if name not in self.tables:
            return False
            
        # Remove from memory
        del self.tables[name]
        
        # Remove persisted file
        table_file = self.persist_dir / f'{name}.pkl'
        try:
            if table_file.exists():
                table_file.unlink()
            return True
        except OSError as e:
            print(f"Error deleting table file for '{name}': {e}")
            return False
    
    def get_table(self, name: str) -> Optional[Table]:
        """Get a table by name if it exists"""
        return self.tables.get(name)
    
    def list_tables(self) -> List[str]:
        """List all table names in the database"""
        return list(self.tables.keys())
    
    def persist(self) -> None:
        """Persist all tables to disk with error handling"""
        for table in self.tables.values():
            try:
                table.persist(self.persist_dir)
            except Exception as e:
                print(f"Error persisting table '{table.name}': {e}")
                raise
    
    def load_tables(self) -> None:
        """Load all tables from disk with error handling"""
        try:
            for table_file in self.persist_dir.glob('*.pkl'):
                table_name = table_file.stem  # Get filename without extension
                if table_name not in self.tables:  # Don't overwrite in-memory tables
                    try:
                        table = Table.load(self.persist_dir, table_name)
                        self.tables[table_name] = table
                    except Exception as e:
                        print(f"Error loading table '{table_name}': {e}")
        except Exception as e:
            print(f"Error loading tables: {e}")

    def __enter__(self):
        """Support for context manager (with statement)"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Persist changes when exiting context"""
        self.persist()





        
        # All changes automatically persisted when exiting 'with' block
