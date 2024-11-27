import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QFileDialog, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt

# Import the grading functions from the original script
from typealong_grader import grade_typealong, find_java_files

class TypeAlongGraderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() 

    def initUI(self):
        self.setWindowTitle('Type-Along Grading Tool')
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        layout = QVBoxLayout()

        # Source Code Selection
        source_layout = QHBoxLayout()
        self.source_label = QLabel('Source Code:')
        self.source_path = QLineEdit()
        self.source_browse = QPushButton('Browse')
        self.source_browse.clicked.connect(self.browse_source_code)
        source_layout.addWidget(self.source_label)
        source_layout.addWidget(self.source_path)
        source_layout.addWidget(self.source_browse)
        layout.addLayout(source_layout)

        # Student Directory Selection
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel('Student Directory:')
        self.dir_path = QLineEdit()
        self.dir_browse = QPushButton('Browse')
        self.dir_browse.clicked.connect(self.browse_student_directory)
        dir_layout.addWidget(self.dir_label)
        dir_layout.addWidget(self.dir_path)
        dir_layout.addWidget(self.dir_browse)
        layout.addLayout(dir_layout)

        # Points Configuration
        points_layout = QHBoxLayout()
        self.total_points_label = QLabel('Total Points:')
        self.total_points = QLineEdit()
        self.points_per_mistake_label = QLabel('Points per Mistake:')
        self.points_per_mistake = QLineEdit('0.1')
        points_layout.addWidget(self.total_points_label)
        points_layout.addWidget(self.total_points)
        points_layout.addWidget(self.points_per_mistake_label)
        points_layout.addWidget(self.points_per_mistake)
        layout.addLayout(points_layout)

        # Comment Handling Configuration
        comment_layout = QHBoxLayout()
        self.comment_label = QLabel('Ignore Comments:')
        self.comment_dropdown = QComboBox()
        self.comment_dropdown.addItems(['eol', 'none', 'all'])
        self.comment_dropdown.setCurrentText('eol')  # Default to end-of-line
        comment_layout.addWidget(self.comment_label)
        comment_layout.addWidget(self.comment_dropdown)
        comment_layout.addStretch(1)  # Add stretch to prevent unnecessary expansion
        layout.addLayout(comment_layout)

        # Output File Configuration
        output_layout = QHBoxLayout()
        self.output_label = QLabel('Output File:')
        self.output_path = QLineEdit('typealong-graded.csv')
        self.output_browse = QPushButton('Browse')
        self.output_browse.clicked.connect(self.browse_output_file)
        
        # Output Format Selection
        self.output_format_label = QLabel('Format:')
        self.output_format_dropdown = QComboBox()
        self.output_format_dropdown.addItems([
            'CSV (*.csv)', 
            'Excel (*.xlsx)', 
            'Tab-Separated (*.tsv)', 
            'JSON (*.json)', 
            'Parquet (*.parquet)'
        ])
        self.output_format_dropdown.currentTextChanged.connect(self.update_output_extension)
        
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(self.output_format_label)
        output_layout.addWidget(self.output_format_dropdown)
        output_layout.addWidget(self.output_browse)
        layout.addLayout(output_layout)

        # Grade Button
        self.grade_button = QPushButton('Grade Assignments')
        self.grade_button.clicked.connect(self.grade_assignments)
        layout.addWidget(self.grade_button)

        # Results Table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(['Student Name', 'Score', 'Mistakes'])
        layout.addWidget(self.results_table)

        self.setLayout(layout)

    def update_output_extension(self, format_text):
        """Update the output file extension based on selected format"""
        current_path = self.output_path.text()
        # Remove existing extension
        base_path = os.path.splitext(current_path)[0]
        
        # Map format to extension
        format_map = {
            'CSV (*.csv)': '.csv',
            'Excel (*.xlsx)': '.xlsx',
            'Tab-Separated (*.tsv)': '.tsv',
            'JSON (*.json)': '.json',
            'Parquet (*.parquet)': '.parquet'
        }
        
        # Update path with new extension
        new_path = base_path + format_map[format_text]
        self.output_path.setText(new_path)

    def browse_source_code(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select Source Code File', 
                                                  '', 'Java Files (*.java)')
        if filename:
            self.source_path.setText(filename)

    def browse_student_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Student Directory')
        if directory:
            self.dir_path.setText(directory)

    def browse_output_file(self):
        # Get the current format
        current_format = self.output_format_dropdown.currentText()
        
        # Map format to file filter
        format_filters = {
            'CSV (*.csv)': 'CSV Files (*.csv)',
            'Excel (*.xlsx)': 'Excel Files (*.xlsx)',
            'Tab-Separated (*.tsv)': 'Tab-Separated Files (*.tsv)',
            'JSON (*.json)': 'JSON Files (*.json)',
            'Parquet (*.parquet)': 'Parquet Files (*.parquet)'
        }
        
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            'Save Output File', 
            self.output_path.text(), 
            format_filters[current_format]
        )
        
        if filename:
            self.output_path.setText(filename)

    def grade_assignments(self):
        # Validate inputs
        if not self.validate_inputs():
            return

        try:
            # Find student files
            student_files = find_java_files(self.dir_path.text())

            # Grade assignments
            total_points = float(self.total_points.text())
            points_per_mistake = float(self.points_per_mistake.text())
            ignore_comments = self.comment_dropdown.currentText()
            
            grades = grade_typealong(
                self.source_path.text(), 
                student_files, 
                total_points, 
                points_per_mistake,
                ignore_comments
            )

            # Convert grades to pandas DataFrame
            df = pd.DataFrame(grades, columns=['Student Name', 'Score', 'Mistakes'])
            
            # Explode the Mistakes column to make it more readable
            df['Mistakes'] = df['Mistakes'].apply(lambda x: ', '.join(x))

            # Save based on selected format
            output_path = self.output_path.text()
            output_format = self.output_format_dropdown.currentText().split()[0].lower()

            # Save using appropriate pandas method
            if output_format == 'csv':
                df.to_csv(output_path, index=False)
            elif output_format == 'excel':
                df.to_excel(output_path, index=False)
            elif output_format == 'tab-separated':
                df.to_csv(output_path, sep='\t', index=False)
            elif output_format == 'json':
                df.to_json(output_path, orient='records')
            elif output_format == 'parquet':
                df.to_parquet(output_path, index=False)

            # Populate results table
            self.results_table.setRowCount(len(grades))
            for row, (name, score, mistakes) in enumerate(grades):
                self.results_table.setItem(row, 0, QTableWidgetItem(name))
                self.results_table.setItem(row, 1, QTableWidgetItem(str(score)))
                self.results_table.setItem(row, 2, QTableWidgetItem(', '.join(mistakes)))

            # Show success message
            QMessageBox.information(self, 'Grading Complete', 
                                    f'Graded {len(grades)} assignments. '
                                    f'Results saved to {output_path}')

        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def validate_inputs(self):
        # Check if all required fields are filled
        if not self.source_path.text():
            QMessageBox.warning(self, 'Missing Input', 'Please select source code file.')
            return False
        
        if not self.dir_path.text():
            QMessageBox.warning(self, 'Missing Input', 'Please select student directory.')
            return False
        
        if not self.total_points.text():
            QMessageBox.warning(self, 'Missing Input', 'Please enter total points.')
            return False
        
        try:
            float(self.total_points.text())
            float(self.points_per_mistake.text())
        except ValueError:
            QMessageBox.warning(self, 'Invalid Input', 'Points must be numeric.')
            return False
        
        return True

def main():
    app = QApplication(sys.argv)
    ex = TypeAlongGraderApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()