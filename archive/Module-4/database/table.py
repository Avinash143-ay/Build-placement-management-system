import os
import pickle
from typing import Dict, List, Tuple, Any, Optional
from bplustree import BPlusTree
from bruteforce import BruteForceIndex

class Table:
    def __init__(self, name: str, columns: Dict[str, type], primary_key: str, use_bplustree: bool = True):
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        self.use_bplustree = use_bplustree
        
        if use_bplustree:
            self.index = BPlusTree(order=4)  # Adjust order as needed
        else:
            self.index = BruteForceIndex()
        
        self.data = []
        self.column_order = list(columns.keys())
    
    def insert(self, record: Dict[str, Any]) -> bool:
        """Insert a record into the table"""
       # Validate keys
        if set(record.keys()) != set(self.columns.keys()):
           raise ValueError(f"Record doesn't match table schema. Expected keys: {set(self.columns.keys())}, got: {set(record.keys())}")
    
    # Validate data types
        for col, value in record.items():
            expected_type = self.columns[col]
            if not isinstance(value, expected_type):
                raise TypeError(f"Column '{col}' expects type {expected_type.__name__}, got {type(value).__name__}")
    
        pk_value = record[self.primary_key]
        found, _ = self.index.search(pk_value)
        if found:
           return False  # Primary key must be unique
    
        self.data.append(record)
        self.index.insert(pk_value, len(self.data) - 1)
        return True

    def show(self, limit: int = 10) -> None:
         """Display table contents in a readable format"""
        # Get column headers
         headers = list(self.columns.keys())
    
    # Get rows (only non-deleted records)
         rows = [record for record in self.data if record is not None]
    
    # Print table header
         print(f"\nTable: {self.name}")
         print("-" * 50)
    
    # Print column headers
         header_row = "| " + " | ".join(f"{col:15}" for col in headers) + " |"
         print(header_row)
         print("-" * len(header_row))
    
    # Print rows (limited by 'limit' parameter)
         for record in rows[:limit]:
             row = "| " + " | ".join(f"{str(record.get(col, '')):15}" for col in headers) + " |"
             print(row)
    
    # Show count
         print(f"\nShowing {min(limit, len(rows))} of {len(rows)} records")
    def select(self, pk_value: Any) -> Optional[Dict[str, Any]]:
        """Select a record by primary key"""
        found, idx = self.index.search(pk_value)
        if found:
            return self.data[idx]
        return None
    
    def select_range(self, start_pk: Any, end_pk: Any) -> List[Dict[str, Any]]:
        """Select records in a primary key range"""
        results = []
        for pk, idx in self.index.range_query(start_pk, end_pk):
            results.append(self.data[idx])
        return results
    
    def update(self, pk_value: Any, updates: Dict[str, Any]) -> bool:
        """Update a record"""
        found, idx = self.index.search(pk_value)
        if not found:
            return False
        
        # Validate updates
        for col, value in updates.items():
            if col not in self.columns:
                raise ValueError(f"Column {col} doesn't exist")
            if not isinstance(value, self.columns[col]):
                raise TypeError(f"Column {col} expects type {self.columns[col]}, got {type(value)}")
        
        # If updating primary key, need to update index
        if self.primary_key in updates:
            new_pk = updates[self.primary_key]
            # Check if new primary key already exists
            found_existing, _ = self.index.search(new_pk)
            if found_existing:
                return False
            
            # Remove old key and insert new one
            self.index.delete(pk_value)
            self.index.insert(new_pk, idx)
        
        # Apply updates
        for col, value in updates.items():
            self.data[idx][col] = value
        
        return True
    
    def delete(self, pk_value: Any) -> bool:
        """Delete a record"""
        found, idx = self.index.search(pk_value)
        if not found:
            return False
        
        # Mark record as deleted (lazy deletion)
        self.data[idx] = None
        self.index.delete(pk_value)
        return True
    
    def aggregate(self, column: str, operation: str) -> Optional[Any]:
        """Aggregate function (sum, avg, min, max, count)"""
        if column not in self.columns:
            raise ValueError(f"Column {column} doesn't exist")
        
        values = []
        for record in self.data:
            if record is not None:  # Skip deleted records
                values.append(record[column])
        
        if not values:
            return None
        
        if operation == 'sum':
            return sum(values)
        elif operation == 'avg':
            return sum(values) / len(values)
        elif operation == 'min':
            return min(values)
        elif operation == 'max':
            return max(values)
        elif operation == 'count':
            return len(values)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
    
    def persist(self, directory: str) -> None:
        """Persist table to disk"""
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        data = {
            'name': self.name,
            'columns': self.columns,
            'primary_key': self.primary_key,
            'use_bplustree': self.use_bplustree,
            'data': self.data
        }
        
        with open(os.path.join(directory, f'{self.name}.pkl'), 'wb') as f:
            pickle.dump(data, f)
    
    @classmethod
    def load(cls, directory: str, name: str) -> 'Table':
        """Load table from disk"""
        filepath = os.path.join(directory, f'{name}.pkl')
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Table {name} not found")
        
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        table = cls(data['name'], data['columns'], data['primary_key'], data['use_bplustree'])
        table.data = data['data']
        
        # Rebuild index
        for idx, record in enumerate(table.data):
            if record is not None:  # Skip deleted records
                table.index.insert(record[table.primary_key], idx)
        
        return table