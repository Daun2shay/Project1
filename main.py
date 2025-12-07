import csv
import os
import sys
from PyQt6.QtWidgets import QApplication
from gui import VotingApp

def main() -> None:
    """
    Main function to initialize and run the voting application.
    """
    votingSystem = VotingSystem()
    app = QApplication(sys.argv)
    window = VotingApp(votingSystem)
    window.show()
    sys.exit(app.exec())

class VotingSystem:
    """
    A voting system that tracks votes by ID and stores them in a CSV file.
    """
    
    def __init__(self, csvFile: str = "data.csv") -> None:
        """
        Initialize the voting system.
        
        Args:
            csvFile: Path to the CSV file for storing votes (default: "data.csv")
        """
        self.csvFile = csvFile
        self.votedIds = set()
        self.initializeCsv()
        self.loadVotes()
    
    def initializeCsv(self) -> None:
        """
        Create CSV file if it doesn't exist or recreate if format is incorrect.
        The CSV file should have columns: id, candidate.
        """
        # Check if file exists and has correct format
        if os.path.exists(self.csvFile):
            with open(self.csvFile, 'r') as file:
                firstLine = file.readline().strip()
                # If wrong format, recreate the file
                if firstLine != 'id,candidate':
                    os.remove(self.csvFile)
        
        # Create file with correct format if it doesn't exist
        if not os.path.exists(self.csvFile):
            with open(self.csvFile, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'candidate'])
    
    def loadVotes(self) -> None:
        """
        Load all voted IDs from the CSV file into memory.
        Populates the votedIds set with IDs that have already voted.
        """
        if os.path.exists(self.csvFile):
            with open(self.csvFile, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.votedIds.add(int(row['id']))
    
    def saveVote(self, voterId: int, candidate: str) -> None:
        """
        Append a vote record to the CSV file.
        
        Args:
            voterId: The ID of the voter (1-100)
            candidate: The name of the candidate voted for
        """
        with open(self.csvFile, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([voterId, candidate])
    
    def castVote(self, voterId: int, candidate: str) -> None:
        """
        Cast a vote for a candidate with voter ID tracking.
        
        Args:
            voterId: The ID of the voter (must be between 1-100)
            candidate: The name of the candidate to vote for
            
        Raises:
            ValueError: If voterId is out of range, has already voted, or candidate is invalid
        """
        # Validate voter ID
        if voterId < 1 or voterId > 100:
            raise ValueError("ID must be between 1 and 100")
        
        if voterId in self.votedIds:
            raise ValueError(f"ID {voterId} has already voted")
        
        candidate = candidate.lower()
        if candidate not in ['john', 'jane']:
            raise ValueError(f"Candidate '{candidate}' not found")
        
        # Record the vote
        self.votedIds.add(voterId)
        
        # Save to CSV
        self.saveVote(voterId, candidate)
    
    def hasVoted(self, voterId: int) -> bool:
        """
        Check if a voter ID has already cast a vote.
        
        Args:
            voterId: The ID to check
            
        Returns:
            True if the ID has voted, False otherwise
        """
        return voterId in self.votedIds
    
    def getVotes(self, candidate: str = None) -> int:
        """
        Get the vote count for a specific candidate.
        
        Args:
            candidate: The name of the candidate (optional)
            
        Returns:
            The number of votes for the candidate, or 0 if no candidate specified
        """
        if candidate:
            count = 0
            if os.path.exists(self.csvFile):
                with open(self.csvFile, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row['candidate'].lower() == candidate.lower():
                            count += 1
            return count
        return 0

if __name__ == "__main__":
    main()