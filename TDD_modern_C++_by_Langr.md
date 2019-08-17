- As the book is old, many features need updated. I keep some bookmarking here.
- gmock is not supported anymore while googletest (https://github.com/google/googletest) might be used instead
  - mkdir buld; cd build; cmake ..; make ; make install

- Prior to compiling sample codes
  - export GMOCK_HOME=<gtest_install_prefix>
- In each folder, adjust CMakeLists.txt from
```
include_directories($ENV{GMOCK_HOME}/include $ENV{GMOCK_HOME}/gtest/include)
link_directories($ENV{GMOCK_HOME}/mybuild $ENV{GMOCK_HOME}/gtest/mybuild)
```
to
```
include_directories($ENV{GMOCK_HOME}/include)
link_directories($ENV{GMOCK_HOME}/lib)
```
- In CMakeLists.txt, `add_executable(test ${sources})` crashes with CMAKE. Adjust using a different name such as `add_executable(testx ${sources})`
- The order of libraries might be important. If the compilation fails with the message of `undefined reference to pthread-getspecific`, then adjust CMakeLists.txt from:
```
target_link_libraries(testx pthread)
target_link_libraries(testx gtest)
target_link_libraries(testx gmock)
```
to:
```
target_link_libraries(testx gtest)
target_link_libraries(testx gmock)
target_link_libraries(testx pthread)
```
or `target_link_libraries(testx gtest gmock pthread)`
