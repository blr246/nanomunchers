#ifndef _HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_H_
#define _HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_H_
#include <vector>
#include <iosfwd>

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
  /// <summary> The where node the muncher will start executing. </summary>
  Position startPos;
  /// <summary> The muncher's program. </summary>
  Program program;
};

/// <summary> A list of munchers. </summary>
typedef std::vector<Muncher> MuncherList;

/// <summary> Serialize a muncher to string. </summary>
/// <remarks>
///   <para> Not yet implemented. </para>
/// </remarks>
void Serialize(const Muncher& mucher);

/// <summary> Serialize a list of munchers to string. <summary>
/// <remarks>
///   <para> Not yet implemented. </para>
/// </remarks>
void Serialize(const MuncherList& muchers);

/// <summary> Serialize a muncher to an ostream. <summary>
/// <remarks>
///   <para> Not yet implemented. </para>
/// </remarks>
std::ostream& operator<<(std::ostream& stream, const Muncher& mucher);

/// <summary> Serialize a list of munchers to an ostream. <summary>
/// <remarks>
///   <para> Not yet implemented. </para>
/// </remarks>
std::ostream& operator<<(std::ostream& stream, const MuncherList& mucher);


}
using namespace nano;
}

#endif //_HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_H_
