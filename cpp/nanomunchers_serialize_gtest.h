#ifndef _HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_GTEST_H_
#define _HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_GTEST_H_
#include "nanomunchers_serialize.h"
#include "gtest/gtest.h"

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

}

#endif //_HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_GTEST_H_
