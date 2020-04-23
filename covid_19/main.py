from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivy.uix.scrollview import ScrollView
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
import json
from fuzzywuzzy import fuzz
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

with open("faq.json") as json_file:
    faq = json.load(json_file)

def classify_question(text):
    text = ' '.join(morph.parse(word)[0].normal_form for word in text.split())
    questions = list(faq.keys())
    scores = list()

    for question in questions:
        norm_question = ' '.join(morph.parse(word)[0].normal_form for word in question.split())
        scores.append(fuzz.WRatio(norm_question.lower(), text.lower()))
    if (max(scores) < 50):
        answer = "Некорректный вопрос или этого я не знаю"
    else:
        answer = faq[questions[scores.index(max(scores))]]
    return answer

class StartApp(Screen):
    pass

class MyBackdropFrontLayerFaq(ScrollView):
    text_input = ObjectProperty()
    label_widget = ObjectProperty()

    def ask_question(self):
        if self.text_input.text != "":
            self.label_widget.text = classify_question(self.text_input.text)
            self.text_input.text = ""
        else:
            self.label_widget.text = "Эмм, пустой вопрос..."

class ItemBackdropBackLayer(ThemableBehavior, BoxLayout):
    icon = StringProperty("android")
    text = StringProperty()
    selected_item = BooleanProperty(False)

    def set_item(self, instance):
        self.icon.set_item(instance.text)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            for item in self.parent.children:
                if item.selected_item:
                    item.selected_item = False
            self.selected_item = True
            if self.text == "Ask question":
                self.backdrop.close()
            if self.text == "About":
                self.backlayer.current = "second screen"
            if self.text == "Exit":
                raise SystemExit(1)
        return super().on_touch_down(touch)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Covid-19 FAQ"
        self.theme_cls.primary_palette = "Red"
        super().__init__(**kwargs)

    def build(self):
        self.root = StartApp()


if __name__ == "__main__":
    MainApp().run()
