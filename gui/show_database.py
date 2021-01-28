from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from settings import SHOW_DATABASE_SCREEN_PATH
from src.db.manager import DatabaseManager


Builder.load_file(SHOW_DATABASE_SCREEN_PATH)
db_manager = DatabaseManager()


class WarningPopup(Popup):

    label = StringProperty()

    def __init__(self, label, **kwargs):
        super(WarningPopup, self).__init__(**kwargs)
        self.set_description(label)

    def set_description(self, label):
        self.label = label


class DataAddPopup(Popup):

    obj = ObjectProperty(None)

    def __init__(self, obj, **kwargs):
        super(DataAddPopup, self).__init__(**kwargs)
        self.obj = obj


class DataRemovePopup(Popup):

    obj = ObjectProperty(None)

    def __init__(self, obj, **kwargs):
        super(DataRemovePopup, self).__init__(**kwargs)
        self.obj = obj


class DataUpdatePopup(Popup):

    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):

        super(DataUpdatePopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    """ Adds selection and focus behaviour to the view. """


class SelectableButton(RecycleDataViewBehavior, Button):
    """ Add selection support to the Button """

    index = None
    data = []
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(SelectableButton, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """

        self.index = index
        self.data = data

        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """

        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """

        self.selected = is_selected

    def on_press(self):

        popup = DataUpdatePopup(self)
        popup.open()

    def update_changes(self, txt):

        self.text = txt
        field_index = self.index % 3
        id_index = self.index // 3
        field = ""
        if field_index == 1:
            field = "T_Stamp"
        elif field_index == 2:
            field = "Butt_Number"
        db_manager.update_data(field, str(txt), id_index)


class ShowDatabase(Screen):

    data_items = ListProperty([])

    def on_enter(self, *args):

        rows = db_manager.read_data()
        for row in rows:
            for col in row:
                self.data_items.append(col)

    def on_leave(self, *args):
        self.data_items.clear()

    def add_data(self):

        popup = DataAddPopup(self)
        popup.open()

    def add_changes(self, t_stamp, butt_nums):

        if t_stamp != "" and butt_nums != "":
            if not self.data_items:
                user_id = 0
            else:
                user_id = int(self.data_items[-3]) + 1
            self.data_items.append(user_id)
            self.data_items.append(t_stamp)
            self.data_items.append(butt_nums)
            db_manager.insert_data(t_stamp=t_stamp, butt_num=butt_nums)

        else:
            warning_popup = WarningPopup("Please insert all fields")
            warning_popup.open()

    def remove_data(self):

        remove_popup = DataRemovePopup(self)
        remove_popup.open()

    def remove_changes(self, data_id):
        try:
            if data_id != "":
                user_id_indices = [n for n, item in enumerate(self.data_items) if item == int(data_id)]
                user_id_index = ""
                for index in user_id_indices:
                    if index % 3 == 0:
                        user_id_index = index
                for j in range(3):
                    self.data_items.pop(user_id_index)
                db_manager.delete_data(data_id=data_id)
            else:
                warning_popup = WarningPopup("Please insert Data ID fields")
                warning_popup.open()

        except Exception as e:
            print(e)
