#include "nanomunchers_serialize_gtest.h"
#include "data_file_gtest.h"
#include "gtest/gtest.h"
#include <iostream>
#ifdef WIN32
#include <time.h>
#elif __APPLE__
#include <time.h>
#else
#include <sys/time.h>
#endif

int main(int argc, char** argv)
{
  const unsigned int randSeed = static_cast<unsigned int>(time(NULL));
  std::cout << "Random seed: " << randSeed << "." << std::endl;
  srand(randSeed);

  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
