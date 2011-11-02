#ifndef _HPS_NANOMUNCHERS_DATA_FILE_H_
#define _HPS_NANOMUNCHERS_DATA_FILE_H_
#include "nanomunchers_serialize.h"
#include "graph.h"
#include <string>
#include <fstream>
#include <sstream>
#include <assert.h>

namespace hps
{
namespace nano
{

/// <summary> Load data from the file with the given name. </summary>
/// <remarks>
///   <para> The NodeData may be any type that will hold the data of where the
///     graph nodes are located. The LoadDataFunc will define a binary function
///     of the following form:
///       void LoadDataFunc::operator()(const hps::nano::Position&, NodeData*);
///     such that the position in the node may be stored within the
///     user-specified type NodeData.
/// </remarks>
template <typename LoadDataFunc, typename NodeData>
inline bool LoadDataFile(const std::string& filename, const LoadDataFunc func,
                         Graph<NodeData>* data);

/// <summary> Load data from the given stream. </summary>
/// <remarks>
///   <para> See the remarks for LoadDataFile() with a string parameter for
///     more information.
///   </para>
/// </remarks>
template <typename LoadDataFunc, typename NodeData>
bool LoadDataFile(std::ifstream& file, const LoadDataFunc func,
                  Graph<NodeData>* data);

/// <summary> Get the integer node id from an adjacency list entry. </sumamry>
template <typename NodeData>
inline int GetNodeId(const Graph<NodeData>& graph,
                     typename Graph<NodeData>::Node* node)
{
  return node - &graph.nodes.front();
}

}
using namespace nano;
}

#endif //_HPS_NANOMUNCHERS_DATA_FILE_H_
#include "data_file-inl.h"
