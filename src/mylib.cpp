#include "mylib.h"
#include <iostream>

#ifdef _WIN32
void mylib_function() {
  std::cout << "Hello from MyLib in windows!" << std::endl;
}
#elif defined(__linux__)
void mylib_function() {
  std::cout << "Hello from MyLib in linux!" << std::endl;
}
#endif