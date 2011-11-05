#ifndef _HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_H_
#define _HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_H_
#include <iosfwd>

namespace hps
{
namespace nano
{

// Forward declarations.
struct Muncher;

/// <summary> Serialize a muncher to string. </summary>
bool Serialize(const Muncher& muncher, std::ostream* stream);

/// <summary> Deserialize a muncher from string. </summary>
bool Deserialize(std::istream* stream, Muncher* muncher);

}
using namespace nano;
}

#endif //_HPS_NANOMUNCHERS_NANOMUNCHERS_SERIALIZE_H_
