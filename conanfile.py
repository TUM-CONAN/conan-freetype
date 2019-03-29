#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, tools, CMake


class LibFreetypeConan(ConanFile):
    name = "freetype"
    package_revision = "-r1"
    upstream_version = "2.9.1"
    version = "{0}{1}".format(upstream_version, package_revision)
    description = "FreeType is a library used to render text onto bitmaps, and provides support for other font-related operations."
    homepage = "https://www.freetype.org"
    license = "BSD"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports_sources = [
        "patches/CMakeProjectWrapper.txt",
        "patches/CMakeLists.patch"
    ]
    url = "https://git.ircad.fr/conan/conan-freetype"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx

    def requirements(self):
        if tools.os_info.is_windows:
            self.requires("zlib/1.2.11-r1@sight/testing")
        
    def source(self):
        freetype_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        tools.get("https://fossies.org/linux/misc/freetype-{0}.tar.bz2".format(self.upstream_version))
        os.rename("freetype-" + self.upstream_version, self.source_subfolder)
        tools.patch(freetype_source_dir, "patches/CMakeLists.patch")
        os.rename(os.path.join(self.source_subfolder, "CMakeLists.txt"),
                  os.path.join(self.source_subfolder, "CMakeListsOriginal.txt"))
        shutil.copy("patches/CMakeProjectWrapper.txt",
                    os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def build(self):
        cmake = CMake(self)
        cmake.definitions["DISABLE_FORCE_DEBUG_POSTFIX"] = "ON"
        if not tools.os_info.is_windows:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
