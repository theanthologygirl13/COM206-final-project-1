import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, 
                             QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt

class SimpleTodoApp(QWidget):
    def __init__(self):
        super().__init__()
        # Window Title and Size
        self.setWindowTitle("Simple Todo List")
        self.resize(400, 400)
        
        # 1. Creating UI Elements
        self.input_task = QLineEdit()
        self.input_task.setPlaceholderText("Type a new task...")
        
        self.btn_add = QPushButton("Add Task")
        self.list_tasks = QListWidget()
        self.btn_delete = QPushButton("Delete Selected")
        
        # 2. Layout Settings
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.input_task)
        top_layout.addWidget(self.btn_add)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.list_tasks)
        main_layout.addWidget(self.btn_delete)
        self.setLayout(main_layout)
        
        # 3. Connecting Signals and Slots
        self.btn_add.clicked.connect(self.add_task)
        self.input_task.returnPressed.connect(self.add_task) # Trigger on Enter key
        self.btn_delete.clicked.connect(self.delete_task)
        
        # Trigger when a checkbox state changes
        self.list_tasks.itemChanged.connect(self.task_status_changed)

    def add_task(self):
        text = self.input_task.text().strip()
        if text:
            item = QListWidgetItem(text)
            # Enable a checkable checkbox for the item
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable) 
            item.setCheckState(Qt.Unchecked) # Start as unchecked by default
            
            self.list_tasks.addItem(item)
            self.input_task.clear() # Clear the input field

    def task_status_changed(self, item):
        # Disconnect signal temporarily to prevent infinite loop/recursion
        self.list_tasks.itemChanged.disconnect(self.task_status_changed)
        
        current_text = item.text()
        
        if item.checkState() == Qt.Checked: # If checkbox is checked
            if not current_text.endswith(" (Completed)"):
                item.setText(f"{current_text} (Completed)")
        else: # If checkbox is unchecked
            if current_text.endswith(" (Completed)"):
                item.setText(current_text.replace(" (Completed)", ""))
                
        # Reconnect the signal
        self.list_tasks.itemChanged.connect(self.task_status_changed)

    def delete_task(self):
        selected_item = self.list_tasks.currentItem()
        if selected_item:
            # Find the row index of the selected item and remove it
            self.list_tasks.takeItem(self.list_tasks.row(selected_item))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleTodoApp()
    window.show()
    sys.exit(app.exec())