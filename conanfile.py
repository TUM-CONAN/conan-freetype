#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, tools, CMake


class LibFreetypeConan(ConanFile):
    name = "freetype"
    package_revision = "-r2"
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
        self.requires("common/1.0.0@sight/stable")
        if tools.os_info.is_windows:
            self.requires("zlib/1.2.11-r2@sight/testing")
        
    def source(self):
        freetype_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        tools.get("https://download.savannah.gnu.org/releases/freetype/freetype-{0}.tar.bz2".format(self.upstream_version))
        os.rename("freetype-" + self.upstream_version, self.source_subfolder)
        tools.patch(freetype_source_dir, "patches/CMakeLists.patch")
        os.rename(os.path.join(self.source_subfolder, "CMakeLists.txt"),
                  os.path.join(self.source_subfolder, "CMakeListsOriginal.txt"))
        shutil.copy("patches/CMakeProjectWrapper.txt",
                    os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def build(self):
        #Import common flags and defines
        import common
        cmake = CMake(self)
        
        #Set common flags
        cmake.definitions["CMAKE_C_FLAGS"] = common.get_c_flags()
        cmake.definitions["CMAKE_CXX_FLAGS"] = common.get_cxx_flags()
        
        cmake.definitions["DISABLE_FORCE_DEBUG_POSTFIX"] = "ON"
        if not tools.os_info.is_windows:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
