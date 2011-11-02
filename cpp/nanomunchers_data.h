#ifndef _HPS_NANOMUNCHERS_NANOMUNCHERS_DATA_H_
#define _HPS_NANOMUNCHERS_NANOMUNCHERS_DATA_H_
#include <vector>
#include <iosfwd>
#include <assert.h>

namespace hps
{
namespace nano
{

/// <summary> A node in the graph defined by its location. </summary>
struct Position
{
  Position() : x(0), y(0) {}
  Position(const int x_, const int y_) : x(x_), y(y_) {}
  int x;
  int y;
};

/// <summary> Equality operator for Position. </sumamry>
inline bool operator==(const Position& lhs, const Position& rhs)
{
  return (lhs.x == rhs.x) && (lhs.y == rhs.y);
}

/// <summary> A muncher is deployed at a node to eat toxic waste. </summary>
struct Muncher
{
  /// <summary> Number of instructions in a muncher program. </summary>
  enum { ProgramLength = 4, };
  /// <summary> A program instruction. </summary>
  enum Instruction { Up, Down, Left, Right, };
  /// <summary> A muncher program. </summary>
  typedef Instruction Program[ProgramLength];
  /// <summary> The time that the muncher is set to start executing. </summary>
  int startTime;
  /// <summary> Where the muncher will start executing. </summary>
  Position startPos;
  /// <summary> The muncher's program. </summary>
  Program program;
};

/// <summary> Equality operator for muncher. </summary>
inline bool operator==(const Muncher& lhs, const Muncher& rhs)
{
  return (lhs.startTime) == (rhs.startTime) &&
         (lhs.startPos == rhs.startPos) &&
         std::equal(lhs.program,
                    lhs.program + Muncher::ProgramLength, rhs.program);
}

/// <summary> A list of munchers. </summary>
typedef std::vector<Muncher> MuncherList;

/// <summary> Serialize the munchers to the given stream. </summary>
/// <remarks>
///   <para> Use this function to write munchers to the nanomunchers
///     validator program.
///   </para>
/// </remakrs>
void WriteMuncherList(const MuncherList& munchers, std::ostream* stream);

}
using namespace nano;
}

#endif //_HPS_NANOMUNCHERS_NANOMUNCHERS_DATA_H_
