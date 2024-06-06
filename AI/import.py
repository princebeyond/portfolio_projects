#!/usr/bin/python3

import pkgutil
import google.generativeai

package = google.generativeai
for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
    print(module_name)
