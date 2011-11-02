#ifndef _HPS_NANOMUNCHERS_DATA_FILE_INL_
#define _HPS_NANOMUNCHERS_DATA_FILE_INL_
#include "data_file.h"
#include "string_util.h"

namespace hps
{
namespace nano
{

template <typename LoadDataFunc, typename NodeData>
inline bool LoadDataFile(const std::string& filename, const LoadDataFunc func,
                  Graph<NodeData>* data)
{
  assert(data);
  std::ifstream file(filename.c_str());
  if (file.good())
  {
    return LoadDataFile(file, func, data);
  }
  else
  {
    return false;
  }
}

template <typename LoadDataFunc, typename NodeData>
bool LoadDataFile(std::ifstream& file, const LoadDataFunc func,
                  Graph<NodeData>* data)
{
  assert(data);
  
  enum ReadState { Read_Locations, Read_Edges };
  ReadState readState = Read_Locations;
  typename Graph<NodeData>::NodeList& graphNodes = data->nodes;
  graphNodes.clear();

  // Read and discard the header line.
  std::string raw;
  std::stringstream line;
  std::stringstream field;
  std::getline(file, raw);
  int nodeId = 0;
  // Read all data lines. Switch modes on whitespace break.
  bool readElementError = false;
  while (file.good())
  {
    // Get comma separated line.
    std::getline(file, raw);
    Trim(&raw);
    // Victims section is over?
    if (raw.empty())
    {
      // Advance to hospital ambulances.
      readState = Read_Edges;
      do
      {
        std::getline(file, raw);
        Trim(&raw);
      } while (file.good() && raw.empty());
      // Ignore the second header line.
      std::getline(file, raw);
      Trim(&raw);
    }
    // Check file finished.
    if (file.eof() || file.bad())
    {
      break;
    }
    line.clear();
    line.str(raw);
    if (Read_Locations == readState)
    {
      // Read fields from the line.
      Position node;
      bool valid = true;
      int nodeIdRead;
      {
        std::getline(line, raw, ',');
        valid |= !raw.empty();
        ExtractToken(raw, &nodeIdRead);
        std::getline(line, raw, ',');
        valid |= !raw.empty();
        ExtractToken(raw, &node.x);
        valid |= line.good();
        line >> node.y;
      }
      if (!valid)
      {
        readElementError = !valid;
        break;
      }
      assert(nodeIdRead == nodeId);
      ++nodeId;
      // Pass data to user-specified storage.
      graphNodes.push_back(typename Graph<NodeData>::Node());
      func(node, &graphNodes.back().data);
    }
    else
    {
      // Read edge.
      Position edge;
      bool valid = true;
      {
        std::getline(line, raw, ',');
        valid |= !raw.empty();
        ExtractToken(raw, &edge.x);
        valid |= line.good();
        line >> edge.y;
      }
      if (!valid)
      {
        readElementError = !valid;
        break;
      }
      assert((edge.x >= 0) && (edge.x < static_cast<int>(graphNodes.size())));
      assert((edge.y >= 0) && (edge.y < static_cast<int>(graphNodes.size())));
      // Create edge in both directions.
      graphNodes[edge.x].adjacencyList.push_back(&*graphNodes.begin() + edge.y);
      graphNodes[edge.y].adjacencyList.push_back(&*graphNodes.begin() + edge.x);
    }
  }
  return !readElementError && !file.bad();
}

}
using namespace nano;
}

#endif //_HPS_NANOMUNCHERS_DATA_FILE_INL_
