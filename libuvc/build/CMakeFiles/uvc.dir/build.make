# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.5

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/sensor/Desktop/coviduipy/libuvc

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/sensor/Desktop/coviduipy/libuvc/build

# Include any dependencies generated for this target.
include CMakeFiles/uvc.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/uvc.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/uvc.dir/flags.make

CMakeFiles/uvc.dir/src/ctrl.c.o: CMakeFiles/uvc.dir/flags.make
CMakeFiles/uvc.dir/src/ctrl.c.o: ../src/ctrl.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sensor/Desktop/coviduipy/libuvc/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/uvc.dir/src/ctrl.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/uvc.dir/src/ctrl.c.o   -c /home/sensor/Desktop/coviduipy/libuvc/src/ctrl.c

CMakeFiles/uvc.dir/src/ctrl.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/uvc.dir/src/ctrl.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sensor/Desktop/coviduipy/libuvc/src/ctrl.c > CMakeFiles/uvc.dir/src/ctrl.c.i

CMakeFiles/uvc.dir/src/ctrl.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/uvc.dir/src/ctrl.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sensor/Desktop/coviduipy/libuvc/src/ctrl.c -o CMakeFiles/uvc.dir/src/ctrl.c.s

CMakeFiles/uvc.dir/src/ctrl.c.o.requires:

.PHONY : CMakeFiles/uvc.dir/src/ctrl.c.o.requires

CMakeFiles/uvc.dir/src/ctrl.c.o.provides: CMakeFiles/uvc.dir/src/ctrl.c.o.requires
	$(MAKE) -f CMakeFiles/uvc.dir/build.make CMakeFiles/uvc.dir/src/ctrl.c.o.provides.build
.PHONY : CMakeFiles/uvc.dir/src/ctrl.c.o.provides

CMakeFiles/uvc.dir/src/ctrl.c.o.provides.build: CMakeFiles/uvc.dir/src/ctrl.c.o


CMakeFiles/uvc.dir/src/ctrl-gen.c.o: CMakeFiles/uvc.dir/flags.make
CMakeFiles/uvc.dir/src/ctrl-gen.c.o: ../src/ctrl-gen.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sensor/Desktop/coviduipy/libuvc/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/uvc.dir/src/ctrl-gen.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/uvc.dir/src/ctrl-gen.c.o   -c /home/sensor/Desktop/coviduipy/libuvc/src/ctrl-gen.c

CMakeFiles/uvc.dir/src/ctrl-gen.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/uvc.dir/src/ctrl-gen.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sensor/Desktop/coviduipy/libuvc/src/ctrl-gen.c > CMakeFiles/uvc.dir/src/ctrl-gen.c.i

CMakeFiles/uvc.dir/src/ctrl-gen.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/uvc.dir/src/ctrl-gen.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sensor/Desktop/coviduipy/libuvc/src/ctrl-gen.c -o CMakeFiles/uvc.dir/src/ctrl-gen.c.s

CMakeFiles/uvc.dir/src/ctrl-gen.c.o.requires:

.PHONY : CMakeFiles/uvc.dir/src/ctrl-gen.c.o.requires

CMakeFiles/uvc.dir/src/ctrl-gen.c.o.provides: CMakeFiles/uvc.dir/src/ctrl-gen.c.o.requires
	$(MAKE) -f CMakeFiles/uvc.dir/build.make CMakeFiles/uvc.dir/src/ctrl-gen.c.o.provides.build
.PHONY : CMakeFiles/uvc.dir/src/ctrl-gen.c.o.provides

CMakeFiles/uvc.dir/src/ctrl-gen.c.o.provides.build: CMakeFiles/uvc.dir/src/ctrl-gen.c.o


CMakeFiles/uvc.dir/src/device.c.o: CMakeFiles/uvc.dir/flags.make
CMakeFiles/uvc.dir/src/device.c.o: ../src/device.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sensor/Desktop/coviduipy/libuvc/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object CMakeFiles/uvc.dir/src/device.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/uvc.dir/src/device.c.o   -c /home/sensor/Desktop/coviduipy/libuvc/src/device.c

CMakeFiles/uvc.dir/src/device.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/uvc.dir/src/device.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sensor/Desktop/coviduipy/libuvc/src/device.c > CMakeFiles/uvc.dir/src/device.c.i

CMakeFiles/uvc.dir/src/device.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/uvc.dir/src/device.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sensor/Desktop/coviduipy/libuvc/src/device.c -o CMakeFiles/uvc.dir/src/device.c.s

CMakeFiles/uvc.dir/src/device.c.o.requires:

.PHONY : CMakeFiles/uvc.dir/src/device.c.o.requires

CMakeFiles/uvc.dir/src/device.c.o.provides: CMakeFiles/uvc.dir/src/device.c.o.requires
	$(MAKE) -f CMakeFiles/uvc.dir/build.make CMakeFiles/uvc.dir/src/device.c.o.provides.build
.PHONY : CMakeFiles/uvc.dir/src/device.c.o.provides

CMakeFiles/uvc.dir/src/device.c.o.provides.build: CMakeFiles/uvc.dir/src/device.c.o


CMakeFiles/uvc.dir/src/diag.c.o: CMakeFiles/uvc.dir/flags.make
CMakeFiles/uvc.dir/src/diag.c.o: ../src/diag.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sensor/Desktop/coviduipy/libuvc/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building C object CMakeFiles/uvc.dir/src/diag.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/uvc.dir/src/diag.c.o   -c /home/sensor/Desktop/coviduipy/libuvc/src/diag.c

CMakeFiles/uvc.dir/src/diag.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/uvc.dir/src/diag.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sensor/Desktop/coviduipy/libuvc/src/diag.c > CMakeFiles/uvc.dir/src/diag.c.i

CMakeFiles/uvc.dir/src/diag.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/uvc.dir/src/diag.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sensor/Desktop/coviduipy/libuvc/src/diag.c -o CMakeFiles/uvc.dir/src/diag.c.s

CMakeFiles/uvc.dir/src/diag.c.o.requires:

.PHONY : CMakeFiles/uvc.dir/src/diag.c.o.requires

CMakeFiles/uvc.dir/src/diag.c.o.provides: CMakeFiles/uvc.dir/src/diag.c.o.requires
	$(MAKE) -f CMakeFiles/uvc.dir/build.make CMakeFiles/uvc.dir/src/diag.c.o.provides.build
.PHONY : CMakeFiles/uvc.dir/src/diag.c.o.provides

CMakeFiles/uvc.dir/src/diag.c.o.provides.build: CMakeFiles/uvc.dir/src/diag.c.o


CMakeFiles/uvc.dir/src/frame.c.o: CMakeFiles/uvc.dir/flags.make
CMakeFiles/uvc.dir/src/frame.c.o: ../src/frame.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sensor/Desktop/coviduipy/libuvc/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building C object CMakeFiles/uvc.dir/src/frame.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/uvc.dir/src/frame.c.o   -c /home/sensor/Desktop/coviduipy/libuvc/src/frame.c

CMakeFiles/uvc.dir/src/frame.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/uvc.dir/src/frame.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sensor/Desktop/coviduipy/libuvc/src/frame.c > CMakeFiles/uvc.dir/src/frame.c.i

CMakeFiles/uvc.dir/src/frame.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/uvc.dir/src/frame.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sensor/Desktop/coviduipy/libuvc/src/frame.c -o CMakeFiles/uvc.dir/src/frame.c.s

CMakeFiles/uvc.dir/src/frame.c.o.requires:

.PHONY : CMakeFiles/uvc.dir/src/frame.c.o.requires

CMakeFiles/uvc.dir/src/frame.c.o.provides: CMakeFiles/uvc.dir/src/frame.c.o.requires
	$(MAKE) -f CMakeFiles/uvc.dir/build.make CMakeFiles/uvc.dir/src/frame.c.o.provides.build
.PHONY : CMakeFiles/uvc.dir/src/frame.c.o.provides

CMakeFiles/uvc.dir/src/frame.c.o.provides.build: CMakeFiles/uvc.dir/src/frame.c.o


CMakeFiles/uvc.dir/src/init.c.o: CMakeFiles/uvc.dir/flags.make
CMakeFiles/uvc.dir/src/init.c.o: ../src/init.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sensor/Desktop/coviduipy/libuvc/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building C object CMakeFiles/uvc.dir/src/init.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/uvc.dir/src/init.c.o   -c /home/sensor/Desktop/coviduipy/libuvc/src/init.c

CMakeFiles/uvc.dir/src/init.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/uvc.dir/src/init.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sensor/Desktop/coviduipy/libuvc/src/init.c > CMakeFiles/uvc.dir/src/init.c.i

CMakeFiles/uvc.dir/src/init.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/uvc.dir/src/init.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sensor/Desktop/coviduipy/libuvc/src/init.c -o CMakeFiles/uvc.dir/src/init.c.s

CMakeFiles/uvc.dir/src/init.c.o.requires:

.PHONY : CMakeFiles/uvc.dir/src/init.c.o.requires

CMakeFiles/uvc.dir/src/init.c.o.provides: CMakeFiles/uvc.dir/src/init.c.o.requires
	$(MAKE) -f CMakeFiles/uvc.dir/build.make CMakeFiles/uvc.dir/src/init.c.o.provides.build
.PHONY : CMakeFiles/uvc.dir/src/init.c.o.provides

CMakeFiles/uvc.dir/src/init.c.o.provides.build: CMakeFiles/uvc.dir/src/init.c.o


CMakeFiles/uvc.dir/src/stream.c.o: CMakeFiles/uvc.dir/flags.make
CMakeFiles/uvc.dir/src/stream.c.o: ../src/stream.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sensor/Desktop/coviduipy/libuvc/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building C object CMakeFiles/uvc.dir/src/stream.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/uvc.dir/src/stream.c.o   -c /home/sensor/Desktop/coviduipy/libuvc/src/stream.c

CMakeFiles/uvc.dir/src/stream.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/uvc.dir/src/stream.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sensor/Desktop/coviduipy/libuvc/src/stream.c > CMakeFiles/uvc.dir/src/stream.c.i

CMakeFiles/uvc.dir/src/stream.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/uvc.dir/src/stream.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sensor/Desktop/coviduipy/libuvc/src/stream.c -o CMakeFiles/uvc.dir/src/stream.c.s

CMakeFiles/uvc.dir/src/stream.c.o.requires:

.PHONY : CMakeFiles/uvc.dir/src/stream.c.o.requires

CMakeFiles/uvc.dir/src/stream.c.o.provides: CMakeFiles/uvc.dir/src/stream.c.o.requires
	$(MAKE) -f CMakeFiles/uvc.dir/build.make CMakeFiles/uvc.dir/src/stream.c.o.provides.build
.PHONY : CMakeFiles/uvc.dir/src/stream.c.o.provides

CMakeFiles/uvc.dir/src/stream.c.o.provides.build: CMakeFiles/uvc.dir/src/stream.c.o


CMakeFiles/uvc.dir/src/misc.c.o: CMakeFiles/uvc.dir/flags.make
CMakeFiles/uvc.dir/src/misc.c.o: ../src/misc.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/sensor/Desktop/coviduipy/libuvc/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building C object CMakeFiles/uvc.dir/src/misc.c.o"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/uvc.dir/src/misc.c.o   -c /home/sensor/Desktop/coviduipy/libuvc/src/misc.c

CMakeFiles/uvc.dir/src/misc.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/uvc.dir/src/misc.c.i"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/sensor/Desktop/coviduipy/libuvc/src/misc.c > CMakeFiles/uvc.dir/src/misc.c.i

CMakeFiles/uvc.dir/src/misc.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/uvc.dir/src/misc.c.s"
	/usr/bin/cc  $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/sensor/Desktop/coviduipy/libuvc/src/misc.c -o CMakeFiles/uvc.dir/src/misc.c.s

CMakeFiles/uvc.dir/src/misc.c.o.requires:

.PHONY : CMakeFiles/uvc.dir/src/misc.c.o.requires

CMakeFiles/uvc.dir/src/misc.c.o.provides: CMakeFiles/uvc.dir/src/misc.c.o.requires
	$(MAKE) -f CMakeFiles/uvc.dir/build.make CMakeFiles/uvc.dir/src/misc.c.o.provides.build
.PHONY : CMakeFiles/uvc.dir/src/misc.c.o.provides

CMakeFiles/uvc.dir/src/misc.c.o.provides.build: CMakeFiles/uvc.dir/src/misc.c.o


# Object files for target uvc
uvc_OBJECTS = \
"CMakeFiles/uvc.dir/src/ctrl.c.o" \
"CMakeFiles/uvc.dir/src/ctrl-gen.c.o" \
"CMakeFiles/uvc.dir/src/device.c.o" \
"CMakeFiles/uvc.dir/src/diag.c.o" \
"CMakeFiles/uvc.dir/src/frame.c.o" \
"CMakeFiles/uvc.dir/src/init.c.o" \
"CMakeFiles/uvc.dir/src/stream.c.o" \
"CMakeFiles/uvc.dir/src/misc.c.o"

# External object files for target uvc
uvc_EXTERNAL_OBJECTS =

libuvc.so: CMakeFiles/uvc.dir/src/ctrl.c.o
libuvc.so: CMakeFiles/uvc.dir/src/ctrl-gen.c.o
libuvc.so: CMakeFiles/uvc.dir/src/device.c.o
libuvc.so: CMakeFiles/uvc.dir/src/diag.c.o
libuvc.so: CMakeFiles/uvc.dir/src/frame.c.o
libuvc.so: CMakeFiles/uvc.dir/src/init.c.o
libuvc.so: CMakeFiles/uvc.dir/src/stream.c.o
libuvc.so: CMakeFiles/uvc.dir/src/misc.c.o
libuvc.so: CMakeFiles/uvc.dir/build.make
libuvc.so: /usr/lib/x86_64-linux-gnu/libusb-1.0.so
libuvc.so: CMakeFiles/uvc.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/sensor/Desktop/coviduipy/libuvc/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Linking C shared library libuvc.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/uvc.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/uvc.dir/build: libuvc.so

.PHONY : CMakeFiles/uvc.dir/build

CMakeFiles/uvc.dir/requires: CMakeFiles/uvc.dir/src/ctrl.c.o.requires
CMakeFiles/uvc.dir/requires: CMakeFiles/uvc.dir/src/ctrl-gen.c.o.requires
CMakeFiles/uvc.dir/requires: CMakeFiles/uvc.dir/src/device.c.o.requires
CMakeFiles/uvc.dir/requires: CMakeFiles/uvc.dir/src/diag.c.o.requires
CMakeFiles/uvc.dir/requires: CMakeFiles/uvc.dir/src/frame.c.o.requires
CMakeFiles/uvc.dir/requires: CMakeFiles/uvc.dir/src/init.c.o.requires
CMakeFiles/uvc.dir/requires: CMakeFiles/uvc.dir/src/stream.c.o.requires
CMakeFiles/uvc.dir/requires: CMakeFiles/uvc.dir/src/misc.c.o.requires

.PHONY : CMakeFiles/uvc.dir/requires

CMakeFiles/uvc.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/uvc.dir/cmake_clean.cmake
.PHONY : CMakeFiles/uvc.dir/clean

CMakeFiles/uvc.dir/depend:
	cd /home/sensor/Desktop/coviduipy/libuvc/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/sensor/Desktop/coviduipy/libuvc /home/sensor/Desktop/coviduipy/libuvc /home/sensor/Desktop/coviduipy/libuvc/build /home/sensor/Desktop/coviduipy/libuvc/build /home/sensor/Desktop/coviduipy/libuvc/build/CMakeFiles/uvc.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/uvc.dir/depend

