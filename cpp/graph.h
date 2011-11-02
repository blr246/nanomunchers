#ifndef _HPS_NANOMUNCHERS_GRAPH_H_
#define _HPS_NANOMUNCHERS_GRAPH_H_
#include <vector>

namespace hps
{
namespace nano
{

/// <summary> An unweighted, directed graph.
template <typename NodeData_>
struct Graph
{
public:
  /// <summary> Type of data stored in the graph. </summary>
  typedef NodeData_ NodeData;
  /// <summary> A graph node. </summary>
  struct Node
  {
    Node() : data(), adjacencyList() {}
    Node(const NodeData& data_) : data(data_), adjacencyList() {}
    typedef std::vector<Node*> AdjacencyList;
    NodeData data;
    AdjacencyList adjacencyList;
  };
  /// <summary> A list of graph nodes. </summary>
  typedef std::vector<Node> NodeList;

  Graph() : nodes() {}

  /// <summary> The graph nodes. </summary>
  NodeList nodes;

private:
  // Disable copy and assign.
  Graph(const Graph&);
  Graph& operator=(const Graph&);
};

}
using namespace nano;
}

#endif //_HPS_NANOMUNCHERS_GRAPH_H_
