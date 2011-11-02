#include "data_file.h"
#include <fstream>

namespace hps
{
namespace nano
{

bool LoadDataFile(const std::string& filename, MuncherList* munchers)
{
  assert(munchers);
  std::ifstream file(filename.c_str());
  if (file.good())
  {
    return LoadDataFile(file, munchers);
  }
  else
  {
    return false;
  }
}

bool LoadDataFile(std::ifstream& stream, MuncherList* munchers)
{
  assert(munchers);
  
  enum ReadState { Read_Locations, Read_Edges };
  victims->clear();
  ReadState readState = Read_Locations;

  // Read and discard the header line.
  std::string raw;
  std::stringstream line;
  std::stringstream field;
  std::getline(file, raw);
  // Read the victims.
  while (file.good())
  {
    // Get comma separated line.
    std::getline(file, raw);
    // Victims section is over?
    if (raw.empty())
    {
      // Advance to hospital ambulances.
      readState = Read_HospitalAmbulances;
      do
      {
        std::getline(file, raw);
      } while (file.good() && raw.empty());
      // Ignore the hospital ambulances header line.
      std::getline(file, raw);
    }
    line.clear();
    line.str(raw);
    // Check for error.
    if (file.eof() || file.bad())
    {
      break;
    }
    if (Read_Victims == readState)
    {
      // Read fields from the line.
      victims->push_back(Victim());
      Victim& victim = victims->back();
      {
        std::getline(line, raw, ',');
        field.clear();
        field.str(raw);
        field >> victim.position.x;
        std::getline(line, raw, ',');
        field.clear();
        field.str(raw);
        field >> victim.position.y;
        line >> victim.timeToLive;
      }
    }
    else
    {
      int ambulanceCount;
      line >> ambulanceCount;
      hospitalAmbulances->push_back(ambulanceCount);
    }
  }
  return !file.bad();
}

}
}
