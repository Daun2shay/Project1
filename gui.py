import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from typing import Callable
# Used AI to help with the GUI
class VotingApp(QMainWindow):
    """
    A PyQt6 GUI application for the voting system.
    Allows users to enter their ID and vote for a candidate.
    """

    def __init__(self, votingSystem) -> None:
        """
        Initialize the voting GUI application.
        
        Args:
            votingSystem: An instance of VotingSystem to handle vote logic
        """
        super().__init__()
        self.votingSystem = votingSystem
        self.setWindowTitle("Vote")
        self.setFixedSize(350, 250)
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        # ID input
        idLabel = QLabel("Enter your ID (1-100):")
        layout.addWidget(idLabel)
        
        self.idInput = QLineEdit()
        self.idInput.setPlaceholderText("Enter ID number")
        layout.addWidget(self.idInput)
        
        for name in ["John", "Jane"]:
            btn = QPushButton(f"Vote for {name}")
            btn.clicked.connect(self.createVoteHandler(name))
            layout.addWidget(btn)
    
    def createVoteHandler(self, candidate: str) -> Callable[[], None]:
        """
        Create a vote handler function for a specific candidate.
        
        Args:
            candidate: The name of the candidate
            
        Returns:
            A callable function that votes for the candidate
        """
        def handler() -> None:
            self.vote(candidate)
        return handler
    
    def vote(self, candidate: str) -> None:
        """
        Process a vote for the specified candidate.
        Validates voter ID and displays appropriate messages.
        
        Args:
            candidate: The name of the candidate to vote for
        """
        # Get voter ID from input
        idText = self.idInput.text().strip()
        
        if not idText:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setWindowTitle("Error")
            msgBox.setText("Please enter your ID")
            msgBox.setStyleSheet("QLabel{color: red;}")
            msgBox.exec()
            return
        
        try:
            voterId = int(idText)
        except ValueError:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setWindowTitle("Error")
            msgBox.setText("ID must be a number")
            msgBox.setStyleSheet("QLabel{color: red;}")
            msgBox.exec()
            return
        
        # Try to cast vote
        try:
            self.votingSystem.castVote(voterId, candidate)
            
            # Clear input and show success
            self.idInput.clear()
            
            # Show success message with red text
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("Success")
            msgBox.setText(f"Vote recorded for {candidate}!")
            msgBox.setStyleSheet("QLabel{color: red;}")
            msgBox.exec()
            
        except ValueError as e:
            msgBox = QMessageBox(self)
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setWindowTitle("Error")
            msgBox.setText(str(e))
            msgBox.setStyleSheet("QLabel{color: red;}")
            msgBox.exec()
