#include "mylib.h"
#include <iostream>

#ifdef _WIN32
void mylib_function() {
#ifdef NDEBUG
  std::cout << "Hello from MyLib in Windows Release mode!" << std::endl;
#else
  std::cout << "Hello from MyLib in Windows Debug mode!" << std::endl;
#endif
}
#elif defined(__linux__)
void mylib_function() {
#ifdef NDEBUG
  std::cout << "Hello from MyLib in Linux Release mode!" << std::endl;
#else
  std::cout << "Hello from MyLib in Linux Debug mode!" << std::endl;
#endif
}
#endif