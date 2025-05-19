"""
MatrixAnalyzer class for Task 5: Matrix operations.
Lab Work #4, Version 1.0, Developer: Alexander Svidinsky, Date: 2025-04-24

This module defines the MatrixAnalyzer class for matrix operations.
"""
import numpy as np
from abc import ABC, abstractmethod  # Добавляем импорт

class Analyzer(ABC):
    """Abstract base class for analyzers."""
    @abstractmethod
    def analyze(self):
        """Analyze the data.

        Returns:
            dict: Analysis results.
        """
        pass

class MatrixAnalyzer(Analyzer):
    """Class to analyze a matrix.

    Attributes:
        matrix (np.ndarray): Random matrix.
    """
    def __init__(self, n, m):
        """Initialize with random matrix.

        Args:
            n (int): Rows.
            m (int): Columns.
        """
        super().__init__()
        self.matrix = np.random.randint(0, 100, (n, m))

    def analyze(self):
        """Analyze the matrix.

        Returns:
            dict: Analysis results.
        """
        flat = self.matrix.flatten()
        return {
            'matrix': self.matrix,
            'mean': np.mean(flat),
            'sum': np.sum(flat)
        }

    def __str__(self):
        """String representation.

        Returns:
            str: String representation.
        """
        return f"MatrixAnalyzer with matrix of shape {self.matrix.shape}"