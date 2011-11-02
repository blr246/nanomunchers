#ifndef _HPS_NANOMUNCHERS_DATA_FILE_INL_
#define _HPS_NANOMUNCHERS_DATA_FILE_INL_
#include "data_file.h"
#include <algorithm>
#include <functional>
#include <cctype>

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

namespace detail
{

/// <summary> Extract typed, formatted input from a string. </summary>
template <typename Type>
inline void ExtractToken(const std::string& token, Type* out)
{
  assert(out);
  std::stringstream ssToken(token);
  ssToken >> *out;
}

// reissb -- 20111102 -- String trim functions taken from:
//   http://stackoverflow.com/questions/216823/whats-the-best-way-to-trim-stdstring
/// <summary> Trim from start. </summary>
inline std::string& LTrim(std::string* s)
{
  assert(s);
  s->erase(s->begin(), std::find_if(s->begin(), s->end(),
           std::not1(std::ptr_fun<int, int>(std::isspace))));
  return *s;
}
/// <summary> Trim from end. </summary>
inline std::string& RTrim(std::string* s)
{
  assert(s);
  s->erase(std::find_if(s->rbegin(), s->rend(),
           std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s->end());
  return *s;
}
/// <summary> Trim from both ends. </summary>
inline std::string& Trim(std::string* s)
{
  assert(s);
  return LTrim(&RTrim(s));
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
  while (file.good())
  {
    // Get comma separated line.
    std::getline(file, raw);
    detail::Trim(&raw);
    // Victims section is over?
    if (raw.empty())
    {
      // Advance to hospital ambulances.
      readState = Read_Edges;
      do
      {
        std::getline(file, raw);
        detail::Trim(&raw);
      } while (file.good() && raw.empty());
      // Ignore the second header line.
      std::getline(file, raw);
      detail::Trim(&raw);
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
        detail::ExtractToken(raw, &nodeIdRead);
        std::getline(line, raw, ',');
        valid |= !raw.empty();
        detail::ExtractToken(raw, &node.x);
        valid |= line.good();
        line >> node.y;
      }
      if (!valid)
      {
        return false;
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
        detail::ExtractToken(raw, &edge.x);
        valid |= line.good();
        line >> edge.y;
      }
      if (!valid)
      {
        return false;
      }
      assert((edge.x >= 0) && (edge.x < static_cast<int>(graphNodes.size())));
      assert((edge.y >= 0) && (edge.y < static_cast<int>(graphNodes.size())));
      // Create edge in both directions.
      graphNodes[edge.x].adjacencyList.push_back(&*graphNodes.begin() + edge.y);
      graphNodes[edge.y].adjacencyList.push_back(&*graphNodes.begin() + edge.x);
    }
  }
  return !file.bad();
}

}
using namespace nano;
}

#endif //_HPS_NANOMUNCHERS_DATA_FILE_INL_
