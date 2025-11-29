import csv
import os
import sys
from PyQt6.QtWidgets import QApplication
from gui import VotingApp

def main():
    votingSystem = VotingSystem()
    app = QApplication(sys.argv)
    window = VotingApp(votingSystem)
    window.show()
    sys.exit(app.exec())

class VotingSystem:
    
    def __init__(self, csvFile="data.csv"):
        self.csvFile = csvFile
        self.votes = {'john': 0, 'jane': 0}
        self.initializeCsv()
    
    def initializeCsv(self):
        """Create CSV file if it doesn't exist"""
        if not os.path.exists(self.csvFile):
            with open(self.csvFile, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['candidate', 'votes'])
                writer.writerow(['john', 0])
                writer.writerow(['jane', 0])
    
    def loadVotes(self):
        with open(self.csvFile, 'r') as file:

            reader = csv.DictReader(file)
            for row in reader:
                candidate = row['candidate'].lower()
                self.votes[candidate] = int(row['votes'])
    
    def saveVotes(self):
        with open(self.csvFile, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['candidate', 'votes'])
            for candidate, votes in self.votes.items():
                writer.writerow([candidate, votes])
    
    def castVote(self, candidate):
        candidate = candidate.lower()
        if candidate in self.votes:
            self.votes[candidate] += 1
            self.saveVotes()  # Save to CSV after each vote
        else:
            raise ValueError(f"Candidate '{candidate}' not found")
    
    def getVotes(self, candidate=None):
        if candidate:
            return self.votes[candidate.lower()]
        return self.votes.copy()

if __name__ == "__main__":
    main()