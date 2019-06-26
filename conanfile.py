# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class MimallocConan(ConanFile):
    name = "mimalloc"
    version = "1.0"
    description = "mimalloc is a compact general purpose allocator with excellent performance"
    topics = ("ansic", "pure-c", "memory", "malloc")
    url = "https://github.com/bincrafters/conan-mimalloc"
    homepage = "https://github.com/microsoft/mimalloc"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "override": [True, False],
        "interpose": [True, False],
        "see_asm": [True, False],
        "use_cxx": [True, False],
        "secure": [True, False],
        "build_object": [True, False],
    }
    default_options = {
        "shared": False,
        "override": True,
        "interpose": True,
        "see_asm": False,
        "use_cxx": False,
        "secure": False,
        "build_object": False,
    }
    _source_subfolder = "source_subfolder"

    def source(self):
    
        # source_url = self.homepage
        source_url = "https://github.com/myd7349/mimalloc/archive/cmake-build-options.zip"
        # checksum = "59eacb387386e2dd4cf0601579864f70a3ebb68dc32195d30314e5d9a0658457"
        commit = "1789452b87d11f6b773f2331d43dd49dd1421e96"
        # tools.get("{0}/archive/{1}.zip".format(source_url, commit), sha256=checksum)
        # tools.get("{0}/archive/{1}.zip".format(source_url, commit))
        tools.get(source_url)
        # extracted_dir = self.name + "-" + commit
        extracted_dir = "mimalloc-cmake-build-options"
        os.rename(extracted_dir, self._source_subfolder)
        
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["MI_SHARED"] = self.options.shared
        cmake.definitions["MI_STATIC"] = not self.options.shared
        cmake.definitions["MI_OVERRIDE"] = self.options.override
        cmake.definitions["MI_INTERPOSE"] = self.options.interpose
        cmake.definitions["MI_SEE_ASM"] = self.options.see_asm
        cmake.definitions["MI_USE_CXX"] = self.options.use_cxx
        cmake.definitions["MI_SECURE"] = self.options.secure
        cmake.definitions["MI_BUILD_OBJECT"] = self.options.build_object
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["mimalloc"] if self.options.shared else ["mimalloc-static"]
        self.cpp_info.libdirs = ["lib/mimalloc-1.0"]
        self.cpp_info.bindirs = ["lib"]
        self.cpp_info.includedirs = ["lib/mimalloc-1.0/include"]