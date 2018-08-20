#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, tools, CMake


class LibFreetypeConan(ConanFile):
    name = "freetype"
    version = "2.9.1"
    description = "FreeType is a library used to render text onto bitmaps, and provides support for other font-related operations."
    homepage = "https://www.freetype.org"
    license = "BSD"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports_sources = [
        "patches/CMakeProjectWrapper.txt",
        "patches/export_all.patch"
    ]
    requires = "zlib/1.2.11@fw4spl/stable"
    url = "https://gitlab.lan.local/conan/conan-freetype"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def source(self):
        freetype_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        tools.get("https://download.savannah.gnu.org/releases/freetype/freetype-{0}.tar.bz2".format(self.version))
        os.rename("freetype-" + self.version, self.source_subfolder)
        tools.patch(freetype_source_dir, "patches/export_all.patch")
        os.rename(os.path.join(self.source_subfolder, "CMakeLists.txt"),
                  os.path.join(self.source_subfolder, "CMakeListsOriginal.txt"))
        shutil.copy("patches/CMakeProjectWrapper.txt",
                    os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
