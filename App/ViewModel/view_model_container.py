from View.LeftPanel.Widgets.directory_widget import DirectoryWidget
from View.LeftPanel.Widgets.execute_stop_buttons import ExecuteStopButtons
from View.LeftPanel.Widgets.platform_dropdown_menu import PlatformDropdownMenu
from View.LeftPanel.Widgets.progress_info_labels import ProgressInfoLabel
from View.LeftPanel.Widgets.status_dialog_bar import StatusDialogBar
from View.config_view import ConfigView


class ViewModelContainer:
    def __init__(self, view_model):
        self.view_model = view_model

        self.directory_widget = DirectoryWidget(view_model)
        self.platform_dropdown_menu = PlatformDropdownMenu(view_model)
        self.progress_info_label = ProgressInfoLabel(view_model)
        self.execution_buttons = ExecuteStopButtons(view_model)
        self.status_dialog_bar = StatusDialogBar(view_model)
        self.config_window = ConfigView(view_model)