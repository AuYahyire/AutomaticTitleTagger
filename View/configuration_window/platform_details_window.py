from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QInputDialog, QGroupBox

PIXEL_SIZE = 25

class PlatformDetailsWindow(QGroupBox):
    def __init__(self, view_model):
        super().__init__("Platform prompts:")
        self.config_view_model = view_model
        self.current_platform = None
        self.layout = QVBoxLayout()
        self.prompt_labels = {}  # Dictionary to store QLabel references
        self.setup_components()
        self.setLayout(self.layout)

        self.config_view_model.platform_changed.connect(self.update_platform)

        # Automatically load the first platform's prompts
        self.auto_load_first_platform()

    def auto_load_first_platform(self):
        platforms = list(self.config_view_model.get_platform_list())
        if platforms:
            first_platform = platforms[0]
            # Manually trigger the platform changed event
            self.config_view_model.platform_changed.emit(first_platform)

    def setup_components(self):
        self.system_prompt_layout = self.create_prompt_row("System prompt:", "system_text")
        self.user_prompt_layout = self.create_prompt_row("User prompt:", "user_text")
        self.layout.addLayout(self.system_prompt_layout)
        self.layout.addLayout(self.user_prompt_layout)

    def create_prompt_row(self, label_text, prompt_type):
        row = QHBoxLayout()

        label = QLabel(label_text)
        value_label = QLabel("")

        edit_button = QPushButton("...")
        edit_button.setFixedSize(PIXEL_SIZE, PIXEL_SIZE)

        # Connect the edit button to the edit_prompt method with the prompt_type
        edit_button.clicked.connect(lambda checked, pt=prompt_type: self.edit_prompt(pt))

        row.addWidget(label)
        row.addWidget(value_label)
        row.addWidget(edit_button)

        # Store the reference to the value_label with the prompt_type as the key
        self.prompt_labels[prompt_type] = value_label

        return row

    def update_platform(self, platform):
        print(f"Updating platform to: {platform}")
        self.current_platform = platform
        if platform:
            system_prompt = self.config_view_model.get_platform_prompts(platform, "system_prompt")
            user_prompt = self.config_view_model.get_platform_prompts(platform, "user_prompt")
            #TODO: Simplificar esto, estoy obteniendo dos veces el mismo diccionario.
            self.update_prompt_displays(system_prompt, user_prompt)

    def update_prompt_displays(self, system_prompt, user_prompt):
        # Update the labels with the new prompt values
        # Add error handling to prevent potential KeyError
        try:
            # Truncate the text to a maximum length (e.g., 100 characters)
            max_length = 100
            system_text = (system_prompt.get('system_text', "") or "")[:max_length]
            user_text = (user_prompt.get('user_text', "") or "")[:max_length]

            self.system_prompt_layout.itemAt(1).widget().setText(system_text) #system_prompt_layout tiene 3 widgets, por eso accede al itemAt(1) que es el QLabel()
            self.user_prompt_layout.itemAt(1).widget().setText(user_text)
        except Exception as e:
            print(f"Error updating prompt displays: {e}")
            # Optionally, set empty strings if there's an error
            self.system_prompt_layout.itemAt(1).widget().setText("")
            self.user_prompt_layout.itemAt(1).widget().setText("")

        # TODO: Truncar texto del prompt.

    def edit_prompt(self, prompt_type):
        if not self.current_platform:
            QMessageBox.warning(self, "No Platform Selected", "Please select a platform first.")
            return

        # Determine prompt attributes based on prompt_type
        if prompt_type == "system_text":
            current_prompt = self.config_view_model.get_platform_prompts(self.current_platform, prompt_type).get(
                'system_text', "")
            dialog_title = "Edit System Prompt"
            label = "System prompt:"
        elif prompt_type == "user_text":
            current_prompt = self.config_view_model.get_platform_prompts(self.current_platform, prompt_type).get(
                'user_text', "")
            dialog_title = "Edit User Prompt"
            label = "User prompt:"
        else:
            QMessageBox.warning(self, "Unknown Prompt Type", "The prompt type is unknown.")
            return

        # Open an input dialog to edit the prompt
        new_prompt, ok = QInputDialog.getMultiLineText(self, dialog_title, label, current_prompt)

        if ok:
            new_prompt = new_prompt.strip()
            if new_prompt:
                # Update the ViewModel with the new prompt
                self.config_view_model.set_platform_prompts(self.current_platform, prompt_type, new_prompt)
                # Refresh the display
                self.update_platform(self.current_platform)
                print(f"{prompt_type} updated to: {new_prompt}")
            else:
                QMessageBox.warning(self, "Invalid Input", "Prompt cannot be empty.")