#include "nanomunchers_serialize.h"
#include "string_util.h"
#include <fstream>
#include <iostream>
#include <algorithm>
#include <functional>
#include <sstream>
#include <string>

namespace hps
{
namespace nano
{

namespace detail
{
/// <summary> Conversion from Muncher instruction to char. </summary>
inline char MuncherInstructionToChar(const Muncher::Instruction instr)
{
  switch (instr)
  {
  case Muncher::Up: return 'U';
  case Muncher::Down: return 'D';
  case Muncher::Left: return 'L';
  case Muncher::Right: return 'R';
  default: assert(false && "Unknown instruction"); return 'X';
  }
}

/// <summary> Conversion from char to Muncher instruction. </summary>
inline int CharToMuncherInstruction(const char c)
{
  switch (c)
  {
  case 'U': return Muncher::Up;
  case 'D': return Muncher::Down;
  case 'L': return Muncher::Left;
  case 'R': return Muncher::Right;
  default: assert(false && "Unknown instruction"); return -1;
  }
}
}

bool Serialize(const Muncher& muncher, std::ostream* stream)
{
  assert(stream);
  // Convert the program.
  char strProgram[Muncher::ProgramLength + 1] = {0};
  std::transform(muncher.program, muncher.program + Muncher::ProgramLength,
                 strProgram, std::ptr_fun(&detail::MuncherInstructionToChar));
  // Format is:
  // <time> <x> <y> <program> NEWLINE
  *stream << muncher.startTime << " "
          << muncher.startPos.x << " " << muncher.startPos.y << " "
          << strProgram << std::endl;
  return stream->good();
}

bool Deserialize(std::istream* stream, Muncher* muncher)
{
  assert(stream && muncher);
  bool parseError = false;
  // Get the full line containing the muncher.
  std::string strLine;
  std::getline(*stream, strLine);
  Trim(&strLine);
  if (strLine.empty())
  {
    parseError = true;
  }
  else
  {
    std::stringstream ssLine(strLine);
    // Read time.
    ssLine >> muncher->startTime;
    parseError |= !ssLine.good();
    // Read start position.
    ssLine >> muncher->startPos.x;
    parseError |= !ssLine.good();
    ssLine >> muncher->startPos.y;
    parseError |= !ssLine.good();
    // Read the program.
    std::string strProgram;
    ssLine >> strProgram;
    Trim(&strProgram);
    if (Muncher::ProgramLength != strProgram.size())
    {
      parseError = true;
    }
    else
    {
      // Read instructions.
      for (int idx = 0; idx < Muncher::ProgramLength; ++idx)
      {
        const int instr = detail::CharToMuncherInstruction(strProgram[idx]);
        if (instr >= 0)
        {
          muncher->program[idx] = static_cast<Muncher::Instruction>(instr);
        }
        else
        {
          parseError = true;
          break;
        }
      }
    }
  }
  return !parseError;
}


}
}
