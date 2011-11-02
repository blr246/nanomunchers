#ifndef _HPS_NANOMUNCHERS_DATA_FILE_GTEST_H_
#define _HPS_NANOMUNCHERS_DATA_FILE_GTEST_H_
#include "data_file.h"
#include "gtest/gtest.h"
#include <math.h>

/// <summary> Ostream operator for Position used during testing. </sumamry>
inline std::ostream& operator<<(std::ostream& stream, const hps::Position& node)
{
  stream << "(" << node.x << ", " << node.y << ")";
  return stream;
}

namespace _hps_nanomunchers_data_file_gtest_h_
{
using namespace hps;

/// <summary> Simple graph type used for testing. </summary>
typedef Graph<Position> NodeGraph;

/// <summary> Print formatted output of node contents. </summary>
inline void PrintNodeInfo(const NodeGraph& graph, const int idx)
{
  const NodeGraph::Node& node = graph.nodes[idx];
  std::cout << "Node " << idx << " has position "
            << node.data << " and edges { ";
  for (int edgeIdx = 0;
       edgeIdx < static_cast<int>(node.adjacencyList.size());
       ++edgeIdx)
  {
    if (edgeIdx > 0)
    {
      std::cout << ", ";
    }
    const int otherId = GetNodeId(graph, node.adjacencyList[edgeIdx]);
    std::cout << Position(idx, otherId);
  }
  std::cout << " }." << std::endl;
}
/// <summary> Helper to load NodeGraph from data file. </summary>
struct PositionPassthroughFunc
{
  inline void operator()(const Position& node, NodeGraph::NodeData* data) const
  {
    *data = node;
  }
};
TEST(data_file, Load)
{
  // Load data_0.
  {
    SCOPED_TRACE("LoadDataFile() -- data_0");
    NodeGraph graph;
    EXPECT_TRUE(LoadDataFile("data_0", PositionPassthroughFunc(), &graph));
    const NodeGraph::NodeList& nodes = graph.nodes;
    ASSERT_EQ(127, nodes.size());
    EXPECT_EQ(Position(12, 5), nodes.front().data);
    EXPECT_EQ(Position(16, 6), nodes.back().data);
    ASSERT_EQ(3, nodes.front().adjacencyList.size());
    EXPECT_EQ(21, GetNodeId(graph, nodes.front().adjacencyList[0]));
    EXPECT_EQ(68, GetNodeId(graph, nodes.front().adjacencyList[1]));
    EXPECT_EQ(82, GetNodeId(graph, nodes.front().adjacencyList[2]));
    ASSERT_EQ(1, nodes.back().adjacencyList.size());
    EXPECT_EQ(36, GetNodeId(graph, nodes.back().adjacencyList[0]));
    // Show random node data. Why not?
    {
      const int biasedRandIdx = rand() % nodes.size();
      PrintNodeInfo(graph, biasedRandIdx);
    }
  }
  // Load data_1.
  {
    SCOPED_TRACE("LoadDataFile() -- data_1");
    NodeGraph graph;
    EXPECT_TRUE(LoadDataFile("data_1", PositionPassthroughFunc(), &graph));
    const NodeGraph::NodeList& nodes = graph.nodes;
    ASSERT_EQ(153, nodes.size());
    EXPECT_EQ(Position(10, 7), nodes.front().data);
    EXPECT_EQ(Position(6, 5), nodes.back().data);
    ASSERT_EQ(4, nodes.front().adjacencyList.size());
    EXPECT_EQ(39, GetNodeId(graph, nodes.front().adjacencyList[0]));
    EXPECT_EQ(44, GetNodeId(graph, nodes.front().adjacencyList[1]));
    EXPECT_EQ(103, GetNodeId(graph, nodes.front().adjacencyList[2]));
    EXPECT_EQ(104, GetNodeId(graph, nodes.front().adjacencyList[3]));
    ASSERT_EQ(3, nodes.back().adjacencyList.size());
    EXPECT_EQ(75, GetNodeId(graph, nodes.back().adjacencyList[0]));
    EXPECT_EQ(128, GetNodeId(graph, nodes.back().adjacencyList[1]));
    EXPECT_EQ(133, GetNodeId(graph, nodes.back().adjacencyList[2]));
    // Show random node data. Why not?
    {
      const int biasedRandIdx = rand() % nodes.size();
      PrintNodeInfo(graph, biasedRandIdx);
    }
  }
}

}

#endif //_HPS_NANOMUNCHERS_DATA_FILE_GTEST_H_
