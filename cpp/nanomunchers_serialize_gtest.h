#ifndef _HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_GTEST_H_
#define _HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_GTEST_H_
#include "nanomunchers_data.h"
#include "nanomunchers_serialize.h"
#include "gtest/gtest.h"
#include <algorithm>
#include <math.h>
#include <iostream>

namespace _hps_nanomunchers_nanomunchers_serialize_gtest_h_
{
using namespace hps;

TEST(nanomunchers_serialize, Position)
{
  // Trivial test default ctor.
  {
    Position p;
  }
  // Trivial test specialized ctor.
  {
    enum { X = 45, };
    enum { Y = 29, };
    Position p(X, Y);
    EXPECT_EQ(X, p.x);
    EXPECT_EQ(Y, p.y);
  }
}

TEST(nanomunchers_serialize, Muncher)
{
  // Number of instructions is 4.
  {
    ASSERT_EQ(4, Muncher::ProgramLength);
  }
  // Set members demo.
  {
    Muncher muncher;
    {
      muncher.startTime = 0;
      muncher.startPos.x = 55;
      muncher.startPos.x = 79;
      muncher.program[0] = Muncher::Right;
      muncher.program[1] = Muncher::Up;
      muncher.program[2] = Muncher::Left;
      muncher.program[3] = Muncher::Down;
    }
  }
}

/// <summary> Return a random muncher. </summary>
inline Muncher RandomMuncher()
{
  enum { MaxCoord = 200, };
  enum { MaxTime = 20, };
  Muncher muncher;
  muncher.startTime = rand() % MaxTime;
  muncher.startPos.x = rand() % MaxCoord;
  muncher.startPos.y = rand() % MaxCoord;
  muncher.program[0] = Muncher::Right;
  muncher.program[1] = Muncher::Up;
  muncher.program[2] = Muncher::Left;
  muncher.program[3] = Muncher::Down;
  std::random_shuffle(muncher.program,
                      muncher.program + Muncher::ProgramLength);
  return muncher;
}

TEST(nanomunchers_serialize, SerializeMuncher)
{
  enum { Iterations = 1000, };
  // Create random munchers, write them, and read them back.
  for (int iteration = 0; iteration < Iterations; ++iteration)
  {
    const Muncher muncher = RandomMuncher();
    std::stringstream ssMuncher;
    Serialize(muncher, &ssMuncher);
    Muncher readMuncher;
    Deserialize(&ssMuncher, &readMuncher);
    EXPECT_TRUE(muncher == readMuncher);
  }
}

/// <summary> Functional helper for RandomMuncher(). </summary>
struct RandomMuncherFunc
{
  inline Muncher operator()() const { return RandomMuncher(); }
};
TEST(nanomunchers_serialize, SerializeMuncherList)
{
  // Merely a visual test.
  enum { MunchersToWrite = 5, };
  MuncherList munchers(MunchersToWrite);
  std::generate(munchers.begin(), munchers.end(), RandomMuncherFunc());
  WriteMuncherList(munchers, &std::cout);
}

}

#endif //_HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_GTEST_H_
