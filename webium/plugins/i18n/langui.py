import os
import importlib

class swtLang(object):
    model = None
    def __init__(self, langfile="ENUS"):
        lib_folder = os.path.join("i18n")
        file_name = os.path.join(lib_folder, "window_" + langfile + ".py")
        model_path = lib_folder + "." + "window_" + langfile
        class_name = "open"
        print("Loading ... " + file_name)
        if os.path.exists(file_name):
            self.model = importlib.import_module(model_path)
        else:
            print("You have to create a gui configuration file for this language")
            raise FileNotFoundError

    def get(self, class_name):
        if class_name != "":
            try:
                return getattr(self.model, class_name)
            except AttributeError:
                return None
