import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton

class VotingApp(QMainWindow):
    def __init__(self, votingSystem):
        super().__init__()
        self.votingSystem = votingSystem
        self.setWindowTitle("Vote")
        self.setFixedSize(300, 200)
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        #used AI to help with this section
        # Display current votes from CSV
        johnVotes = self.votingSystem.getVotes('john')
        janeVotes = self.votingSystem.getVotes('jane')
        self.label = QLabel(f"John: {johnVotes} | Jane: {janeVotes}")
        layout.addWidget(self.label)
        
        for name in ["John", "Jane"]:
            btn = QPushButton(f"Vote for {name}")
            btn.clicked.connect(lambda _, n=name: self.vote(n))
            layout.addWidget(btn)
    
    def vote(self, candidate):
        # Save vote to CSV through the voting system
        self.votingSystem.castVote(candidate)
        
        # Update display with current votes from CSV
        johnVotes = self.votingSystem.getVotes('john')
        janeVotes = self.votingSystem.getVotes('jane')
        self.label.setText(f"John: {johnVotes} | Jane: {janeVotes}")
